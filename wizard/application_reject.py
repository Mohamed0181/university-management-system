
from odoo import fields, models
from odoo.exceptions import ValidationError


class ApplicationReject(models.TransientModel):
    """This model for providing a rejection explanation while
        rejecting an application."""
    _name = 'application.reject'
    _description = 'Choose Reject Reason'

    reject_reason_id = fields.Many2one('reject.reason',
                                       string="Rejecting reason",
                                       help="Select Reason for "
                                            "rejecting the Applications")

    def action_reject_reason_submit(self):
        """This method writes the reject reason selected by the user to the
            application record.It then calls the `action_reject` method to
            reject the application.

            :returns class: university.application, The rejected application.
        """
        for rec in self:
            application = self.env['university.application'].browse(
                self.env.context.get('active_ids'))
            application.write({'reject_reason_id': rec.reject_reason_id.id})
            return application.action_reject()
