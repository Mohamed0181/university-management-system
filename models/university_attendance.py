
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class UniversityAttendance(models.Model):
    _name = 'university.attendance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Student Attendance"

    name = fields.Char(string="Name", default="New")
    college_id = fields.Many2one('university.college', string='College', required=True)
    department_id = fields.Many2one(
        'university.department',
        string="Department",
        domain="[('college_id', '=', college_id)]",
        required=True
    )
    batch_id = fields.Many2one('university.batch', string="Batch", required=True, domain="[('college_id', '=', college_id)]")
    faculty_id = fields.Many2one('university.doctors', string="Doctor")
    course_id = fields.Many2one('university.course', string="Course", domain="[('department_id', '=', department_id)]")

    date = fields.Date(string="Date", default=fields.Date.today, required=True)
    attendance_line_ids = fields.One2many(
        'university.attendance.line',
        'attendance_id',
        string='Attendance Line'
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], default='draft')
    is_attendance_created = fields.Boolean(string='Attendance Created')

    @api.onchange('batch_id')
    def _onchange_batch_id(self):
        if self.batch_id:
            self.is_attendance_created = False
            self.attendance_line_ids = False

    def action_create_attendance_line(self):
        if self.search_count([
            ('course_id', '=', self.course_id.id),
            ('date', '=', self.date),
            ('state', '=', 'done')
        ]) > 0:
            raise ValidationError(_('Attendance for this course on this date already exists.'))
        self.name = str(self.date)
        if len(self.batch_id.batch_student_ids) < 1:
            raise UserError(_('There are no students in this Batch'))

        for student in self.batch_id.batch_student_ids:
            self.env['university.attendance.line'].create({
                'name': self.name,
                'attendance_id': self.id,
                'student_id': student.id,
                'batch_id': self.batch_id.id,
                'date': self.date,
                'status': 'absent'
            })
        self.is_attendance_created = True

    def action_mark_all_present(self):
        for record in self.attendance_line_ids:
            record.status = 'present'

    def action_mark_all_absent(self):
        for record in self.attendance_line_ids:
            record.status = 'absent'

    def action_attendance_done(self):
        self.state = 'done'
