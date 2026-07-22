/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToElement } from "@web/core/utils/render";

publicWidget.registry.CustomWebsiteCalendar = publicWidget.Widget.extend({
    selector: '.s_calendar',
    
    events: {
        'click': '_onAnyClick',
        'click .btn-prev-month': '_onPrevMonth',
        'click .btn-next-month': '_onNextMonth',
        'click .calendar-day-cell': '_onDayClick',
        'click .btn-save-event': '_onSaveEvent',
    },

    start: function () {
        console.log("KALENDARZ: Widget próbuje wystartować!");
        const def = this._super.apply(this, arguments);
        this.container = this.el.querySelector('.o_s_calendar_widget');
        this.currentDate = new Date();
        
        // POBIERAMY UPRAWNIENIA BEZPOŚREDNIE Z HTML (DOM)
        const wrapper = this.el.querySelector('.s_calendar_wrapper');
        this.isAdmin = wrapper ? wrapper.getAttribute('data-is-admin') === 'true' : false;
        
        console.log("KALENDARZ: Uprawnienia admina z DOM:", this.isAdmin);

        this.selectedDate = null;

        if (this.container) {
            this._fetchEvents().then(() => this._renderCalendar());
        }
        return def;
    },

    _fetchEvents: async function () {
        try {
            const response = await fetch('/website_calendar/get_events', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ jsonrpc: "2.0", method: "call", params: {} })
            });
            const data = await response.json();
            
            // Standardowa odpowiedź JSON-RPC w Odoo ma strukturę data.result
            // Jeśli Twój kontroler zwraca bezpośrednio słownik, dane są w data.result
            const res = data.result || {};
            
            this.events = res.result || res.events || [];
            this.isAdmin = res.is_admin || false;
            
            console.log("KALENDARZ: Wczytano wydarzenia. Uprawnienia admina z serwera:", this.isAdmin);
            
        } catch (e) {
            console.error("Error fetching events:", e);
            this.events = [];
            this.isAdmin = false;
        }
    },

    _renderCalendar: function () {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const startDayIndex = firstDay === 0 ? 6 : firstDay - 1; 

        let weeks = [];
        let currentWeek = [];
        let dayCount = 1;

        for (let i = 0; i < 42; i++) {
            if (i > 0 && i % 7 === 0) {
                weeks.push(currentWeek);
                currentWeek = [];
            }
            
            let fullDateStr = "";
            let isCurrent = false;
            let displayDay = "";

            if (i >= startDayIndex && dayCount <= daysInMonth) {
                fullDateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(dayCount).padStart(2, '0')}`;
                isCurrent = true;
                displayDay = dayCount;
                dayCount++;
            }

            const dayEvents = this.events.filter(e => e.date === fullDateStr);
            
            currentWeek.push({
                is_current_month: isCurrent,
                day_num: displayDay,
                full_date: fullDateStr,
                events: dayEvents
            });
        }
        if (currentWeek.length > 0) weeks.push(currentWeek);

        const renderedEl = renderToElement("custom_website_calendar.calendar_template", {
            weeks: weeks,
            monthName: monthNames[month],
            year: year,
            isAdmin: true
        });

        this.container.innerHTML = '';
        this.container.appendChild(renderedEl);
    },

    _onDayClick: function (ev) {
        console.log("KALENDARZ: Kliknięto dzień!");
        
        const clickedCell = ev.currentTarget;
        this.selectedDate = clickedCell.getAttribute('data-date');
        
        if (!this.selectedDate) return;

        // 1. Ustawienie daty w nagłówku modala
        const displayDateEl = document.querySelector('#modalDisplayDate');
        if (displayDateEl) {
            displayDateEl.textContent = this.selectedDate;
        }

        // 2. Wylistowanie wydarzeń z przyciskiem usuwania (X)
        const renderEventsList = () => {
            const eventsListEl = document.querySelector('#modalEventsList');
            if (!eventsListEl) return;
            
            eventsListEl.innerHTML = '';
            const dayEvents = this.events.filter(e => e.date === this.selectedDate);
            
            if (dayEvents.length > 0) {
                dayEvents.forEach(evItem => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item d-flex justify-content-between align-items-center py-2';
                    
                    const spanName = document.createElement('span');
                    spanName.textContent = evItem.name;
                    li.appendChild(spanName);

                    // Przycisk usuwania (X) widoczny tylko dla admina
                    if (this.isAdmin) {
                        const deleteBtn = document.createElement('button');
                        deleteBtn.className = 'btn btn-sm btn-outline-danger border-0';
                        deleteBtn.innerHTML = '<i class="fa fa-times"/>';
                        deleteBtn.title = "Remove event";
                        
                        deleteBtn.addEventListener('click', async () => {
                            await this._deleteEvent(evItem.id);
                            await this._fetchEvents();
                            renderEventsList();
                            this._renderCalendar();
                        });
                        li.appendChild(deleteBtn);
                    }

                    eventsListEl.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.className = 'list-group-item text-muted fst-italic';
                li.textContent = 'No events.';
                eventsListEl.appendChild(li);
            }
        };

        renderEventsList();

        // 3. Czyszczenie inputa nowego wydarzenia
        const nameInputEl = document.querySelector('#eventNameInput');
        if (nameInputEl) {
            nameInputEl.value = '';
        }
        
        // 4. Otwarcie modala
        const modalEl = document.querySelector('#calendarAddEventModal');
        if (modalEl) {
            $(modalEl).modal('show');
        }
    },

    // Nowa pomocnicza funkcja do usuwania
    _deleteEvent: async function (eventId) {
        try {
            const response = await fetch('/website_calendar/delete_event', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    jsonrpc: "2.0",
                    method: "call",
                    params: { event_id: eventId } // Klucz musi pasować do argumentu w metodzie Pythona (event_id)
                })
            });
            const data = await response.json();
            console.log("KALENDARZ: Wynik usuwania:", data);
            
            if (data.error) {
                console.error("Błąd Odoo RPC:", data.error);
                alert("Błąd serwera podczas usuwania.");
            }
        } catch (e) {
            console.error("Błąd sieci podczas usuwania:", e);
        }
    },

    _onSaveEvent: async function (ev) {
        ev.preventDefault();
        
        // Szukamy elementów w całym dokumencie, bo modal renderuje się dynamicznie
        const nameInput = document.querySelector('#eventNameInput');
        const colorSelect = document.querySelector('#eventColorSelect');
        
        const name = nameInput ? nameInput.value : '';
        const color = colorSelect ? colorSelect.value : '';

        if (!name) return alert("Please enter an event name.");

        const saveButton = ev.currentTarget;
        saveButton.disabled = true;
        const originalText = saveButton.textContent;
        saveButton.textContent = "Saving...";

        try {
            const response = await fetch('/website_calendar/add_event', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    jsonrpc: "2.0", 
                    method: "call", 
                    params: {
                        name: name,
                        date: this.selectedDate,
                        color: color
                    }
                })
            });
            const data = await response.json();
            
            if (data.result && data.result.success) {
                // Zamknij modal przez jQuery
                const modalEl = document.querySelector('#calendarAddEventModal');
                if (modalEl) {
                    $(modalEl).modal('hide');
                }
                
                // Odśwież kalendarz
                await this._fetchEvents();
                this._renderCalendar();
            } else {
                alert("Failed to save event. You might not have permission.");
            }
        } catch (e) {
            console.error(e);
        } finally {
            saveButton.disabled = false;
            saveButton.textContent = originalText;
        }
    },

    _onPrevMonth: function (ev) {
        ev.preventDefault();
        this.currentDate.setMonth(this.currentDate.getMonth() - 1);
        this._renderCalendar();
    },

    _onNextMonth: function (ev) {
        ev.preventDefault();
        this.currentDate.setMonth(this.currentDate.getMonth() + 1);
        this._renderCalendar();
    },

    _onAnyClick: function (ev) {
        console.log("TEST: Kliknąłeś w element ->", ev.target.tagName, "| Klasy CSS:", ev.target.className);
    },
});