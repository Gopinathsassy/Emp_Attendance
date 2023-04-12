from datetime import datetime
import datetime
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import django
from django.db import transaction
from django.contrib.auth import authenticate
from attendance_tools import models
from attendance_tools.models import User




@login_required(login_url='login_page')
def lead_base(request):
    return render(request, 'lead/lead_base.html')


@login_required(login_url='login_page')
def lead_details(request):
    return render(request,'lead/lead_details.html')



@login_required(login_url='login_page')
def timesheet_open_page(request):
    lead_name = models.assign_lead.objects.filter(username=request.user.username)
    current_user = request.user.username
    project_code_name = models.assign_project.objects.filter(username_assign=current_user)
    # current_user = request.user.username
    # current_date = datetime.datetime.now().date()

    current_date = datetime.datetime.now().date()
    #
    # hours = models.timesheet.objects.filter(user=current_user, posting_date=current_date, status='draft').only('hours').aggregate(Sum('hours'))
    # print(hours)
    
    total_hours = models.timesheet.objects.filter(username=current_user, posting_date=current_date, status='draft').only('hours')

    mysum = datetime.timedelta()
    for i in total_hours:
        (h, m) = i.hours.split(':')
        d = datetime.timedelta(hours=int(h), minutes=int(m))
        mysum += d
    print(str(mysum))

    totsec = mysum.total_seconds()
    h = totsec // 3600
    m = (totsec % 3600) // 60
    # s = (totsec % 3600) % 60  # just for reference

    hourss = "%d:%d" % (h, m)
    print(hourss)

    # total_user = models.timesheet.objects.filter(username=current_user, posting_date=current_date, status='draft').raw('SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(hours))) as hours,id from attendance_tools_timesheet WHERE today_date=DATE(NOW()) and emp_id=%s',[request.user.emp_id])
    count = models.timesheet.objects.filter(username=current_user, status='draft').count()
    print(total_user)
    return render(request,'user_templates/timesheet/create_timesheet.html', {'project_code_name': project_code_name, 'count':count, 'total_hours': hourss,'lead_name':lead_name})


@login_required(login_url='login_page')
def emp_user_leave_requests(request):
    emp_leave_request = models.leave_apply.objects.filter(status='request',lead_name=request.user.emp_id)
    return render(request, 'lead/leave/emp_user_leave_requests.html',{'emp_leave_request':emp_leave_request})

@login_required(login_url='login_page')
def lead_view_leave_request(request,id):
    view_leave_data_details = models.leave_apply.objects.get(id=id)

    return render(request, "lead/leave/lead_view_leave_request.html",{'view_leave_data_details':view_leave_data_details})


@login_required(login_url='login_page')
def lead_create_timesheet(request):
    if request.method == 'POST':
        user = request.user.username
        emp_id = request.user.emp_id
        
        # posting_date = datetime.datetime.now().date()

        project_name = request.POST.get('project_name')
        project_code = request.POST.get('project_code')
        job_name = request.POST.get('job_name')
        task_name = request.POST.get('task_name')
        total_hours = request.POST.get('total_hours')
        date = request.POST.get('date')
        description = request.POST.get('description')
        status = "draft"
        image = request.FILES.get('image')

        var1 = re.search("[0-9]{2}:[0-9]{2}", total_hours)
        if var1 == None:
            print("None")
            return HttpResponse("None")
        else:
            if total_hours == var1[0]:
                timesheet_user = models.timesheet.objects.create(username=user, emp_id=emp_id,
                                                                 project_name=project_name, project_code=project_code,
                                                                 job_name=job_name,
                                                                 task_name=task_name, hours=total_hours,
                                                                 today_date=date, description=description, image=image,
                                                                 status=status)
                timesheet_user.save()

    return HttpResponse("done")

@login_required(login_url='login_page')
def lead_leave_apply(request):
    return render(request, 'lead/leave/lead_leave_apply.html')

@login_required(login_url='login_page')
def lead_leave_apply_table(request):
    # leave_apply_tablea = models.user_clock_in.objects.raw('SELECT * from attendance_tools_leave_apply where status=%s ',['request','rejected' ])
    leave_apply_table = models.leave_apply.objects.filter(username=request.user.username).exclude(status ='approved')
    return render(request, 'lead/leave/lead_leave_apply_table.html',{'leave_apply_table':leave_apply_table})

@login_required(login_url='login_page')
def lead_timesheet_draft(request):
    user = request.user
    current_user = user.username
    current_date = datetime.datetime.now().date()
    
    total_hours = models.timesheet.objects.filter(username=current_user, posting_date=current_date, status='draft').only('hours')

    mysum = datetime.timedelta()
    for i in total_hours:
        (h, m) = i.hours.split(':')
        d = datetime.timedelta(hours=int(h), minutes=int(m))
        mysum += d
    print(str(mysum))

    totsec = mysum.total_seconds()
    h = totsec // 3600
    m = (totsec % 3600) // 60
    # s = (totsec % 3600) % 60  # just for reference

    hourss = "%d:%d" % (h, m)
    print(hourss)
    # total_user = models.timesheet.objects.raw('SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(hours))) as hours,id from attendance_tools_timesheet WHERE today_date=DATE(NOW()) and emp_id=%s',[request.user.emp_id])
    all_timesheet = models.timesheet.objects.filter(username=current_user,status='draft',work_status='')
    return render(request, 'lead/timesheet/lead_timesheet_draft.html', {'all_timesheet': all_timesheet, 'total_hours': hourss})


@login_required(login_url='login_page')
def lead_create_timesheet(request):
    # current_user = request.user.username
    # project_code_name = models.assign_project.objects.filter(username_assign=current_user)
    # current_date = datetime.datetime.now().date()
    # total_user = models.timesheet.objects.filter(username=current_user, posting_date=current_date, status='draft').raw('SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(hours))) as hours,id from attendance_tools_timesheet WHERE today_date=DATE(NOW()) and emp_id=%s',[request.user.emp_id])
    # count = models.timesheet.objects.filter(username=current_user, posting_date=current_date, status='draft').count()
    # print(total_user)
    
    lead_name = models.assign_lead.objects.filter(username=request.user.username)
    current_user = request.user.username
    project_code_name = models.assign_project.objects.filter(username_assign=current_user)
    # current_user = request.user.username
    # current_date = datetime.datetime.now().date()

    current_date = datetime.datetime.now().date()
    #
    # hours = models.timesheet.objects.filter(user=current_user, posting_date=current_date, status='draft').only('hours').aggregate(Sum('hours'))
    # print(hours)
    #
    
    total_hours = models.timesheet.objects.filter(username=current_user, posting_date=current_date, status='draft').only('hours')

    mysum = datetime.timedelta()
    for i in total_hours:
        (h, m) = i.hours.split(':')
        d = datetime.timedelta(hours=int(h), minutes=int(m))
        mysum += d
    print(str(mysum))

    totsec = mysum.total_seconds()
    h = totsec // 3600
    m = (totsec % 3600) // 60
    # s = (totsec % 3600) % 60  # just for reference

    hourss = "%d:%d" % (h, m)
    print(hourss)

    # total_user = models.timesheet.objects.filter(username=current_user, posting_date=current_date, status='draft').raw('SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(hours))) as hours,id from attendance_tools_timesheet WHERE today_date=DATE(NOW()) and emp_id=%s',[request.user.emp_id])
    count = models.timesheet.objects.filter(username=current_user, status='draft').count()
    # print(total_user)
    return render(request,'lead/timesheet/lead_create_timesheet.html', {'project_code_name': project_code_name, 'count':count, 'total_hours': hourss,'lead_name':lead_name})

    # return render(request,'lead/timesheet/lead_create_timesheet.html', {'project_code_name': project_code_name, 'count':count, 'total_user': total_user})


@login_required(login_url='login_page')
def lead_my_timesheet(request,id):
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        my_timesheets = models.timesheet.objects.raw('select * from  attendance_tools_timesheet where posting_date between"'+fromdate+'"and"'+todate+'" and username=%s',[request.user.username])

        # my_timesheets = models.timesheet.objects.filter(username=id)
        return render(request, 'user_templates/timesheet/my_timesheets.html', {'my_timesheets': my_timesheets})
    else:
        my_timesheets = models.timesheet.objects.filter(username=id)
        return render(request, 'lead/timesheet/lead_my_timesheet.html', {'my_timesheets': my_timesheets})



@login_required(login_url='login_page')
def lead_my_timesheet_status(request):
    my_timesheet_status = models.timesheet.objects.filter(username=request.user.username,status='').exclude(work_status ='approved')
    return render(request, 'lead/timesheet/lead_my_timesheet_status.html', {'my_timesheet_status': my_timesheet_status})



@login_required(login_url='login_page')
def lead_timesheet_edit_page(request,id):
    current_user = request.user.username
    project_code_name = models.assign_project.objects.filter(username_assign=current_user)
    current_date = datetime.datetime.now().date()

    edit_timesheet = models.timesheet.objects.get(id=id)
    count = models.timesheet.objects.filter(username=current_user, posting_date=current_date, status='draft').count()
    return render(request, 'lead/timesheet/lead_timesheet_edit_page.html', {'edit_timesheet': edit_timesheet, 'project_code_name':project_code_name, 'count':count})
    
@login_required(login_url='login_page')
def lead_timesheet_edit_values(request, id):
    if request.method == 'POST':

        user = request.user.username
        emp_id = request.user.emp_id
        # posting_date = datetime.now().date()

        id1 = request.POST.get('id')
        project_name = request.POST.get('project_name')
        project_code = request.POST.get('project_code')
        # job_name = request.POST.get('job_name')
        task_name = request.POST.get('task_name')
        total_hours = request.POST.get('total_hours')
        date = request.POST.get('date')
        description = request.POST.get('description')
        status = "draft"
        image = request.FILES.get('image')
        
        var1 = re.search("[0-9]{2}:[0-9]{2}",total_hours)
        if var1 == None:
            print("None")
            return HttpResponse("None")
        else:
            if total_hours == var1[0]:
        
       
       
        # timesheet_user = timesheet(id=id,user=user, emp_id=emp_id,
        #                                                  project_name_code=project_name,
        #                                                   job_name=job_name,
        #                                                  task_name=task_name, hours=total_hours,
        #                                                  date=date, description=description, image=image, status=status)
        # timesheet_user.save()

                timesheet_edit = timesheet.objects.get(id=id)
                timesheet_edit.username = user
                timesheet_edit.emp_id = emp_id
                timesheet_edit.project_name = project_name
                timesheet_edit.project_code = project_code
                # timesheet_edit.job_name = job_name
                timesheet_edit.task_name = task_name
                timesheet_edit.hours = total_hours
                timesheet_edit.today_date = date
                timesheet_edit.description = description
                timesheet_edit.status = status
                timesheet_edit.image = image
        
                timesheet_edit.save()

    return HttpResponse("ok")


@login_required(login_url='login_page')
def lead_view_my_timesheet(request,id):
    lead_view_my_timesheet = models.timesheet.objects.get(id=id)
    return render(request, 'lead/timesheet/lead_view_my_timesheet.html',{'lead_view_my_timesheet':lead_view_my_timesheet})

@login_required(login_url='login_page')
def lead_show_mytimesheet_status(request,id):
    lead_view = models.timesheet.objects.get(id=id,status='')
    return render(request, 'lead/timesheet/lead_show_mytimesheet_status.html',{'lead_view':lead_view})


@login_required(login_url='login_page')
def emp_time_sheet_request(request):
    # emp_time_request = models.timesheet.objects.all()
    emp_time_request = models.timesheet.objects.filter(leadname=request.user.emp_id,work_status='request')
    return render(request, 'lead/emp_time_sheet_request.html',{'emp_time_request':emp_time_request})





@login_required(login_url='login_page')
def lead_attendance(request, id):
        clockin = models.user_clock_in.objects.get(emp_id=id)
        get_username = models.user_clock_in.objects.raw('SELECT username,id from attendance_tools_user_clock_in ')
        compare = models.user_clock_in.objects.filter(username__in=[x.username for x in get_username], status=1)
        get_time = models.user_clock_in.objects.raw(
            'SELECT * from attendance_tools_user_clock_in WHERE status=1 and username=%s', [request.user.username])
        recent = models.user_time_log.objects.raw(
            'SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(user_total_hours ))) as user_total_hours,id from attendance_tools_user_time_log WHERE user_current_date=DATE(NOW()) and username=%s',
            [request.user.username])
        # timme = models.Image.objects.raw('SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(time_now ))) as time_now,id from attendance_tools_image WHERE user_current_date=DATE(NOW())')

        context = {'clockin': clockin, 'id': id, 'recent': recent, 'get_time': get_time, 'compare': compare}

        return render(request, "lead/lead_attendance.html", context)

    # return render(request, 'user_templates/timesheet/edit_timesheet_send.html',{'edit_my_timesheet':edit_my_timesheet})





@login_required(login_url='login_page')
def lead_timesheet_view(request,id):
    timesheet_view = models.timesheet.objects.get(id=id)
    context = {'timesheet_view': timesheet_view, 'id': id}
    return render(request, 'lead/lead_timesheet_view_user.html',context)

@login_required(login_url='login_page')
def employee_timesheet_approval(request):
    if request.method == 'POST':
        timesheet_approval = models.timesheet(id=request.POST['id'],emp_id=request.POST['emp_id'],username=request.POST['username'],project_name=request.POST['project_name'],project_code=request.POST['project_code'], 
                                task_name=request.POST['task_name'],
                                hours=request.POST['hours'], posting_date=request.POST['posting_date'],image=request.POST['image'], description=request.POST['description'],
                                work_status=request.POST['work_status'],today_date=request.POST['today_date'],leadname=request.POST['lead_name'])
        timesheet_approval.save()
    return render(request, 'lead/emp_time_sheet_request.html')



@login_required(login_url='login_page')
def employee_timesheet_reject(request):
    if request.method == 'POST':
        leave_request_approval = models.timesheet(id=request.POST['id'],emp_id=request.POST['emp_id'],username=request.POST['username'],project_name=request.POST['project_name'],project_code=request.POST['project_code'],
                                task_name=request.POST['task_name'],
                                hours=request.POST['hours'], posting_date=request.POST['posting_date'],image=request.POST['image'], description=request.POST['description'],
                                work_status=request.POST['work_status'],today_date=request.POST['today_date'],rejected_reason=request.POST['timesheet_rejected_reason'],leadname=request.POST['lead_name'])
        leave_request_approval.save()
    return render(request, 'lead/emp_time_sheet_request.html')
    
    
    
@login_required(login_url='login_page')
def employee_leave_request_approval(request):
    if request.method == 'POST':
        leave_dates = request.POST.getlist('leave_dates[]')
        emp_id = request.POST.get('emp_id')
        username = request.POST.get('username')
        clockin_time = ''
        clockout_time = ''
        time = ''
        attendance_form = 'absent'

        with django.db.transaction.atomic():
            for x in range(len(request.POST.getlist('leave_dates[]'))):
                leave_post = models.user_time_log.objects.create(username=username,emp_id=emp_id,user_clockin_time=clockin_time,user_clockout_time=clockout_time,
                                           user_current_date=leave_dates[x],user_total_hours=time,attendance_form=attendance_form)




                leave_request_approval = models.leave_apply(id=request.POST['id'], emp_id=request.POST['emp_id'],
                                                            username=request.POST['username'], reason=request.POST['reason'],
                                                            leave_days=request.POST['leave_days'],
                                                            start_date=request.POST['start_date'],
                                                            end_date=request.POST['end_date'],
                                                            leave_apply_time=request.POST['applied_time'],
                                                            status=request.POST['status'],lead_name=request.POST['leadname'])

        leave_post.save()
        leave_request_approval.save()
    return render(request, 'lead/leave/emp_user_leave_requests.html')


@login_required(login_url='login_page')
def employee_leave_request_rejected(request):
    if request.method == 'POST':
        leave_request_rejected = models.leave_apply(id=request.POST['id'],emp_id=request.POST['emp_id'],username=request.POST['username'], reason=request.POST['reason'],
                                leave_days=request.POST['leave_days'],
                                start_date=request.POST['start_date'], end_date=request.POST['end_date'],
                                leave_apply_time=request.POST['applied_time'],status=request.POST['status'],rejected_reason=request.POST['rejected_reason'],lead_name=request.POST['leadname'])
        leave_request_rejected.save()
        return render(request, 'lead/leave/emp_user_leave_requests.html')


@login_required(login_url='login_page')
def lead_edit_details(request,id):
    admin_edit_user_profile = models.User.objects.get(emp_id=id)
    context = {'admin_edit_user_profile': admin_edit_user_profile,'id':id}
    return render(request, 'lead/lead_edit_details.html', context)
    
    
    
@login_required(login_url='login_page')
def lead_update_details(request,id):
    if request.method == 'POST':
        id1 = request.POST.get('id')
        emp_id = request.POST.get('emp_id')
        user_name = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        module = request.POST.get('module')
        official_email_id = request.POST.get('official_email_id')
        personal_email_id = request.POST.get('personal_email_id')
        adhar_no = request.POST.get('adhar_no')
        mobile_no = request.POST.get('mobile_no')
        password = request.POST.get('password')
        # date_of_join = request.POST.get('date_of_join')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        job_role = request.POST.get('job_role')
        blood_group = request.POST.get('blood_group')
        acc_no = request.POST.get('acc_no')
        ifsc_code = request.POST.get('ifsc_code')
        branch = request.POST.get('branch')
        image1 = request.FILES.get('profile_avatar')



        # post_user_update = models.User(id=request.POST['id'],password=request.POST['password'],emp_id=request.POST['emp_id'], first_name=request.POST['first_name'],
        #                         last_name=request.POST['last_name'],username=request.POST['username'],
        #                         dob=request.POST['dob'],module=request.POST['module'],blood_group=request.POST['blood_group'], official_email_id=request.POST['official_email_id'], personal_email_id=request.POST['personal_email_id'],
        #                         adhar_no=request.POST['adhar_no'], mobile_no=request.POST['mobile_no'],
        #                         job_role=request.POST['job_role'], address=request.POST['address'],
        #                         acc_no = request.POST['acc_no'],ifsc_code=request.POST['ifsc_code'],branch=request.POST['branch'])
        #
        # post_user_update.save()


        user = User.objects.get(id=id)
        user.id = id1
        user.emp_id = emp_id
        user.user_name = user_name
        user.first_name = first_name
        user.last_name = last_name
        user.dob = dob
        user.module = module
        user.official_email_id = official_email_id
        user.personal_email_id = personal_email_id
        user.adhar_no = adhar_no

        user.mobile_no = mobile_no
        user.password = password
        # user.date_of_join = date_of_join
        user.address = address
        user.gender = gender

        user.job_role = job_role
        user.blood_group = blood_group
        user.acc_no = acc_no
        user.ifsc_code = ifsc_code
        user.branch = branch
        if image1 != None:
            user.user_image = image1
        # print(str(image))
        user.save()
    return HttpResponse("ok")
    # return render(request, 'admin_templates/crud/admin_edit_user_profile.html')


@login_required(login_url='login_page')
def lead_change_password(request):
    return render(request, 'lead/lead_change_password.html')


@login_required(login_url='login_page')
def lead_update_password(request):
    # Change Password for admin panel
    uname = request.user.username
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user_password = request.POST.get('user_password')

        user = authenticate(username=uname, password=old_password)
        if user is not None:
            if new_password == confirm_password and new_password != '':
                u = models.User.objects.get(username=uname)
                u.user_password = user_password
                u.set_password(new_password)
                u.save()
                message = 'Successfully Changed the Password.'
                return HttpResponse("Updated")

            else:
                return HttpResponse("new_and_confirm_not_ok")

        else:
            return HttpResponse("error_old_password")




@login_required(login_url='login_page')
def lead_calender_view(request,id):
    # today = datetime.now().date()
    lead_calender_view = models.user_time_log.objects.raw('select * from attendance_tools_user_time_log where emp_id= %s group by user_current_date',[id])

    # today_log = models.user_time_log.objects.filter(emp_id=id,user_current_date=today)
    # username = User.objects.filter(emp_id=id)

    return render(request,"lead/lead_calender_view.html",{"lead_calender_view":lead_calender_view})