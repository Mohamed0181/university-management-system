
from odoo import fields, models


class UniversityDepartment(models.Model):
    """Used to manage department of every courses"""
    _name = 'university.department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Department"

    name = fields.Char(string="Name", help="Name of the course")
    code = fields.Char(string="Code", help="Code of the course", required=True)

    semester_ids = fields.One2many('university.semester',
                                   'department_id',
                                   string="Semester", required=1,
                                   help="List of semesters under every course")
    college_id = fields.Many2one('university.college', string='College', required=True)
