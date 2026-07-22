/** @odoo-module */
import options from "@web_editor/js/editor/snippets.options";

const CustomSlider = options.Class.extend({
    start: function () {
        this._updateInputVisuals();
        return this._super(...arguments);
    },
    onFocus: function () {
        this._updateInputVisuals();
    },
    async selectDataAttribute(previewMode, widgetValue, params) {
        await this._super(...arguments);
        this._updateInputVisuals();
    },
    _updateInputVisuals: function () {
        const min = this.$target.attr('data-min') || "0";
        const max = this.$target.attr('data-max') || "100";
        const step = this.$target.attr('data-step') || "10";
        const val = this.$target.attr('data-value') || "50";

        const $input = this.$target.find('input[type="range"]');
        $input.attr({'min': min, 'max': max, 'step': step, 'value': val});
        $input.val(val);

        // Znajduje istniejący element wyświetlający i tylko podmienia w nim wartość
        const $display = this.$target.find('.slider-value-display');
        if ($display.length) {
            $display.text(val);
        }
    }
});

options.registry.CustomSlider = CustomSlider;
export default CustomSlider;