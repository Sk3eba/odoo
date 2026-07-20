/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CustomSliderDisplay = publicWidget.Widget.extend({
    selector: '.s_website_form_field[data-type="range"]',
    events: {
        'input input[type="range"]': '_onSliderChange',
    },
    start() {
        this.$input = this.$('input[type="range"]');
        this.$display = this.$('.slider-value-display');
        
        const min = this.$el.attr('data-min') || "0";
        const max = this.$el.attr('data-max') || "100";
        const step = this.$el.attr('data-step') || "10";
        const val = this.$el.attr('data-value') || "50";

        this.$input.attr({'min': min, 'max': max, 'step': step, 'value': val});
        this.$input.val(val);
        
        this._updateDisplay();
        return this._super.apply(this, arguments);
    },
    _onSliderChange() {
        this._updateDisplay();
    },
    _updateDisplay() {
        if (this.$display.length) {
            this.$display.text(this.$input.val());
        }
    }
});