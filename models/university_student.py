from odoo import api, fields, models,_
from odoo.api import readonly
from odoo.exceptions import ValidationError

class UniversityStudent(models.Model):
    """To keep records of university student details"""
    _name = 'university.student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}
    _description = 'University student records'

    @api.model
    def create(self, vals):
        """ This method overrides the create method to assign a sequence number
            to the newly created record.
           :param vals (dict): Dictionary containing the field values for the
                                new university student record.
           :returns class: university.student The created university student
                            record."""
        vals['admission_no'] = self.env['ir.sequence'].next_by_code(
            'university.student')
        res = super(UniversityStudent, self).create(vals)
        return res

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help="Student Partner",
        required=True,
        ondelete="cascade"
    )

    application_no = fields.Char(string="Application No",help="Application number of the student")
    date_of_birth = fields.Date(string="Date of Birth", required=True,help="Date of Birth details")
    college_id = fields.Many2one('university.college', string='College', required=True)
    semester_id = fields.Many2one('university.semester',
                                  string="Semester",
                                  help="Which semester of student is"
    )
    department_id = fields.Many2one(
        'university.department',
        string="Department",
        domain="[('college_id', '=', college_id)]",
        required=True
    )
    course_id = fields.Many2many(
        'university.course',
        string="Course",
        required=True,
        domain="[('department_id', '=', department_id)]",
        readonly=True
    )
    admission_no = fields.Char(string="Admission Number", readonly=True,
                               help="Admission no. of the student ")
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),],
                              help="Student gender details",
                              string='Gender', required=True, default='male',
                              track_visibility='onchange'
    )

    company_id = fields.Many2one('res.company', string='Faculty',help="Company")
    per_street = fields.Char(string="Street", help="Street Address")
    per_zip = fields.Char(change_default=True, string="Zip", help="Zip/Pincode details")
    per_city = fields.Char(string="City", help="Student living city")
    per_country_id = fields.Many2one('res.country',
                                     string='Country',
                                     help="Nationality of student",
                                     ondelete='restrict'
    )

    national_number = fields.Char(string="National ID",help="Student caste details")
    religion = fields.Selection([('مسلم','مسلم'),('مسيحى','مسيحى'),],"Religion")
    is_same_address = fields.Boolean(string="Is same Address?",
                                     help="Enable if student have single "
                                          "address")
    nationality_id = fields.Many2one('res.country',
                                     string='Nationality',
                                     help="Nationality of student",
                                     ondelete='restrict')
    application_id = fields.Many2one('university.application',
                                     help="Application no of student",
                                     string="Application No")
    user_id = fields.Many2one('res.users', string="User",
                              readonly=True,
                              help="Related User of the student")
    batch_id = fields.Many2one('university.batch', string="Batch",
                               help="Relation to batches of university")
    academic_year_id = fields.Many2one('university.academic.year',
                                       string="Academic Year",
                                       help="Academic year of the student")

    def action_student_documents(self):
        """ Open the documents submitted by the student along with the admission
            application. This method retrieves the documents associated with
            the admission application linked to the current student record.
            :returns dict: A dictionary defining the action to open the
                            'university.document' records."""
        self.ensure_one()
        if self.application_id.id:
            documents_list = self.env['university.document'].search(
                [('application_ref_id', '=', self.application_id.id)]).mapped(
                'id')
            return {
                'domain': [('id', 'in', documents_list)],
                'name': _('Documents'),
                'view_mode': 'list,form',
                'res_model': 'university.document',
                'view_id': False,
                'context': {'application_ref_id': self.application_id.id},
                'type': 'ir.actions.act_window'
            }

