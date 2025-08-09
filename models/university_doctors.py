from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class UniversityDoctors(models.Model):

    _name = 'university.doctors'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Faculty records"

    name = fields.Char(string='Name', required=True,
                       help="Enter the full name")

    image = fields.Binary(string="Image", attachment=True,
                          help="Image of the faculty")
    date_of_birth = fields.Date(string="Date of Birth", required=True,
                                help="Enter the DOB")
    email = fields.Char(string="Email", required=True,
                        help="Enter the Email for contact purpose")
    phone = fields.Char(string="Phone", help="Enter the Phone for contact purpose",size=11)

    mobile = fields.Char(string="Mobile", required=True,
                         help="Enter the Mobile for contact purpose",size=11)
    national_id = fields.Char(string="National ID",size=14 )
    religion = fields.Selection([('مسلم', 'مسلم'), ('مسيحى', 'مسيحى'), ], "Religion")
    nationality_id = fields.Many2one('res.country', string='Nationality', ondelete='restrict', default=lambda self: self.env['res.country'].search([('name', '=', 'Egypt')],limit=1))

    degree_id = fields.Many2one('hr.recruitment.degree',
                                string="Degree",
                                Help="Select your Highest degree")

    course_id = fields.Many2many('university.course', string="Course", required=True)
    employee_id = fields.Many2one('hr.employee',
                                  string="Related Employee",
                                  help="Related employee of faculty")
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'),],
        string='Gender', required=True, default='male',
        help="Gender of the doctor",
        track_visibility='onchange')


    def action_create_employee(self):
        """Creating the employee for the faculty"""
        for rec in self:
            emp_id = self.env['hr.employee'].create({
                'name': rec.name,
                'gender': rec.gender,
                'birthday': rec.date_of_birth,
                'image_1920': rec.image,
                'work_phone': rec.phone,
                'work_email': rec.email,
            })
            rec.employee_id = emp_id.id

    @api.onchange('date_of_birth')
    def _onchange_date_of_birth(self):
        if self.date_of_birth:
            if (fields.date.today().year - self.date_of_birth.year) < 18:
                raise ValidationError('Please provide valid date of birth')