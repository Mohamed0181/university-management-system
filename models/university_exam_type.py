
from odoo import fields, models


class UniversityExamType(models.Model):
    """For managing type of exams such as internal or semester"""
    _name = 'university.exam.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'University Exam Type'

    name = fields.Char(string='Name', required=True,
                       help="Name of the exam type")
    exam_type = fields.Selection(
        [('internal', 'Mid Term'), ('sem', 'Final Term')],
        string='Exam Type', default='internal',
        help="Select exam type for exams")
    company_id = fields.Many2one(
        'res.company', string='Company', help="Company of the "
                                              "exam type",
        default=lambda self: self.env.company)
