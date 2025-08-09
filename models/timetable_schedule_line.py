
from odoo import api, fields, models


class TimeTableScheduleLine(models.Model):
    """ Manages the schedule for subjects and faculty while
        creating timetable"""
    _name = 'timetable.schedule.line'
    _description = 'Timetable Schedule'
    _rec_name = 'period_id'

    period_id = fields.Many2one('timetable.period',
                                string="Period", required=True,
                                help="select period")
    faculty_id = fields.Many2one('university.doctors',
                                 string='Doctor', required=True,
                                 help="Set faculty who is taking ")
    time_from = fields.Float(string='From', related='period_id.time_from',
                             readonly=False,
                             help="Start and End time of Period.")
    time_till = fields.Float(string='Till', related='period_id.time_to',
                             readonly=False,
                             help="Start and End time of Period.")

    course_id = fields.Many2one('university.course', string="Course", required=True, )
    week_day = fields.Selection([
        ('0', 'Saturday'),
        ('1', 'Sunday'),
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday'),
        ('6', 'Friday'),

        ('0', 'Saturday'),
    ], string='Week', required=True, help="Select week for scheduling period")
    timetable_id = fields.Many2one('university.timetable',
                                   required=True, string="Timetable",
                                   help="Relation to university.timetable")
    batch_id = fields.Many2one('university.batch', string='Batch',
                               help="Batch")

    @api.model
    def create(self, vals):
        """ This method overrides the create method to automatically store
            :param vals (dict): Dictionary containing the field values for the
                                new timetable schedule line.
            :returns class:`timetable.schedule.line`The created timetable
                            schedule line record. """
        res = super(TimeTableScheduleLine, self).create(vals)
        res.batch_id = res.timetable_id.batch_id.id
        return res

    time_from_str = fields.Char(string="Time From (Formatted)", compute="_compute_time_strings")
    time_till_str = fields.Char(string="Time Till (Formatted)", compute="_compute_time_strings")

    @api.depends('time_from', 'time_till')
    def _compute_time_strings(self):
        for rec in self:
            rec.time_from_str = self.env['university.timetable']._format_float_time(rec.time_from)
            rec.time_till_str = self.env['university.timetable']._format_float_time(rec.time_till)
