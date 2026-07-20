from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"
    name = fields.Char(required=True)

    sequence = fields.Integer('Sequence', default=1)

    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    # 1. Pole One2many relacji zwrotnej do ofert
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    
    # 2. Pole obliczeniowe (licznik)
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ("unique_property_type_name", "UNIQUE(name)", "Property type name must be unique."),
    ]