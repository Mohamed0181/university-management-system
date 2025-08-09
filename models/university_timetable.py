
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class UniversityTimeTable(models.Model):
    """Manages the timetable of every batch"""
    _name = 'university.timetable'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Timetable'

    name = fields.Char(string="Name", compute="_compute_name",help="Name of the timetable")

    college_id = fields.Many2one('university.college', string='College', required=True)
    batch_id = fields.Many2one(
        'university.batch',
        string="Batch",
        domain="[('college_id', '=', college_id)]"
    )
    academic_year_id = fields.Many2one(related="batch_id.academic_year_id",
                                       help="Batch academic year",
                                       string='Academic Year')
    mon_timetable_ids = fields.One2many('timetable.schedule.line',
                                        'timetable_id',
                                        help="Scheduled line of Monday",
                                        domain=[('week_day', '=', '2')])
    tue_timetable_ids = fields.One2many('timetable.schedule.line',
                                        'timetable_id',
                                        help="Scheduled line of Tuesday",
                                        domain=[('week_day', '=', '3')])
    wed_timetable_ids = fields.One2many('timetable.schedule.line',
                                        'timetable_id',
                                        help="Scheduled line of Wednesday",
                                        domain=[('week_day', '=', '4')])
    thur_timetable_ids = fields.One2many('timetable.schedule.line',
                                         'timetable_id',
                                         help="Scheduled line of Thursday",
                                         domain=[('week_day', '=', '5')])
    fri_timetable_ids = fields.One2many('timetable.schedule.line',
                                        'timetable_id',
                                        help="Scheduled line of Sunday",
                                        domain=[('week_day', '=', '1')])
    sat_timetable_ids = fields.One2many('timetable.schedule.line',
                                        'timetable_id',
                                        help="Scheduled line of Saturday",
                                        domain=[('week_day', '=', '0')])


    def _compute_name(self):
        """generate name for the timetable records"""
        for rec in self:
            rec.name = False
            if rec.batch_id and rec.academic_year_id:
                rec.name = "/".join([rec.batch_id.name, "Schedule"])

    @api.constrains('batch_id')
    def _check_batch(self):
        """ This method ensures that only one timetable can be scheduled for a
            specific Batch.

            :raises: ValidationError if more than one timetable is already
                    scheduled for the Batch."""
        batches = self.search_count([('batch_id', '=', self.batch_id.id)])
        if batches > 1:
            raise ValidationError(_('Timetable is already scheduled for '
                                    'this Batch'))

    def generate_latex_table(self, lines):
        """توليد جدول LaTeX لبيانات يوم معين"""
        latex = r"""
        \begin{table}[h]
            \centering
            \begin{tabular}{|c|c|c|c|c|}
                \hline
                \textbf{الفترة} & \textbf{من} & \textbf{إلى} & \textbf{المادة} & \textbf{الدكتور} \\
                \hline
        """
        for line in lines:
            time_from = self._format_float_time(line.time_from)
            time_till = self._format_float_time(line.time_till)
            latex += f"                {line.period_id.name or ''} & {time_from} & {time_till} & {line.course_id.name or ''} & {line.faculty_id.name or ''} \\\\\n"
            latex += "                \\hline\n"
        latex += r"""
            \end{tabular}
        \end{table}
        """
        return latex

    def _format_float_time(self, float_time):
        """تحويل الوقت العشري إلى تنسيق الساعة (مثل 08:30)"""
        if not float_time:
            return ''
        hours = int(float_time)
        minutes = int((float_time - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"