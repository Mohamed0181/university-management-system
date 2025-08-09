
from odoo import fields, models,api,_


class ResultsSubjectLine(models.Model):
    """Used to manage subject details of student exam result"""
    _name = 'results.subject.line'
    _description = 'Results Subject Line'

    name = fields.Char(string='Name', help="Name of the result")

    course_id = fields.Many2one(
        'university.course',
        string="Course",
        related='result_id.course_id',
        store=True,
        readonly=True
    )

    max_mark = fields.Float(string='Max Mark', help="Maximum mark of subject")
    pass_mark = fields.Float(string='Pass Mark',
                             help="Pass mark of the subject")
    mark_scored = fields.Float(string='Mark Scored',
                               help="Marks scored by the students in subjects")
    is_pass = fields.Boolean(string='Pass/Fail',
                             help="Enable if the student "
                                  "pass the subject")
    result_id = fields.Many2one('exam.result', string='Result Id',
                                help="Relation to result model")