
from odoo import fields, models


class ExamSubjectLine(models.Model):
    """For managing the subjects in the exam"""
    _name = 'exam.subject.line'
    _description = 'Subject Line of Exam'

    course_id = fields.Many2one('university.course', string="Course", required=True)

    date = fields.Date(string='Date', required=True,
                       help="Select date of the subject")
    time_from = fields.Float(string='Time From', required=True,
                             help="Enter starting time of the subject")
    time_to = fields.Float(string='Time To', required=True,
                           help="Enter ending time of the subject")
    mark = fields.Integer(string='Mark', help="Enter mark for the subject")
    exam_id = fields.Many2one('university.exam', string='Exam',
                              help="Relation to exam model")
    company_id = fields.Many2one(
        'res.company', string='Company', help="Company of the exam",
        default=lambda self: self.env.company)
