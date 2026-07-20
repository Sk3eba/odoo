from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()

    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.context_today(self) + timedelta(days=90)
    )

    expected_price = fields.Float(required=True)

    selling_price = fields.Float(readonly=True, copy=False)

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new'
    )

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled properties cannot be sold.")
            record.state = "sold"

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be canceled.")
            record.state = "canceled"

    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.partner", string="Salesman", default=lambda self: self.env.user)

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.constrains('expected_price', 'selling_price')
    def _check_price_difference(self):
        for record in self:
            # Pomijamy sprawdzanie, jeśli cena sprzedaży wynosi 0 (czyli oferta nie została jeszcze zaakceptowana)
            if not float_is_zero(record.selling_price, precision_digits=2):
                # Obliczamy 90% oczekiwanej ceny
                lowest_accepted_price = record.expected_price * 0.90
                
                # Porównujemy ceny. float_compare zwraca -1, jeśli pierwsza wartość jest mniejsza
                if float_compare(record.selling_price, lowest_accepted_price, precision_digits=2) < 0:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price.")
                
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError("You can only delete properties in 'New' or 'Canceled' state.")

    _sql_constraints = [
        ("check_expected_price_positive", "CHECK(expected_price >= 0)", "Expected price must be strictly positive."),
        ("check_selling_price_positive", "CHECK(selling_price >= 0)", "Selling price must be positive."),
    ]