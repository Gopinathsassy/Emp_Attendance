import datetime as dt
import datetime
import re

from django.contrib.auth import authenticate
from django.db.models import Sum, Q
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import django
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect

from attendance_tools import models
# from datetime import datetime

from attendance_tools.models import timesheet


@login_required(login_url='login_page')
def user_base(request):
    user = request.user
    current_user = user.username
    current_date = datetime.datetime.now().date()
    total_user =models.timesheet.objects.filter(username=current_user, posting_date=current_date, status='draft').only('hours')
    mysumm = datetime.timedelta()
    for i in total_user:
        (h, m) = i.hours.split(':')
        d = datetime.timedelta(hours=int(h), minutes=int(m))
        mysumm += d
    print(str(mysumm))

    totsecc = mysumm.total_seconds()
    h = totsecc // 3600
    m = (totsecc % 3600) // 60
    # s = (totsec % 3600) % 60  # just for reference

    hoursss = "%d:%d" % (h, m)
    print(hoursss)

    # total_user = models.timesheet.objects.raw('SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(hours))) as hours,id from attendance_tools_timesheet WHERE today_date=DATE(NOW()) and username=%s',[request.user.username])
    total_leave = models.leave_apply.objects.raw('SELECT COUNT(leave_days) as leave_days,id FROM attendance_tools_leave_apply WHERE status="approved" and username=%s',[request.user.username])
    total_timesheet = models.timesheet.objects.raw('SELECT COUNT(Project_Name) as Project_Name,id FROM attendance_tools_timesheet WHERE status="approved" and username=%s',[request.user.username])
    request_timesheet = models.timesheet.objects.raw('SELECT COUNT(Project_Name) as Project_Name,id FROM attendance_tools_timesheet WHERE status="request" and username=%s',[request.user.username])
    announcement = models.announcement.objects.raw('SELECT * FROM attendance_tools_announcement WHERE today_date=DATE(NOW())')
    # recent = models.user_time_log.objects.raw('SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(user_total_hours ))) as user_total_hours,id from attendance_tools_user_time_log WHERE user_current_date=DATE(NOW()) and username=%s',[request.user.username])
    total_hours = models.user_time_log.objects.filter(username=current_user, user_current_date=current_date).only('user_total_hours')

    mysum = datetime.timedelta()
    for i in total_hours:
        (h, m, s) = i.user_total_hours.split(':')
        d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        mysum += d
    print(str(mysum))

    totsec = mysum.total_seconds()
    h = totsec // 3600
    m = (totsec % 3600) // 60
    s = (totsec % 3600) % 60  # just for reference

    hourss = "%d:%d:%d" %(h,m,s)
    print(hourss)
    context = {"total_leave":total_leave,"total_timesheet":total_timesheet,"request_timesheet":request_timesheet,"announcement":announcement,"total_hours":hourss, "total_user": hoursss}
    return render(request, 'user_templates/user_base.html',context)

@login_required(login_url='login_page')
def user_attendance(request,id):
    clockin = models.user_clock_in.objects.get(emp_id=id)
    recent_log = models.user_time_log.objects.raw('select * from attendance_tools_user_time_log where attendance_form="present" and username=%s ORDER BY id desc  LIMIT 5',[request.user.username])
    today_log = models.user_time_log.objects.raw('select * from attendance_tools_user_time_log where user_current_date=DATE(NOW()) and username=%s ',[request.user.username])
    get_username=models.user_clock_in.objects.raw('SELECT username,id from attendance_tools_user_clock_in ')
    compare=models.user_clock_in.objects.filter(username__in=[x.username for x in get_username],status=1)
    get_time = models.user_clock_in.objects.raw('SELECT * from attendance_tools_user_clock_in WHERE status=1 and username=%s', [request.user.username])
    recent = models.user_time_log.objects.raw('SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(user_total_hours ))) as user_total_hours,id from attendance_tools_user_time_log WHERE user_current_date=DATE(NOW()) and username=%s',[request.user.username])
    # timme = models.Image.objects.raw('SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(time_now ))) as time_now,id from attendance_tools_image WHERE user_current_date=DATE(NOW())')

    context = {'clockin': clockin, 'id': id, 'recent': recent,'get_time':get_time,'compare':compare,'recent_log':recent_log,'today_log':today_log}

    return render(request, "user_templates/user_attendance.html", context)

@login_required(login_url='login_page')
def clockin_update(request):
    if request.method == "POST":
        member = models.user_clock_in(id=request.POST['id'],emp_id=request.POST['emp_id'], username=request.POST['username'],
                        button_id=request.POST['button_id'], button_color=request.POST['button_color'], button_name=request.POST['button_name'],
                        curr_time=request.POST['current_time'], curr_date=request.POST['current_date'],
                        status=request.POST['status'], location=request.POST['location'])

        member.save()
        # return HttpResponse('id')
    return render(request, "user_templates/user_attendance.html")

@csrf_exempt
@login_required(login_url='login_page')
def clockout_update(request):
    if request.method == "POST":
        with django.db.transaction.atomic():

            emp_id = request.POST.get('emp_id')
            username = request.POST.get('username')
            button_id=request.POST.get('button_id')
            button_color = request.POST.get('button_color')
            button_name = request.POST.get('button_name')
            current_time = request.POST.get('current_time')
            current_date = request.POST.get('current_date')
            user_clockout_time = request.POST.get('user_clockout_time')
            user_clockin_time = request.POST.get('user_clockin_time')
            user_current_date = request.POST.get('user_current_date')
            attendance_form = request.POST.get('attendance_form')
            hourss = request.POST.get('total_hours')
            timm = request.POST.get('timm')
            total_hours = request.POST.get('tot_hours')
            calender_form = 'success'

            member1 = models.user_clock_in(id=request.POST['id'],emp_id=request.POST['emp_id'], username=request.POST['username'],
                            button_id=request.POST['button_id'], button_color=request.POST['button_color'], button_name=request.POST['button_name'],
                            curr_time=request.POST['current_time'], curr_date=request.POST['current_date'])


            s1 = user_clockin_time
            s2 = user_clockout_time
            FMT = '%H:%M:%S'
            total_hours1 = datetime.datetime.strptime(s2, FMT) - datetime.datetime.strptime(s1, FMT)
                # print(tdelta)
            # 
            member2= models.user_time_log(emp_id=request.POST['emp_id'], username=request.POST['username'],
                                         user_clockout_time=request.POST['user_clockout_time'],
                                         user_clockin_time=request.POST['user_clockin_time'],
                                         user_current_date=user_current_date,user_total_hours=total_hours,attendance_form=attendance_form,calender_form=calender_form)

            member1.save()
            member2.save()

            today = datetime.datetime.now().date()
            a = models.overall_work_hours.objects.filter(emp_id=emp_id,dates=today)

            # a.hours= total_hours

            if a:
                b = models.overall_work_hours.objects.get(emp_id=emp_id,dates=today)
                # timess= datetime.datetime.strftime(timm, FMT) + datetime.datetime.strftime(hourss, FMT)


                t1 = dt.datetime.strptime(timm, '%H:%M:%S')
                t2 = dt.datetime.strptime(hourss, '%H:%M:%S')
                time_zero = dt.datetime.strptime('00:00:00', '%H:%M:%S')
                print=(t1 - time_zero + t2).time()
                b.hours=print
                b.save()


            else:
                member3 = models.overall_work_hours(emp_id=request.POST['emp_id'], username=request.POST['username'],
                                                    dates=user_current_date, hours=total_hours,
                                                    location='office')
                member3.save()


            # member3 = models.overall_work_hours(emp_id=request.POST['emp_id'], username=request.POST['username'],
            #                                date=user_current_date, hours=total_hours,
            #                                location='office')


            # member3.save()

    return render(request, "user_templates/user_attendance.html")


@login_required(login_url='login_page')
def user_details(request):
    return render(request,"user_templates/profile/user_details.html")

@login_required(login_url='login_page')
def user_edit_details(request,id):
    admin_edit_user_profile = models.User.objects.get(emp_id=id)
    context = {'admin_edit_user_profile': admin_edit_user_profile,'id':id}
    return render(request, 'user_templates/crud/user_edit_details.html', context)



@login_required(login_url='login_page')
def leave_apply_table(request):
    # leave_apply_tablea = models.user_clock_in.objects.raw('SELECT * from attendance_tools_leave_apply where status=%s ',['request','rejected' ])
    leave_apply_table = models.leave_apply.objects.filter(username=request.user.username).exclude(status ='approved')
    return render(request, 'user_templates/user_leave/leave_apply_table.html',{'leave_apply_table':leave_apply_table})

@login_required(login_url='login_page')
def leave_apply(request):
    lead_name = models.assign_lead.objects.filter(username=request.user.username)
    return render(request, 'user_templates/user_leave/leave_apply.html',{'lead_name':lead_name})


@login_required(login_url='login_page')
def leave_apply_post(request):
    if request.method == "POST":
        leave = models.leave_apply(username=request.POST['username'],emp_id=request.POST['emp_id'],reason=request.POST['reason'],leave_days=request.POST['leave_days'],start_date=request.POST['start_date'],end_date=request.POST['end_date'],leave_apply_time=request.POST['current_time'],status=request.POST['status'],lead_name=request.POST['leadname'])
        leave.save()
    return render(request, 'user_templates/user_leave/leave_apply_table.html')

@login_required(login_url='login_page')
def change_password(request):
    return render(request, 'user_templates/profile/user_password_change.html')

@login_required(login_url='login_page')
def user_update_password(request):
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
def show_leave_status(request,id):
    show_leave_status = models.leave_apply.objects.get(id=id)
    return render(request, 'user_templates/user_leave/show_leave_status.html',{'show_leave_status':show_leave_status})

@login_required(login_url='login_page')
def delete_leave_request(request):
    if request.method == "POST":
        id = request.POST.get('id')
        department = models.leave_apply.objects.get(id=id)
        department.delete()
        return HttpResponse(id)

@login_required(login_url='login_page')
def edit_leave_request(request,id):
    edit_leave_request = models.leave_apply.objects.get(id=id)
    return render(request, 'user_templates/user_leave/edit_leave_request.html',{'edit_leave_request':edit_leave_request})

@login_required(login_url='login_page')
def resend_leave_apply(request):
    if request.method == "POST":
        member = models.leave_apply(id=request.POST['id'],emp_id=request.POST['emp_id'], username=request.POST['username'],
                        reason=request.POST['reason'], leave_days=request.POST['leave_days'], start_date=request.POST['start_date'],
                        end_date=request.POST['end_date'],
                         leave_apply_time=request.POST['current_time'], status=request.POST['status'])

        member.save()
        # return HttpResponse('id')
    return render(request, 'user_templates/user_leave/edit_leave_request.html')

@login_required(login_url='login_page')
def approved_leave_requests(request):
    approved_leave_requests = models.leave_apply.objects.filter(status='approved',username=request.user.username)
    return render(request, 'user_templates/user_leave/approved_leave_requests.html',{'approved_leave_requests':approved_leave_requests})



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
    count = models.timesheet.objects.filter(username=current_user,status='draft').count()
    # print(total_user)
    return render(request,'user_templates/timesheet/create_timesheet.html', {'project_code_name': project_code_name, 'count':count, 'total_hours': hourss,'lead_name':lead_name})

@login_required(login_url='login_page')
def timesheet_create(request):
    if request.method == 'POST':
        user = request.user.username
        emp_id = request.user.emp_id
        module=request.user.module
        # posting_date = datetime.datetime.now().date()

        project_name = request.POST.get('project_name')
        project_code = request.POST.get('project_code')
        # job_name = request.POST.get('job_name')
        task_name = request.POST.get('task_name')
        total_hours = request.POST.get('total_hours')
        date = request.POST.get('date')
        description = request.POST.get('description')
        status = "draft"
        leadname = request.POST.get('leadname')
        image = request.FILES.get('image')

       
        var1 = re.search("[0-9]{2}:[0-9]{2}",total_hours)
        if var1 == None:
            print("None")
            return HttpResponse("None")
        else:
            if total_hours == var1[0]:
                timesheet_user = models.timesheet.objects.create(username=user, emp_id=emp_id,module=module,
                                                                 project_name=project_name,project_code=project_code,
                                                                 task_name=task_name, hours=total_hours,
                                                                 today_date=date, description=description, image=image,
                                                                 status=status,leadname=leadname)
                timesheet_user.save()

    return HttpResponse("ok")


@login_required(login_url='login_page')
def timesheet_draft(request):
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
    return render(request, 'user_templates/timesheet/Submit_timesheet.html', {'all_timesheet': all_timesheet, 'total_hours': hourss})
    
    
    
    
    
    
    
    

@login_required(login_url='login_page')
def timesheet_sent_toadmin(request):
    if request.method == 'POST':

        id = request.POST.getlist('id[]')
        username = request.POST.getlist('username[]')
        project_name = request.POST.getlist('project_name[]')
        project_code = request.POST.getlist('task_name[]')
        hours = request.POST.getlist('hours[]')
        today_date = request.POST.getlist('today_date[]')
        description = request.POST.getlist('description[]')
        # status = request.POST.getlist('statuss[]')

        for x in range(len(request.POST.getlist('id[]'))):
            time_user = models.timesheet.objects.get(id=id[x])
            time_user.status=''
            time_user.work_status='request'
            time_user.save()
    return HttpResponse('Done')
    
    
    
        

@login_required(login_url='login_page')
def lead_timesheet_toadmins(request):
    if request.method == 'POST':

        id = request.POST.getlist('id[]')
        username = request.POST.getlist('username[]')
        project_name = request.POST.getlist('project_name[]')
        project_code = request.POST.getlist('project_code[]')
        task_name = request.POST.getlist('task_name[]')
        hours = request.POST.getlist('hours[]')
        today_date = request.POST.getlist('today_date[]')
        description = request.POST.getlist('description[]')
        # status = request.POST.getlist('statuss[]')

        for x in range(len(request.POST.getlist('id[]'))):
            time_user = models.timesheet.objects.get(id=id[x])
            time_user.status=''
            time_user.work_status='approved'
            time_user.save()
    return HttpResponse('Done')
    
    
    

@login_required(login_url='login_page')
def emp_timesheet_toadmins(request):
    if request.method == 'POST':

        id = request.POST.getlist('id[]')
       
        username = request.POST.getlist('username[]')
        project_name = request.POST.getlist('project_name[]')
        project_code = request.POST.getlist('project_code[]')
        module = request.POST.getlist('module[]')
        # task_name = request.POST.getlist('task_name[]')
        hours = request.POST.getlist('hours[]')
        posting_date = request.POST.getlist('posting_date[]')
        description = request.POST.getlist('description[]')
        # status = request.POST.getlist('statuss[]')

        for x in range(len(request.POST.getlist('id[]'))):
            time_user = models.timesheet.objects.get(id=id[x])
            time_user.status=''
            time_user.work_status='approved'
            time_user.save()
    return HttpResponse('Done')    
    
 
 
 

@login_required(login_url='login_page')
def emp_timesheet_leadtoadmin(request):
    if request.method == 'POST':

        id = request.POST.getlist('id[]')
        username = request.POST.getlist('username[]')
        project_name = request.POST.getlist('project_name[]')
        project_code = request.POST.getlist('project_code[]')
        # module = request.POST.getlist('module[]')
        task_name = request.POST.getlist('task_name[]')
        hours = request.POST.getlist('hours[]')
        today_date = request.POST.getlist('posting_date[]')
        description = request.POST.getlist('description[]')
        # status = request.POST.getlist('statuss[]')

        for x in range(len(request.POST.getlist('id[]'))):
            time_user = models.timesheet.objects.get(id=id[x])
            time_user.status=''
            time_user.work_status='approved'
            time_user.save()
    return HttpResponse('Done') 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
    
    
    
    
    

@login_required(login_url='login_page')
def timesheet_delete(request):
    id = request.POST.getlist('id[]')

    for x in range(len(request.POST.getlist('id[]'))):
        time_user = models.timesheet.objects.get(id=id[x])
        time_user.delete()
    return HttpResponse('Deleted')

@login_required(login_url='login_page')
def timesheet_edit_page(request,id):
    current_user = request.user.username
    project_code_name = models.assign_project.objects.filter(username_assign=current_user)
    current_date = datetime.datetime.now().date()

    edit_timesheet = models.timesheet.objects.get(id=id)
    count = models.timesheet.objects.filter(username=current_user, posting_date=current_date, status='draft').count()
    return render(request, 'user_templates/timesheet/edit_delete_timesheet.html', {'edit_timesheet': edit_timesheet, 'project_code_name':project_code_name, 'count':count})

@login_required(login_url='login_page')
def timesheet_edit_values(request, id):
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



# @login_required(login_url='login_page')
# def timesheet_edit_data_values(request, id):
#     if request.method == 'POST':

#         user = request.user.username
#         emp_id = request.user.emp_id
#         # posting_date = datetime.now().date()

#         id1 = request.POST.get('id')
#         project_name = request.POST.get('project_name')
#         project_code = request.POST.get('project_code')
#         job_name = request.POST.get('job_name')
#         task_name = request.POST.get('task_name')
#         total_hours = request.POST.get('total_hours')
#         date = request.POST.get('date')
#         description = request.POST.get('description')
#         status = "draft"
#         work_status = ""
#         image = request.FILES.get('image')



#         # timesheet_user = timesheet(id=id,user=user, emp_id=emp_id,
#         #                                                  project_name_code=project_name,
#         #                                                   job_name=job_name,
#         #                                                  task_name=task_name, hours=total_hours,
#         #                                                  date=date, description=description, image=image, status=status)
#         # timesheet_user.save()

#         timesheet_edit = timesheet.objects.get(id=id)
#         timesheet_edit.user = user
#         timesheet_edit.emp_id = emp_id
#         timesheet_edit.project_name = project_name
#         timesheet_edit.project_code = project_code
#         timesheet_edit.job_name = job_name
#         timesheet_edit.task_name = task_name
#         timesheet_edit.hours = total_hours
#         timesheet_edit.today_date = date
#         timesheet_edit.description = description
#         timesheet_edit.status = status
#         timesheet_edit.image = image

#         timesheet_edit.save()

#     return HttpResponse("ok")

@login_required(login_url='login_page')
def view_all_timesheet(request):

    current_user = request.user.username
    currrent_user_id = request.user.emp_id
    # print(currrent_user_id)
    all_timesheet = models.timesheet.objects.filter(username=current_user,emp_id=currrent_user_id)
    return render(request, 'user_templates/timesheet/view_all_timesheet.html', {'all_timesheet': all_timesheet})


@login_required(login_url='login_page')
def my_timesheets(request,id):
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        my_timesheets = models.timesheet.objects.raw('select * from  attendance_tools_timesheet where today_date between"'+fromdate+'"and"'+todate+'" and username=%s',[request.user.username])
        # my_timesheets = models.timesheet.objects.filter(username=id)
        return render(request, 'user_templates/timesheet/my_timesheets.html', {'my_timesheets': my_timesheets})
    else:
        my_timesheets = models.timesheet.objects.filter(username=id).order_by('today_date')
        return render(request, 'user_templates/timesheet/my_timesheets.html', {'my_timesheets': my_timesheets})

@login_required(login_url='login_page')
def view_my_timesheet(request,id):
    view_my_timesheet = models.timesheet.objects.get(id=id)
    return render(request, 'user_templates/timesheet/view_my_timesheet.html', {'view_my_timesheet': view_my_timesheet})

@login_required(login_url='login_page')
def my_timesheet_status(request):
    my_timesheet_status = models.timesheet.objects.filter(username=request.user.username,status='').exclude(work_status ='approved')
    return render(request, 'user_templates/timesheet/my_timesheet_status.html', {'my_timesheet_status': my_timesheet_status})

@login_required(login_url='login_page')
def show_mytimesheet_status(request,id):
    show_mytimesheet_status = models.timesheet.objects.get(id=id)
    return render(request, 'user_templates/timesheet/show_my_timesheet.html', {'show_mytimesheet_status': show_mytimesheet_status})

@login_required(login_url='login_page')
def edit_my_timesheet(request,id):
    current_user = request.user.username
    project_code_name = models.assign_project.objects.filter(username_assign=current_user)
    current_date = datetime.datetime.now().date()

    edit_timesheet = models.timesheet.objects.get(id=id)
    count = models.timesheet.objects.filter(username=current_user, posting_date=current_date, status='draft').count()
    return render(request, 'user_templates/timesheet/edit_timesheet_send.html', {'edit_timesheet': edit_timesheet, 'project_code_name':project_code_name, 'count':count})


@login_required(login_url='login_page')
def user_calender_view(request,id):
    # today = datetime.now().date()
    user_calender_view = models.user_time_log.objects.raw('select * from attendance_tools_user_time_log where emp_id= %s group by user_current_date',[id])

    # today_log = models.user_time_log.objects.filter(emp_id=id,user_current_date=today)
    # username = User.objects.filter(emp_id=id)

    return render(request,"user_templates/user_calender_view.html",{"user_calender_view":user_calender_view})








 

