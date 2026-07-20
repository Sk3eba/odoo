from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    property_type_id = fields.Many2one(
        "estate.property.type", 
        related="property_id.property_type_id", 
        store=True,
        string="Property Type"
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity or 0)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline - base_date).days
            else:
                record.validity = 0

    

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            offer_price = vals.get("price", 0.0)
            
            if property_id:
                # Inicjalizacja obiektu nieruchomości na podstawie ID
                property_record = self.env["estate.property"].browse(property_id)
                
                # Sprawdzenie, czy nowa oferta nie jest niższa od istniejących
                if property_record.offer_ids:
                    max_offer = max(property_record.offer_ids.mapped("price"))
                    if offer_price < max_offer:
                        raise UserError(f"The offer amount must be higher than the existing highest offer: {max_offer}")
                
                # Zmiana statusu nieruchomości
                property_record.state = "offer_received"
                
        # Zapis do bazy danych
        return super().create(vals_list)
    
    def action_accept(self):
        for offer in self:
            other_offers = offer.property_id.offer_ids - offer
            other_offers.write({"status": "refused"})
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"

    _sql_constraints = [
        ("check_offer_price_positive", "CHECK(price >= 0)", "Offer price must be strictly positive."),
    ]