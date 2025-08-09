
from odoo import api, fields, models


class UniversitySemester(models.Model):
    """Used to manage the semester of department"""
    _name = 'university.semester'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Semester"

    name = fields.Char(string="Name", help="Name of the semester",required=True)
    semester_no = fields.Integer(string="Semester", help="Semester number",
                                 required=True)
    department_id = fields.Many2one('university.department',
                                    string="Department",
                                    required=True,
                                    help="In which department the semester "
                                         "belongs to")
