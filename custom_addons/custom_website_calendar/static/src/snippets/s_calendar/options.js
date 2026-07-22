/** @odoo-module **/

// W Odoo 18 tak wygląda poprawny import opcji edytora
import options from "@web_editor/js/editor/snippets.options";

options.registry.CustomWebsiteCalendarOptions = options.Class.extend({
    // Upewnij się, że selektor zgadza się z klasą w XML
    // W XML powinno to wyglądać np. tak: data-snippet="s_calendar" lub podobnie
    
    start: function () {
        // Ta funkcja wywołuje się, gdy klikniesz snippet w edytorze Odoo
        return this._super.apply(this, arguments);
    },

    // Tutaj w przyszłości dodamy opcje (np. zmianę kolorów),
    // ale na razie wystarczy pusty szkielet, aby pozbyć się błędu!
});