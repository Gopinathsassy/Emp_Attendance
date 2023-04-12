"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import attendance_tools.views
from admin import views
import lead.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_page, name='login_page'),
    path('admin_base/', views.admin_base, name='admin_base'),
    path('logout/', views.logout_page, name='logout'),
    path('index_page', views.index_page, name='index_page'),
    path('total_users/', views.total_users, name='total_users'),
    path('user_operations', views.user_operations, name='user_operations'),
    path('user_profile_page/<id>', views.user_profile_page, name='user_profile_page'),
    path('admin_edit_details/<id>',views.admin_edit_details, name='admin_edit_details'),
    path('admin_delete_user',views.admin_delete_user, name="admin_delete_user"),
    path('user_edit_details/admin_user_update_details/<id>', views.admin_user_update_details, name='admin_user_update_details'),
    path('user_leave_requests', views.user_leave_requests, name='user_leave_requests'),
    path('view_leave_request_details/<id>',views.view_leave_request_details, name='view_leave_request_details'),
    path('leave_request_approval', views.leave_request_approval, name='leave_request_approval'),
    path('leave_request_rejected', views.leave_request_rejected, name='leave_request_rejected'),
    path('total_employees', views.total_employees, name='total_employees'),
    path('view_attendance_details/<id>', views.view_attendance_details, name='view_attendance_details'),
    path('employee_attendance', views.employee_attendance, name='employee_attendance'),
    path('create_project', views.create_project, name='create_project'),
    path('project_assigning', views.project_assigning, name='project_assigning'),
    path('view_time_log/<id>', views.view_time_log, name='view_time_log'),
    path('assign_project/', views.assign_project, name='assign_project'),
    path('total_timesheet_users/', views.total_timesheet_users, name='total_timesheet_users'),
    path('total_timesheet/', views.total_timesheet, name='total_timesheet'),
    path('time_sheet_request/', views.time_sheet_request, name='time_sheet_request'),
    path('user_leave_approvals/', views.user_leave_approvals, name='user_leave_approvals'),
    path('view_leave_approvals/<id>', views.view_leave_approvals, name='view_leave_approvals'),
    path('user_timesheet_approvals/', views.user_timesheet_approvals, name='user_timesheet_approvals'),
    path('total_users_leave/', views.total_users_leave, name='total_users_leave'),
    path('view_user_leave_datas/<id>', views.view_user_leave_datas, name='view_user_leave_datas'),
    path('view_leave_data_details/<id>', views.view_leave_data_details, name='view_leave_data_details'),
    path('total_user_attendance/<id>', views.total_user_attendance, name='total_user_attendance'),
    path('user_location_requsts', views.user_location_requsts, name='user_location_requsts'),
    path('project_type_post', views.project_type_post, name='project_type_post'),
    path('assign_poject_post', views.assign_poject_post, name='assign_poject_post'),
    path('assign_poject_val', views.assign_poject_val, name='assign_poject_val'),
    path('view_user_timesheets/<id>',views.view_user_timesheets, name='view_user_timesheets'),
    path('announcement/',views.announcement, name='announcement'),
    path('admin_announcement/',views.admin_announcement, name='admin_announcement'),
    path('emp_log/',views.emp_log, name='emp_log'),


    path('admin_user_update_data', views.admin_user_update_data, name='admin_user_update_data'),




    # timesheet
    path('timesheet_view/<id>', views.timesheet_view, name='timesheet_view'),
    path('timesheet_approval', views.timesheet_approval, name='timesheet_approval'),
    path('timesheet_reject', views.timesheet_reject, name='timesheet_reject'),
    path('my_timesheets/<id>', attendance_tools.views.my_timesheets, name='my_timesheets'),
    path('edit_my_timesheet/<id>', attendance_tools.views.edit_my_timesheet, name='edit_my_timesheet'),
    path('my_timesheet_status', attendance_tools.views.my_timesheet_status, name='my_timesheet_status'),
    # path('show_timesheet_status/<id>', attendance_tools.views.show_timesheet_status, name='show_timesheet_status'),
    # path('edit_timesheet_send/', attendance_tools.views.edit_timesheet_send, name='edit_timesheet_send'),

    path('assign_lead', views.assign_lead, name='assign_lead'),
    path('assign_lead_post', views.assign_lead_post, name='assign_lead_post'),
    path('lead_list', views.lead_list, name='lead_list'),


    path('view_location_request_details/<id>', views.view_location_request_details, name='view_location_request_details'),
    path('user_location_approval', views.user_location_approval, name='user_location_approval'),
    path('user_location_rejected', views.user_location_rejected, name='user_location_rejected'),
    # path('project_list', views.project_list, name='project_list'),


    path('show_mytimesheet_status/<id>', attendance_tools.views.show_mytimesheet_status, name='show_mytimesheet_status'),
    path('view_my_timesheet/<id>', attendance_tools.views.view_my_timesheet, name='view_my_timesheet'),

    path('project_list', views.project_list, name='project_list'),
    path('edit_project_details/<id>', views.edit_project_details, name='edit_project_details'),
    path('edit_lead/<id>', views.edit_lead, name='edit_lead'),
     path('save_lead_edit', views.save_lead_edit, name='save_lead_edit'),
         path('delete_lead', views.delete_lead, name='delete_lead'),
    path('delete_project', views.delete_project, name='delete_project'),
    path('save_project_edit', views.save_project_edit, name='save_project_edit'),


    #     registration urls
    path('registration', views.registration, name='registration'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('admin_edit_user_profile/<id>', views.admin_edit_user_profile, name='admin_edit_user_profile'),




#     user side urls
    path('user_base/', attendance_tools.views.user_base, name='user_base'),
    # path('user_attendance/', attendance_tools.views.user_attendance, name="user_attendance"),
    path('user_attendance/<id>', attendance_tools.views.user_attendance, name="user_attendance"),
    path('clockin_update', attendance_tools.views.clockin_update, name="clockin_update"),
    path('clockout_update', attendance_tools.views.clockout_update, name="clockout_update"),
    path('user_details', attendance_tools.views.user_details, name="user_details"),
    path('user_edit_details/<id>', attendance_tools.views.user_edit_details, name='user_edit_details'),
    path('leave_apply_table', attendance_tools.views.leave_apply_table, name='leave_apply_table'),
    path('leave_apply', attendance_tools.views.leave_apply, name='leave_apply'),
    path('leave_apply_post', attendance_tools.views.leave_apply_post, name="leave_apply_post"),
    path('change_password', attendance_tools.views.change_password, name="change_password"),
    path('user_update_password', attendance_tools.views.user_update_password, name="user_update_password"),
    path('show_leave_status/<id>', attendance_tools.views.show_leave_status, name="show_leave_status"),
    path('delete_leave_request', attendance_tools.views.delete_leave_request, name="delete_leave_request"),
    path('edit_leave_request/<id>', attendance_tools.views.edit_leave_request, name="edit_leave_request"),
    path('resend_leave_apply', attendance_tools.views.resend_leave_apply, name="resend_leave_apply"),
    path('approved_leave_requests', attendance_tools.views.approved_leave_requests, name="approved_leave_requests"),

    path('timesheet_open_page', attendance_tools.views.timesheet_open_page, name='timesheet_open_page'),
    path('timesheet_create', attendance_tools.views.timesheet_create, name='timesheet_create'),
    path('timesheet_draft', attendance_tools.views.timesheet_draft, name='timesheet_draft'),
    path('timesheet_sent_toadmin',attendance_tools.views.timesheet_sent_toadmin, name='timesheet_sent_toadmin'),
    
    
    
    path('total_timesheet/lead_timesheet_toadmins',attendance_tools.views.lead_timesheet_toadmins, name='lead_timesheet_toadmins'),
    path('time_sheet_request/emp_timesheet_toadmins',attendance_tools.views.emp_timesheet_toadmins, name='emp_timesheet_toadmins'),
    path('emp_timesheet_leadtoadmin',attendance_tools.views.emp_timesheet_leadtoadmin, name='emp_timesheet_leadtoadmin'),
    
    
    
    
    
    path('timesheet_delete', attendance_tools.views.timesheet_delete, name='timesheet_delete'),
    path('timesheet_edit_page/<id>', attendance_tools.views.timesheet_edit_page, name='timesheet_edit_page.id'),
    path('timesheet_edit_page/timesheet_edit_values/<id>', attendance_tools.views.timesheet_edit_values, name='timesheet_edit_values.id'),
    # path('edit_my_timesheet/timesheet_edit_data_values/<id>', attendance_tools.views.timesheet_edit_data_values, name='timesheet_edit_data_values.id'),
    path('view_all_timesheet', attendance_tools.views.view_all_timesheet, name='view_all_timesheet'),
    path('user_calender_view/<id>',attendance_tools.views.user_calender_view, name='user_calender_view'),
    
    
    
    # lead
    path('lead_base', lead.views.lead_base, name='lead_base'),
    path('lead_details', lead.views.lead_details, name='lead_details'),
    path('emp_time_sheet_request', lead.views.emp_time_sheet_request, name='emp_time_sheet_request'),
    
    path('lead_attendance/<id>', lead.views.lead_attendance, name="lead_attendance"),

    path('emp_user_leave_requests',lead.views.emp_user_leave_requests, name='emp_user_leave_requests'),
    path('lead_view_leave_request/<id>', lead.views.lead_view_leave_request, name='lead_view_leave_request'),
    path('lead_leave_apply', lead.views.lead_leave_apply, name='lead_leave_apply'),
    path('lead_leave_apply_table', lead.views.lead_leave_apply_table, name='lead_leave_apply_table'),


    path('lead_create_timesheet', lead.views.lead_create_timesheet, name='lead_create_timesheet'),
    path('lead_my_timesheet/<id>', lead.views.lead_my_timesheet, name='lead_my_timesheet'),
    path('lead_timesheet_draft', lead.views.lead_timesheet_draft, name='lead_timesheet_draft'),
    path('lead_my_timesheet_status', lead.views.lead_my_timesheet_status, name='lead_my_timesheet_status'),
    path('lead_view_my_timesheet/<id>', lead.views.lead_view_my_timesheet, name='lead_view_my_timesheet'),

    path('lead_timesheet_edit_page/<id>', lead.views.lead_timesheet_edit_page, name='lead_timesheet_edit_page'),
    path('lead_timesheet_edit_page/lead_timesheet_edit_values/<id>', lead.views.lead_timesheet_edit_values, name='lead_timesheet_edit_values.id'),
    path('lead_show_mytimesheet_status/<id>', lead.views.lead_show_mytimesheet_status,name='lead_show_mytimesheet_status'),

    path('lead_timesheet_view/<id>', lead.views.lead_timesheet_view,name='lead_timesheet_view'),

    path('employee_timesheet_approval',lead.views.employee_timesheet_approval, name='employee_timesheet_approval'),
    path('employee_timesheet_reject', lead.views.employee_timesheet_reject, name='employee_timesheet_reject'),


    path('employee_leave_request_approval', lead.views.employee_leave_request_approval, name='employee_leave_request_approval'),
    path('employee_leave_request_rejected', lead.views.employee_leave_request_rejected, name='employee_leave_request_rejected'),
    
    path('lead_edit_details/<id>', lead.views.lead_edit_details, name='lead_edit_details'),
    path('lead_edit_details/lead_update_details/<id>',lead.views.lead_update_details, name='lead_update_details'),
    
    path('lead_change_password', lead.views.lead_change_password, name="lead_change_password"),
    path('lead_update_password', lead.views.lead_update_password, name="lead_update_password"),
    path('lead_calender_view/<id>', lead.views.lead_calender_view, name="lead_calender_view"),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
