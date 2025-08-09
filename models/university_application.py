from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class UniversityApplication(models.Model):
    _name = 'university.application'
    _inherit = ['mail.thread']
    _description = 'Applications for the admission'

    _sql_constraints = [('unique_name', 'unique("name")', 'This name already exists'),
                        ('unique_national_number', 'unique("national_number")', 'The national ID already exists'),
                        ('unique_phone', 'unique("phone")', 'This number already exists'),
                        ('unique_email', 'unique("email")', 'This email already exists'),
                        ('unique_mobile', 'unique("mobile")', 'This number already exists'),
                        ]

    @api.model
    def create(self, vals):
        if vals.get('application_no', _('New')) == _('New'):
            vals['application_no'] = self.env['ir.sequence'].next_by_code(
                'university.application') or _('New')
        res = super(UniversityApplication, self).create(vals)
        return res

    name = fields.Char(string='Name', required=True, help="Enter Name of Student")
    national_number = fields.Char(string='National ID',size=14,required=True,)
    image = fields.Binary(string='Image', attachment=True, help="Provide the image of the Student")
    academic_year_id = fields.Many2one('university.academic.year', string='Academic Year')

    college_id = fields.Many2one('university.college', string='College', required=True)

    department_id = fields.Many2one(
        'university.department',
        string="Department",
        domain="[('college_id', '=', college_id)]",
        required=True
    )

    semester_ids = fields.Many2many('university.semester', string="Semester", compute="_compute_semester_ids")
    semester_id = fields.Many2one('university.semester', string="Semester", required=True)
    batch_ids = fields.Many2many('university.batch', string="Batch",    compute="_compute_batch_ids" )
    batch_id = fields.Many2one(
        'university.batch',
        string="Batch",
        domain="[('college_id', '=', college_id)]"
    )
    admission_date = fields.Datetime('Admission Date', default=fields.Datetime.now, required=True)
    application_no = fields.Char(string='Application No', readonly=True, default=lambda self: _('New'))


    is_same_address = fields.Boolean(string="Permanent Address same as above", default=True)
    email = fields.Char(string="Email", required=True,)
    phone = fields.Char(string="Phone",size=11)
    mobile = fields.Char(string="Mobile", required=True,size=11)

    nationality_id = fields.Many2one('res.country', string='Nationality', ondelete='restrict', default=lambda self: self.env['res.country'].search([('name', '=', 'Egypt')],limit=1))

    religion = fields.Selection([('مسلم','مسلم'),('مسيحى','مسيحى'),],"Religion")

    # Current Address
    street = fields.Char(string='Address')
    zip = fields.Char(change_default=True, string='ZIP code')
    city = fields.Char(string='City')
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    # Permanent Address
    per_street = fields.Char(string="Permanent Street", help="Enter the permanent address")
    per_zip = fields.Char(change_default=True, string='ZIP code')
    per_city = fields.Char(string='City')
    per_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    date_of_birth = fields.Date(string="Date of Birth", required=True)
    description = fields.Text(string="Note")

    active = fields.Boolean(string='Active', default=True)
    document_count = fields.Integer(compute='_compute_document_count', string='# Documents')
    verified_by_id = fields.Many2one('res.users', string='Verified by')
    reject_reason_id = fields.Many2one('reject.reason', string='Reject Reason')

    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True, default='male', track_visibility='onchange')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('verification', 'Verify'),
        ('approve', 'Approve'),
        ('reject', 'Rejected'),
        ('done', 'Done')], string='State', required=True, default='draft', track_visibility='onchange')

    prev_institute = fields.Char('Previous Institute')
    prev_course = fields.Char('Previous Course')
    prev_result = fields.Char('Previous Result')

    def _compute_document_count(self):
        for rec in self:
            rec.document_count = self.env['university.document'].search_count([('application_ref_id', '=', rec.id)])

    def action_document_view(self):
        return {
            'name': _('Documents'),
            'domain': [('application_ref_id', '=', self.id)],
            'res_model': 'university.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'list,form',
            'context': {'default_application_ref_id': self.id}
        }

    def action_send_verification(self):
        for rec in self:
            if not self.env['university.document'].search([('application_ref_id', '=', rec.id)]):
                raise ValidationError(_('No Documents provided'))
            rec.write({'state': 'verification'})

    def action_verify_application(self):
        for rec in self:
            doc_status = self.env['university.document'].search([('application_ref_id', '=', rec.id)]).mapped('state')
            if doc_status:
                if all(state in 'done' for state in doc_status):
                    rec.write({
                        'verified_by_id': self.env.uid,
                        'state': 'approve'
                    })
                else:
                    raise ValidationError(_('All Documents are not Verified Yet, Please complete the verification'))
            else:
                raise ValidationError(_('No Documents provided'))

    def action_reject(self):
        for rec in self:
            rec.write({'state': 'reject'})

    def action_create_student(self):
        for rec in self:
            values = {
                'name': rec.name,
                'department_id': rec.department_id.id,
                'application_id': rec.id,
                'street': rec.street,
                'city': rec.city,
                'country_id': rec.country_id.id,
                'zip': rec.zip,
                'per_street': rec.per_street,
                'per_city': rec.per_city,
                'per_country_id': rec.per_country_id.id,
                'per_zip': rec.per_zip,
                'gender': rec.gender,
                'date_of_birth': rec.date_of_birth,
                'nationality_id': rec.nationality_id.id,
                'email': rec.email,
                'mobile': rec.mobile,
                'phone': rec.phone,
                'image_1920': rec.image,
                'is_student': True,
                'religion': rec.religion,
                'semester_id': rec.semester_id.id,
                'academic_year_id': rec.academic_year_id.id,
                'batch_id': rec.batch_id.id,
                'national_number': rec.national_number,
                'college_id':rec.college_id.id,
            }
            if rec.is_same_address:
                values.update({
                    'per_street': rec.street,
                    'per_city': rec.city,
                    'per_country_id': rec.country_id.id,
                    'per_zip': rec.zip,
                })
            student = self.env['university.student'].create(values)
            student.user_id = self.env['res.users'].create({
                'name': student.name,
                'login': student.email,
                'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
            })
            rec.write({'state': 'done'})
            return {
                'name': _('Student'),
                'view_mode': 'form',
                'res_model': 'university.student',
                'type': 'ir.actions.act_window',
                'res_id': student.id,
                'context': self.env.context
            }

    @api.depends()
    def _compute_department_ids(self):
        for rec in self:
            rec.department_ids = self.env['university.department'].search([])

    @api.depends('department_id')
    def _compute_semester_ids(self):
        for rec in self:
            rec.semester_ids = self.env['university.semester'].search([('department_id', '=', rec.department_id.id)]).ids if rec.department_id else False

    @api.depends('semester_id')
    def _compute_batch_ids(self):
        for rec in self:
            rec.batch_ids = self.env['university.batch'].search([('semester_id', '=', rec.semester_id.id)]).ids if rec.semester_id else False

    @api.onchange('date_of_birth')
    def _onchange_date_of_birth(self):
        if self.date_of_birth:
            if (fields.date.today().year - self.date_of_birth.year) < 18:
                raise ValidationError(_('Please provide valid date of birth'))



