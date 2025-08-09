from odoo import fields,models,api
class UniversityCollege(models.Model):
    _name = 'university.college'
    _description = 'University College'

    name = fields.Char(string='College Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
