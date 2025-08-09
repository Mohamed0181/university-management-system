
from odoo import fields, models


class RejectReason(models.Model):
    """For managing rejection reasons for an application"""
    _name = 'reject.reason'
    _description = "Application reject reasons"

    name = fields.Char(string="Name", help="Reject Reasons of application")
