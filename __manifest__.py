{
    'name': ' University Management System',
    'version': '18.0.1.0.0',
    'category': 'Education',
    'summary': """This modules helps to manage the university 
     management system""",
    'description': """This module serves as a comprehensive solution for
     efficiently managing the education system of a university enhancing
     its overall functionality and user experience.""",
    'author': 'Tiba Academy students',

    'maintainer': 'Tiba Academy students',

    'depends': ['mail', 'hr_recruitment', 'account'],
    'data': [
        'security/education_university_management_groups.xml',
        'security/ir.model.access.csv',
        'wizard/application_reject_views.xml',
        'views/education_university_management_menus.xml',
        'views/res_partner_views.xml',
        'views/timetable_period_views.xml',
        'views/university_exam_type_views.xml',
        'views/university_exam_views.xml',
        'views/exam_valuation_views.xml',
        'views/exam_result_views.xml',
        'views/university_timetable_views.xml',
        'views/timetable_schedule_line_views.xml',
        'views/university_application_views.xml',
        'views/university_attendace_views.xml',
        'views/university_attendance_line_views.xml',
        'views/university_student_views.xml',
        'views/university_document_type_views.xml',
        'views/university_document_views.xml',
        'views/reject_reason_views.xml',
        'views/university_course_views.xml',
        'views/university_department_views.xml',
        'views/university_semester_views.xml',
        'views/university_academic_year_views.xml',
        'views/university_batch_views.xml',
        'views/university_doctors_views.xml',
        'views/university_college_view.xml',
        'views/student_fee_views.xml',
        'views/course_registration_view.xml',
        'reports/university_batch_report.xml',
        'reports/report_university_timetable.xml',
        'reports/university_attendance_report.xml',
        'reports/exam_valuation_report.xml',
    ],


    'installable': True,
    'auto_install': False,
    'application': True,
}
