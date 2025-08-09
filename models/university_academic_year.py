
from odoo import fields, models


class UniversityAcademicYear(models.Model):
    """For managing university academic year"""
    _name = 'university.academic.year'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Academic Year"

    name = fields.Char(string="Name", help="Name of the academic year")
    start_date = fields.Date(string="Start Date", required=True,
                             help="Enter the start date of the academic year")
    end_date = fields.Date(string="End Date", required=True,
                           help="Enter the end date of the academic year")
    is_active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the Academic "
             "Year without removing it.")
