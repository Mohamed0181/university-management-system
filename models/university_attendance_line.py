from odoo import models, fields

class UniversityAttendanceLine(models.Model):
    _name = 'university.attendance.line'
    _description = 'Attendance Line'

    name = fields.Char(string='Name', compute='_compute_name', store=True)  # حقل محسوب أو يدوي
    attendance_id = fields.Many2one('university.attendance', string="Attendance", required=True, ondelete='cascade')
    student_id = fields.Many2one('university.student', string="Student", required=True)
    batch_id = fields.Many2one('university.batch', string="Batch", related='attendance_id.batch_id',store=True)
    date = fields.Date(string="Date", related='attendance_id.date', store=True)
    status = fields.Selection([
        ('present', 'حاضر'),
        ('absent', 'غائب'),
    ], string="الحالة", required=True, default='absent')

    def _compute_name(self):
        for record in self:
            record.name = f"{record.student_id.name} - {record.date or ''}"  # مثال: اسم الطالب + التاريخ