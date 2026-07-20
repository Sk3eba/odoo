from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # Wywołanie oryginalnej metody (zmiana stanu na 'sold')
        res = super().action_sold()
        
        # Iterujemy przez każdą sprzedawaną nieruchomość (self może być recordsetem)
        for record in self:
            # Tworzenie faktury (account.move)
            self.env["account.move"].create({
                "partner_id": record.buyer_id.id,  #
                "move_type": "out_invoice",        # 'out_invoice' to techniczna nazwa 'Customer Invoice'
                "invoice_line_ids": [
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06, # Przykładowa prowizja 6%
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100.0,
                    }),
                ],
            })
            
        return res