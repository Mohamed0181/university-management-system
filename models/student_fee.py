from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StudentFee(models.Model):
    _name = 'student.fee'
    _description = 'Student Fee'

    student_id = fields.Many2one('university.student', string='Student', required=True)
    batch_id = fields.Many2one('university.batch', string='Batch', required=True)
    semester_id = fields.Many2one('university.semester', string='Semester', required=True)
    academic_year_id = fields.Many2one('university.academic.year', string='Academic Year', required=True)

    amount_due = fields.Float(string='Amount Due', required=True)
    amount_paid = fields.Float(string='Amount Paid', default=0.0)
    payment_date = fields.Date(string='Payment Date')

    balance = fields.Float(string='Remaining Amount', compute='_compute_balance', store=True)
    payment_status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid')
    ], string='Payment Status', compute='_compute_status', store=True)

    @api.depends('amount_due', 'amount_paid')
    def _compute_balance(self):
        for record in self:
            record.balance = record.amount_due - record.amount_paid

    @api.depends('amount_due', 'amount_paid')
    def _compute_status(self):
        for record in self:
            balance = record.amount_due - record.amount_paid
            if balance == 0:
                record.payment_status = 'paid'
            elif record.amount_paid == 0:
                record.payment_status = 'unpaid'
            else:
                record.payment_status = 'partial'

    @api.onchange('student_id')
    def _onchange_student_id(self):
        for rec in self:
            if rec.student_id:
                rec.batch_id = rec.student_id.batch_id.id if rec.student_id.batch_id else False
                rec.semester_id = rec.student_id.semester_id.id if rec.student_id.semester_id else False
                rec.academic_year_id = rec.student_id.academic_year_id.id if rec.student_id.academic_year_id else False
            else:
                rec.batch_id = False
                rec.semester_id = False
                rec.academic_year_id = False

    @api.constrains('amount_paid', 'payment_date')
    def _check_payment_date(self):
        for record in self:
            if record.amount_paid > 0 and not record.payment_date:
                raise ValidationError('يجب تحديد تاريخ الدفع عند وجود مبلغ مدفوع.')

    @api.constrains('amount_due', 'amount_paid')
    def _check_amounts(self):
        for record in self:
            if record.amount_due < 0:
                raise ValidationError('المبلغ المستحق لا يمكن أن يكون سالبًا.')
            if record.amount_paid < 0:
                raise ValidationError('المبلغ المدفوع لا يمكن أن يكون سالبًا.')

    _sql_constraints = [
        ('unique_fee_per_student_semester',
         'unique(student_id, semester_id, academic_year_id)',
         'تم تسجيل رسوم هذا الطالب مسبقًا لهذا الترم والسنة الأكاديمية.')
    ]