from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StudentFee(models.Model):
    _name = 'student.fee'
    _description = 'Student Fee'

    student_id = fields.Many2one('university.student', string='Student', required=True)
    batch_id = fields.Many2one('university.batch', string='Batch', required=True)
    semester_id = fields.Many2one('university.semester', string='Semester', required=True)
    academic_year_id = fields.Many2one('university.academic.year', string='Academic Year', required=True)

    amount_due = fields.Float(string='Amount Due', compute='_compute_amount_due', store=True)
    amount_paid = fields.Float(string='Amount Paid', required=True, default=0.0)
    payment_date = fields.Date(string='Payment Date')

    balance = fields.Float(string='Remaining Amount', compute='_compute_amounts', store=True)
    payment_status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid')
    ], string='Payment Status', compute='_compute_payment_status', store=True, tracking=True)

    fee_line_ids = fields.One2many('student.fee.line', 'fee_id', string='Course Fees')

    @api.depends('batch_id.manual_fee_amount')
    def _compute_amount_due(self):
        for record in self:
            record.amount_due = record.batch_id.manual_fee_amount or 0.0

    @api.depends('amount_paid', 'amount_due')
    def _compute_amounts(self):
        for record in self:
            record.balance = record.amount_due - record.amount_paid

    @api.depends('amount_due', 'amount_paid')
    def _compute_payment_status(self):
        for record in self:
            if record.amount_paid == 0:
                record.payment_status = 'unpaid'
            elif record.amount_paid >= record.amount_due:
                record.payment_status = 'paid'
            else:
                record.payment_status = 'partial'

    @api.constrains('amount_paid')
    def _check_amount_paid(self):
        for record in self:
            if record.amount_paid < 0:
                raise ValidationError("المبلغ المدفوع لا يمكن أن يكون سالبًا.")
            if record.amount_paid > record.amount_due:
                raise ValidationError("المبلغ المدفوع لا يمكن أن يتجاوز المبلغ المستحق.")

    @api.onchange('student_id')
    def _onchange_student_id(self):
        for rec in self:
            if rec.student_id:
                rec.batch_id = rec.student_id.batch_id.id
                rec.semester_id = rec.student_id.semester_id.id
                rec.academic_year_id = rec.student_id.academic_year_id.id

    _sql_constraints = [
        ('unique_fee_per_student_semester',
         'unique(student_id, semester_id, academic_year_id)',
         'تم تسجيل رسوم هذا الطالب مسبقًا لهذا الترم والسنة الأكاديمية.')
    ]

    def action_pay_fee(self):
        
        # زر دفع: نفتح نافذة لتسجيل الدفع أو ببساطة نحدث amount_paid مباشرةً
        for record in self:
            if record.payment_status == 'paid':
                continue  # تم الدفع بالكامل مسبقًا
            # مثال تحديث مبلغ الدفع ليغطي كامل الرسوم:
            record.amount_paid = record.amount_due
            record.payment_date = fields.Date.today()




class StudentFeeLine(models.Model):
    _name = 'student.fee.line'
    _description = 'Student Fee Line'

    fee_id = fields.Many2one('student.fee', string='Fee', required=True, ondelete='cascade')
    course_id = fields.Many2one('university.course', string='Course', required=True)
    course_fee = fields.Float(string='Course Fee', required=True)

    _sql_constraints = [
        ('unique_course_per_fee',
         'unique(fee_id, course_id)',
         'لا يمكن تسجيل نفس المادة أكثر من مرة في نفس الرسوم.')
    ]


from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CourseRegistration(models.Model):
    _name = 'course.registration'
    _description = 'Course Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Many2one('university.student', string='Student', required=True)

    semester_id = fields.Many2one('university.semester', string='Semester', required=True)
    batch_id = fields.Many2one('university.batch', string='Batch', required=True)
    academic_year_id = fields.Many2one('university.academic.year', string="Academic Year", required=True)
    registration_date = fields.Date(string="Registration Date", default=fields.Date.today)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string="Status", default='draft', tracking=True)

    course_line_ids = fields.One2many('course.registration.line', 'registration_id', string='Courses',)

    @api.model
    def create(self, vals):
        student_id = vals.get('student_id')
        semester_id = vals.get('semester_id')
        batch_id = vals.get('batch_id')
        academic_year_id = vals.get('academic_year_id')

        fee_record = self.env['student.fee'].search([
            ('student_id', '=', student_id),
            ('semester_id', '=', semester_id),
            ('batch_id', '=', batch_id),
            ('academic_year_id', '=', academic_year_id),
            ('payment_status', '=', 'paid')
        ], limit=1)

        if not fee_record:
            raise ValidationError("لا يمكن تسجيل المادة. يجب دفع رسوم هذا الترم أولاً.")

        return super().create(vals)

    @api.onchange('student_id')
    def _onchange_student_id(self):
        if self.student_id:
            self.semester_id = self.student_id.semester_id.id
            self.batch_id = self.student_id.batch_id.id
            self.academic_year_id = self.student_id.academic_year_id.id

    def action_confirm_registration(self):
        for rec in self:
            rec.state = 'confirmed'
            # اجلب الكورسات المسجلة
            course_ids = rec.course_line_ids.mapped('course_id').ids
            # أضفها إلى سجل الطالب
            rec.student_id.course_id = [(6, 0, course_ids)]


class CourseRegistrationLine(models.Model):
    _name = 'course.registration.line'
    _description = 'Course Registration Line'

    registration_id = fields.Many2one('course.registration', string='Registration', required=True, ondelete='cascade')
    course_id = fields.Many2one('university.course', string='Course', required=True)

    _sql_constraints = [
        ('unique_course_per_registration',
         'unique(registration_id, course_id)',
         'لا يمكن تسجيل نفس المادة مرتين في نفس التسجيل.')
    ]
