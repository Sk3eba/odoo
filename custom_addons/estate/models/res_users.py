from odoo import models, fields

class ResUsers(models.Model):
    # Wskazujemy model, który chcemy rozszerzyć
    _inherit = "res.users"

    # Relacja zwrotna do nieruchomości. 
    # Domena zapewnia, że wyświetlą się tylko dostępne nieruchomości (np. pomijając 'sold' czy 'canceled')
    property_ids = fields.One2many(
        "estate.property", 
        "seller_id", 
        string="Properties",
        domain=[('state', 'in', ['new', 'offer_received'])]
    )