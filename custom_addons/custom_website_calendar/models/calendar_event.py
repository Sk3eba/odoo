from odoo import models, fields

class WebsiteCalendarEvent(models.Model):
    _name = 'website.calendar.event'
    _description = 'Website Calendar Event'

    name = fields.Char(string="Event Name", required=True)
    date = fields.Date(string="Event Date", required=True)
    color = fields.Selection([
        ('primary', 'Primary (Blue)'),
        ('success', 'Success (Green)'),
        ('danger', 'Danger (Red)'),
        ('warning', 'Warning (Yellow)'),
        ('info', 'Info (Light Blue)'),
    ], string="Color Theme", default='primary')
    description = fields.Text(string="Description")