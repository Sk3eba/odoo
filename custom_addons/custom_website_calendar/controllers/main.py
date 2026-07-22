from odoo import http
from odoo.http import request

class WebsiteCalendar(http.Controller):

    @http.route('/website_calendar/get_events', type='json', auth='public', website=True)
    def get_calendar_events(self):
        events = request.env['website.calendar.event'].search([])
        
        # Sprawdzamy uprawnienia na podstawie faktycznego UID w sesji żądania
        user = request.env.user
        if request.session.uid:
            user = request.env['res.users'].browse(request.session.uid)
            
        is_admin = user.has_group('website.group_website_designer')
        
        return {
            'result': events.read(['name', 'date', 'color', 'description']),
            'is_admin': is_admin
        }

    @http.route('/website_calendar/add_event', type='json', auth='user', website=True)
    def add_calendar_event(self, date, name, color=None):
        # Sprawdzamy, czy użytkownik ma uprawnienia administratora/designera strony
        if not request.env.user.has_group('website.group_website_designer'):
            return {'success': False, 'error': 'Brak uprawnień'}

        # Zabezpieczenie przed pustymi danymi
        if not date or not name:
            return {'success': False, 'error': 'Brak wymaganych danych'}

        # Tworzenie rekordu w modelu wydarzeń kalendarza
        request.env['website.calendar.event'].create({
            'name': name,
            'date': date,
        })
        
        return {'success': True}

    @http.route('/website_calendar/delete_event', type='json', auth='user', website=True)
    def delete_calendar_event(self, event_id):
        # Sprawdzanie uprawnień administratora/designera
        #if not request.env.user.has_group('website.group_website_designer'):
            #return {'success': False, 'error': 'Brak uprawnień'}

        event = request.env['website.calendar.event'].browse(event_id)
        if event.exists():
            event.unlink()
            return {'success': True}
            
        return {'success': False, 'error': 'Wydarzenie nie istnieje'}