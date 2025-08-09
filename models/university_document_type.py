from odoo import fields, models

class UniversityDocumentType(models.Model):
    """For managing document types in the document"""
    _name = 'university.document.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "University Document Type"

    name = fields.Char(string="Name", help="Name of the document type")
    description = fields.Char(string="Description",
                              help="Description about type")
