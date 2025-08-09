from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UniversityBatch(models.Model):
    _name = 'university.batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Batches"

    name = fields.Char(string="Name")
    semester_id = fields.Many2one('university.semester', string="Semester", required=True)
    academic_year_id = fields.Many2one('university.academic.year', string="Academic Year", required=True)
    batch_strength = fields.Integer(string='Batch Strength')
    college_id = fields.Many2one('university.college', string='College')
    batch_student_ids = fields.One2many('university.student', 'batch_id', string="Students")

    manual_fee_amount = fields.Float(string="قيمة المصاريف")

    def _create_or_update_fees(self):
        student_fee_model = self.env['student.fee']
        for batch in self:
            if batch.manual_fee_amount <= 0:
                continue  # أو ترفع ValidationError اذا تحب

            for student in batch.batch_student_ids:
                fee = student_fee_model.search([
                    ('student_id', '=', student.id),
                    ('semester_id', '=', batch.semester_id.id),
                    ('academic_year_id', '=', batch.academic_year_id.id),
                ], limit=1)
                if fee:
                    # تحديث قيمة المصاريف إذا اختلفت
                    if fee.amount_due != batch.manual_fee_amount:
                        fee.amount_due = batch.manual_fee_amount
                        fee.balance = fee.amount_due - fee.amount_paid
                else:
                    # إنشاء رسوم جديدة
                    student_fee_model.create({
                        'student_id': student.id,
                        'batch_id': batch.id,
                        'semester_id': batch.semester_id.id,
                        'academic_year_id': batch.academic_year_id.id,
                        'amount_due': batch.manual_fee_amount,
                        'amount_paid': 0.0,
                        'payment_status': 'unpaid',
                    })

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._create_or_update_fees()
        return record

    def write(self, vals):
        res = super().write(vals)
        if 'manual_fee_amount' in vals:
            self._create_or_update_fees()
        return res

    def action_generate_fees(self):
        self._create_or_update_fees()
        return True
