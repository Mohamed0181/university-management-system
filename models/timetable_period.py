
from odoo import fields, models


class TimetablePeriod(models.Model):
    """Manages the period details """
    _name = 'timetable.period'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Timetable Period'

    name = fields.Char(string="Name", required=True, help="Enter Period Name")
    time_from = fields.Float(string='From', required=True,
                             help="Start and End time of Period.")
    time_to = fields.Float(string='To', required=True,
                           help="Start and End time of Period.")
    college_id = fields.Many2one('university.college', string='College', required=True)