from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import django
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from attendance_tools import models
from attendance_tools.models import User


@login_required(login_url='login_page')
def admin_base(request):
    today=datetime.now().date()
    leave_count = models.leave_apply.objects.filter(status="request").count()
    emp_id = request.POST.get('emp_id')
    leave_request_count = models.leave_apply.objects.filter(status="request").count()
    leave_approved_count = models.leave_apply.objects.filter(status="approved").count()
    attendance_count= models.user_clock_in.objects.filter(curr_date=today).count()
    timesheet_notification=models.timesheet.objects.filter(work_status='request')
    timesheet_request_count = models.timesheet.objects.raw("select count(distinct username)as count,id from attendance_tools_timesheet where today_date=DATE(NOW())")
    return render(request, 'admin_templates/admin_base.html',
                  {"leave_request_count": leave_request_count, "leave_approved_count": leave_approved_count,
                   "attendance_count": attendance_count, "timesheet_request_count": timesheet_request_count,"leave_count":leave_count,'timesheet_notification':timesheet_notification})





@csrf_exempt
def login_page(request):
    if request.method == 'POST': #if someone fills out form , Post it
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:# if user exist
            login(request, user)
            messages.success(request,(f'hii {username} You are now logined'))
            return redirect('admin_base')
        elif user is not None and user.is_lead:
            login(request, user)
            return redirect('lead_base')
        elif user is not None:
            login(request, user)
            return redirect('user_base')
        else:
            messages.success(request,('Error logging in'))

            return redirect('login_page') #re routes to login page upon unsucessful login
    else:
        return render(request, 'login_page.html', {})

@login_required(login_url='login_page')
def logout_page(request):
    logout(request)
    return redirect('login_page')
    
    
@login_required(login_url='login_page')
def index_page(request):
    return render(request, 'index_page.html')

@login_required(login_url='login_page')
def registration(request):
    return render(request, 'admin_templates/crud/user_registration.html')


@login_required(login_url='login_page')
def user_registration(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        is_lead = request.POST.get('is_lead')
        is_admin = request.POST.get('is_admin')
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
        date_of_join = request.POST.get('date_of_join')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        job_role = request.POST.get('job_role')
        blood_group = request.POST.get('blood_group')
        acc_no = request.POST.get('acc_no')
        ifsc_code = request.POST.get('ifsc_code')
        branch = request.POST.get('branch')
        user_password = request.POST.get('user_password')

        # position = ""
        with django.db.transaction.atomic():
                post_user_create = User.objects.create_user(emp_id=emp_id,username=user_name,is_lead=is_lead,is_superuser=is_admin,
                                                     first_name=first_name, last_name=last_name,dob=dob,blood_group=blood_group,
                                                     official_email_id=official_email_id,personal_email_id=personal_email_id,module=module,
                                                     adhar_no=adhar_no,mobile_no=mobile_no,password=password,
                                                     address=address,gender=gender,date_of_join=date_of_join,job_role=job_role,acc_no=acc_no,ifsc_code=ifsc_code,branch=branch,user_password=user_password)

                user_clock_in = models.user_clock_in.objects.create(emp_id=emp_id,username=user_name,button_id="clock_in",button_name="clock in",button_color="#0BB783", status="0",location="location")

        post_user_create.save()
        user_clock_in.save()
    return render(request, 'admin_templates/crud/user_registration.html')

@login_required(login_url='login_page')
def total_users(request):
    total_users = User.objects.raw("SELECT DISTINCT id,username,first_name,email FROM attendance_tools_user where is_superuser='0'")
    return render(request, "admin_templates/profile/total_users.html", {'total_users':total_users})


@login_required(login_url='login_page')
def user_operations(request):
    user_operation = User.objects.raw("SELECT DISTINCT * FROM attendance_tools_user where is_superuser='0'")
    return render(request, "admin_templates/crud/user_operations.html",{'user_operation':user_operation})

@login_required(login_url='login_page')
def admin_edit_user_profile(request,id):
    admin_edit_user_profile = models.User.objects.get(emp_id=id)
    context = {'admin_edit_user_profile': admin_edit_user_profile,'id':id}
    return render(request, 'admin_templates/crud/admin_edit_user_profile.html', context)

@login_required(login_url='login_page')
def admin_edit_details(request,id):
    admin_edit_user_profile = models.User.objects.get(emp_id=id)
    context = {'admin_edit_user_profile': admin_edit_user_profile,'id':id}
    return render(request, 'admin_templates/crud/admin_edit_user_profile.html', context)

@login_required(login_url='login_page')
def user_profile_pageer(request):
    if request.method == "POST":
        id = request.POST.get('id')
        user_profile = User.objects.get(username=id)
        return render(request,'admin_templates/profile/users_profile_page.html', {'user_profile': user_profile})

@login_required(login_url='login_page')
def user_profile_page(request,id):
        members = User.objects.filter(emp_id=id)
        context = {'members': members, 'id': id}
        return render(request, 'admin_templates/profile/users_profile_page.html', context)

@login_required(login_url='login_page')
def admin_delete_user(request):
    if request.method == "POST":
        id = request.POST.get('id')
        department = User.objects.get(emp_id=id)
        department.delete()
        return HttpResponse(id)


@login_required(login_url='login_page')
def admin_user_update_details(request,id):
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
def admin_user_update_data(request):
    if request.method == 'POST':
        # image = request.FILES.get('profile_avatar')
        admin_user_update_data = models.User(id=request.POST['id'],password=request.POST['password'],emp_id=request.POST['emp_id'], first_name=request.POST['first_name'],
                                last_name=request.POST['last_name'],username=request.POST['username'],
                                dob=request.POST['dob'],module=request.POST['module'],blood_group=request.POST['blood_group'], official_email_id=request.POST['official_email_id'], personal_email_id=request.POST['personal_email_id'],
                                adhar_no=request.POST['adhar_no'],gender=request.POST['gender'], mobile_no=request.POST['mobile_no'],
                                job_role=request.POST['job_role'], address=request.POST['address'],
                                acc_no = request.POST['acc_no'],ifsc_code=request.POST['ifsc_code'],branch=request.POST['branch'],user_image=request.POST['image'],is_lead=request.POST['is_lead'],user_password=request.POST['user_password'])

        admin_user_update_data.save()
    return render(request,"admin_templates/crud/admin_edit_user_profile.html")


@login_required(login_url='login_page')
def user_leave_requests(request):
    leave_requests = models.leave_apply.objects.filter(status='request')
    return render(request,"admin_templates/leave/user_leave_requests.html", {'leave_requests':leave_requests})


@login_required(login_url='login_page')
def view_leave_request_details(request,id):
    view_leave_request = models.leave_apply.objects.get(id=id)
    context = {'view_leave_request': view_leave_request, 'id': id}
    return render(request, 'admin_templates/leave/view_leave_requests.html', context)



@login_required(login_url='login_page')
def leave_request_approval(request):
    if request.method == 'POST':
        leave_dates = request.POST.getlist('leave_dates[]')
        emp_id = request.POST.get('emp_id')
        username = request.POST.get('username')
        clockin_time = ''
        clockout_time = ''
        time = ''
        attendance_form = 'absent'
        calender_form = 'danger'

        with django.db.transaction.atomic():
            for x in range(len(request.POST.getlist('leave_dates[]'))):
                leave_post = models.user_time_log.objects.create(username=username,emp_id=emp_id,user_clockin_time=clockin_time,user_clockout_time=clockout_time,
                                           user_current_date=leave_dates[x],user_total_hours=time,attendance_form=attendance_form,calender_form=calender_form)




                leave_request_approval = models.leave_apply(id=request.POST['id'], emp_id=request.POST['emp_id'],
                                                            username=request.POST['username'], reason=request.POST['reason'],
                                                            leave_days=request.POST['leave_days'],
                                                            start_date=request.POST['start_date'],
                                                            end_date=request.POST['end_date'],
                                                            leave_apply_time=request.POST['applied_time'],
                                                            status=request.POST['status'],lead_name=request.POST['lead_name'])

        leave_post.save()
        leave_request_approval.save()
    return render(request, 'admin_templates/leave/user_leave_requests.html')


@login_required(login_url='login_page')
def leave_request_rejected(request):
    if request.method == 'POST':
        leave_request_rejected = models.leave_apply(id=request.POST['id'],emp_id=request.POST['emp_id'],username=request.POST['username'], reason=request.POST['reason'],
                                leave_days=request.POST['leave_days'],
                                start_date=request.POST['start_date'], end_date=request.POST['end_date'],
                                leave_apply_time=request.POST['applied_time'],status=request.POST['status'],rejected_reason=request.POST['rejected_reason'],lead_name=request.POST['lead_name'])
        leave_request_rejected.save()
        return render(request, 'admin_templates/leave/user_leave_requests.html')


@login_required(login_url='login_page')
def total_employees(request):
    total_employees = User.objects.raw("SELECT DISTINCT id,username,first_name,email FROM attendance_tools_user where is_superuser='0'")
    return render(request,"admin_templates/profile/total_employees.html",{"total_employees":total_employees})

@login_required(login_url='login_page')
def view_attendance_details(request,id):
    today = datetime.now().date()
    total_users = models.user_time_log.objects.raw('select * from attendance_tools_user_time_log where emp_id= %s group by user_current_date',[id])

    today_log = models.user_time_log.objects.filter(emp_id=id,user_current_date=today)
    username = User.objects.filter(emp_id=id)

    return render(request,"admin_templates/profile/user_attendance_details.html",{"total_users":total_users,'today_log':today_log,'username':username})

@login_required(login_url='login_page')
def employee_attendance(request):
    if request.method =='POST':
        fromdate = request.POST.get('fromdate')

        total_users = models.User.objects.filter(is_superuser="0").count()
        today = datetime.now().date()
        # today_attendance_log = models.user_time_log.objects.all().latest('username','-user_clockin_time').distinct('username')

        today_attendance_log = models.user_time_log.objects.raw("SELECT * FROM attendance_tools_user_time_log where user_current_date=DATE(NOW()) and (select max(user_clockin_time) from attendance_tools_user_time_log ) group by username")
        # today_attendance = models.user_time_log.objects.raw("Select emp_id, username,user_total_hours,id,user_clockin_time,user_clockout_time,user_current_date from attendance_tools_user_time_log where user_clockin_time IN(SELECT MAX(user_clockin_time) and distinct username FROM attendance_tools_user_time_log)")
        total_entries_in=models.user_time_log.objects.raw("select * from attendance_tools_user_time_log where(user_clockin_time,user_current_date)in (select max(user_clockin_time) as user_clockin_time,user_current_date=DATE(NOW()) from attendance_tools_user_time_log group by username)  ")
        total_entries=models.user_time_log.objects.raw("select count(distinct username)as count,id from attendance_tools_user_time_log where user_current_date=DATE(NOW())")
        new=models.user_time_log.objects.raw("select distinct emp_id,username,id,min(user_clockin_time)as user_clockin_time,max(user_clockout_time) as user_clockout_time,user_current_date from attendance_tools_user_time_log where user_current_date=%s group by username",[fromdate])
        today_attendance=models.user_time_log.objects.raw("select * from attendance_tools_user_time_log where user_current_date=DATE(NOW()) group by username having max(id) ")
        # today_attendancee=models.user_time_log.objects.raw("select  user_clockin_time , user_clockout_time,emp_id,username,id,user_total_hours from attendance_tools_user_time_log  group by username where (user_current_date=DATE(NOW()) and max(user_clockin_time))")
        new1=models.user_time_log.objects.raw("select  * from attendance_tools_user_time_log where ( id,user_clockin_time) IN (select id,max(user_clockin_time)as user_clockin_time from attendance_tools_user_time_log group by username ORDER BY id)")
        new2=models.user_time_log.objects.raw("select  * from attendance_tools_user_time_log as t join (select max(user_clockin_time)as user_clockin_time from attendance_tools_user_time_log group by username) as o on o.user_clockin_time=t.user_clockin_time  ")


        return render(request,"admin_templates/profile/total_employee_attendance.html",{"today_attendance":today_attendance,'total_users':total_users,'total_entries':total_entries,'today_attendance_log':today_attendance_log,'total_entries_in':total_entries_in,'new':new})
    else:
        total_users = models.User.objects.filter(is_superuser="0").count()
        today = datetime.now().date()

        today_attendance_log = models.user_time_log.objects.raw(
            "SELECT * FROM attendance_tools_user_time_log where user_current_date=DATE(NOW()) and (select max(user_clockin_time) from attendance_tools_user_time_log ) group by username")
        # today_attendance = models.user_time_log.objects.raw("Select emp_id, username,user_total_hours,id,user_clockin_time,user_clockout_time,user_current_date from attendance_tools_user_time_log where user_clockin_time IN(SELECT MAX(user_clockin_time) and distinct username FROM attendance_tools_user_time_log)")
        total_entries_in = models.user_time_log.objects.raw(
            "select * from attendance_tools_user_time_log where(user_clockin_time,user_current_date)in (select max(user_clockin_time) as user_clockin_time,user_current_date=DATE(NOW()) from attendance_tools_user_time_log group by username)  ")
        total_entries = models.user_time_log.objects.raw(
            "select count(distinct username)as count,id from attendance_tools_user_time_log where user_current_date=DATE(NOW())")
        new = models.user_time_log.objects.raw(
            "select distinct emp_id,username,id,max(user_clockin_time)as user_clockin_time,max(user_clockout_time) as user_clockout_time,user_current_date from attendance_tools_user_time_log where user_current_date=DATE(NOW()) group by username")
        today_attendance = models.user_time_log.objects.raw(
            "select * from attendance_tools_user_time_log where user_current_date=DATE(NOW()) group by username having max(id) ")

        return render(request, "admin_templates/profile/total_employee_attendance.html",
                      {"today_attendance": today_attendance, 'total_users': total_users, 'total_entries': total_entries,
                       'today_attendance_log': today_attendance_log, 'total_entries_in': total_entries_in, 'new': new})



@login_required(login_url='login_page')
def project_list(request):
    project_list = models.project.objects.all()
    return render(request, "admin_templates/project/project_list.html",{'project_list':project_list})

@login_required(login_url='login_page')
def lead_list(request):
    lead_list = models.assign_lead.objects.all()
    return render(request, "admin_templates/lead/lead_list.html",{'lead_list':lead_list})


@login_required(login_url='login_page')
def delete_lead(request):
    if request.method == 'POST':
        id1=request.POST.get('id')
        delete1 = models.assign_lead.objects.get(id=id1)
        delete1.delete()
        return render(request, "admin_templates/lead/lead_list.html")




@login_required(login_url='login_page')
def edit_project_details(request,id):
    project_edit = models.project.objects.get(id=id)
    return render(request, "admin_templates/project/edit_project_details.html",{'project_edit':project_edit})

@login_required(login_url='login_page')
def edit_lead(request,id):
    project_edit = models.assign_lead.objects.get(id=id)
    return render(request, "admin_templates/lead/edit_lead.html",{'project_edit':project_edit})
    
    
    
    
@login_required(login_url='login_page')
def save_lead_edit(request):
    if request.method == 'POST':
        edit_lead_save = models.assign_lead(id=request.POST['id'],lead_empid=request.POST['lead_empid'],
                                           lead_name=request.POST['lead_name'],module=request.POST['module'],username=request.POST['username'])

        edit_lead_save.save()


    return render(request, "admin_templates/lead/edit_lead.html")


@login_required(login_url='login_page')
def save_project_edit(request):
    if request.method == 'POST':
        edit_project_save = models.project(id=request.POST['id'],project_name=request.POST['project_name'],
                                           project_code=request.POST['project_code'])

        edit_project_save.save()


    return render(request, "admin_templates/project/assign_project.html")

@login_required(login_url='login_page')
def delete_project(request):
    if request.method == 'POST':
        id1=request.POST.get('id')
        delete1 = models.project.objects.get(id=id1)
        delete1.delete()
        return render(request, "admin_templates/project/project_list.html")



@login_required(login_url='login_page')
def create_project(request):
    users=models.User.objects.filter(is_superuser='0')
    return render(request, 'admin_templates/project/create_project.html', {'users':users})

@login_required(login_url='login_page')
def project_assigning(request):
    return render(request, 'admin_templates/project/project_assigning.html')


@login_required(login_url='login_page')
def view_time_log(request,id):
    view_time_log = User.objects.get(username=id)
    context = {'view_time_log': view_time_log, 'id': id}
    return render(request, 'admin_templates/profile/user_attendance_details.html', context)


@login_required(login_url='login_page')
def project_type_post(request):
    if request.method == 'POST':
        project_type_post = models.project(project_name=request.POST['project_name'],
                                           project_code=request.POST['project_code'])

        project_type_post.save()
        return render(request, 'admin_templates/project/project_assigning.html')


@login_required(login_url='login_page')
def assign_poject_post(request):
    global x
    if request.method == 'POST':
        project_code = request.POST.get('project_code')

        project_name = request.POST.get('project_name')
        # job_name = request.POST.get('job_name')


        username_assign = request.POST.getlist('username_assign[]')
        for x in range(len(request.POST.getlist('username_assign[]'))):
            project_type_post = models.assign_project.objects.create(project_code=project_code,project_name=project_name,
                                           username_assign=username_assign[x])
            # print(x)
            project_type_post.save()


            # usernames = assign_project.objects.filter().exclude(project_code=project_code)
        return render(request, 'admin_templates/project/project_assigning.html')










@login_required(login_url='login_page')
def assign_project(request):
    assign_usernames = User.objects.filter(is_superuser='0')
    usernames=models.assign_project.objects.all().values('username_assign').distinct()

    assign_project = models.project.objects.all()

    return render(request, 'admin_templates/project/assign_project.html',{'assign_usernames':assign_usernames,'assign_project':assign_project,'usernames':usernames})


@login_required(login_url='login_page')
def assign_poject_val(request):
    if request.method == 'POST':
        project_code = request.POST.get('project_code')

        data1 = []
        present_user = []

        assign_usernames = models.assign_project.objects.filter(project_code=project_code)

        for i in assign_usernames:
            data1.append(i.username_assign)
        alluser = models.User.objects.filter(is_superuser='0')

        for j in alluser:
            present_user.append(j.username)

        # for j in range(len(data1)):
        #     present_user.append(models.User.objects.filter(username=data1[j]))
            # no_user.append(models.User.objects.filter(username != data1[j]))
            # fetch_all = models.User.objects.raw("SELECT * FROM attendance_tools_user where username <>%s ",[ data1[j]] )
            # for x in fetch_all:
            #     id12.append(x.username)

        #     usernames=models.User.objects.filter(username=assign_usernames[x])
        #     usernames1.append(usernames.username_assign)
        #     # non_usernames = models.User.objects.exclude(username=assign_usernames[x])
        #
        data={
            'data1': data1,
            'present_user':present_user
        }
        return JsonResponse(data)
        # return HttpResponse(id12)
    # assign_project = models.project.objects.all()

    # return render(request, 'admin_templates/project/assign_project.html',{'assign_usernames':assign_usernames,'assign_project':assign_project,'usernames':usernames})




# @login_required(login_url='login_page')
# def project_list(request):
#     project_list = models.project.objects.all()
#     return render(request, "admin_templates/time_sheet/total_timesheet_users.html",{'project_list':project_list})




@login_required(login_url='login_page')
def total_timesheet_users(request):
    total_timesheet_users = User.objects.raw("SELECT DISTINCT * FROM attendance_tools_user where is_superuser='0'")
    return render(request, "admin_templates/time_sheet/total_timesheet_users.html",{'total_timesheet_users':total_timesheet_users})


@login_required(login_url='login_page')
def total_timesheet(request):
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        total_timesheets = models.timesheet.objects.raw('select * from  attendance_tools_timesheet where  today_date between"'+fromdate+'"and"'+todate+'" and status=%s and leadname=%s ' ,['','admin'] )
        return render(request, "admin_templates/time_sheet/total_timesheet.html", {'total_timesheets': total_timesheets})

    else:
        total_timesheets = models.timesheet.objects.filter(work_status='request',leadname='admin')
        return render(request, "admin_templates/time_sheet/total_timesheet.html",{'total_timesheets':total_timesheets})


@login_required(login_url='login_page')
def time_sheet_request(request):
    if request.method == "POST":      
        fromdate = request.POST.get('fromdates')
        todate = request.POST.get('todates')
        
        time_sheet_request=models.timesheet.objects.raw('select * from  attendance_tools_timesheet where today_date between"'+fromdate+'"and"'+todate+'" and status=%s and leadname!=%s ',['','admin'])
        return render(request, "admin_templates/time_sheet/time_sheet_request.html",{'time_sheet_request':time_sheet_request})
    else:
        time_sheet_request = models.timesheet.objects.filter(work_status='request')
        return render(request, "admin_templates/time_sheet/time_sheet_request.html",{'time_sheet_request':time_sheet_request})


@login_required(login_url='login_page')
def timesheet_view(request,id):
    timesheet_view = models.timesheet.objects.get(id=id)

    return render(request, "admin_templates/time_sheet/timesheet_view.html",{'timesheet_view':timesheet_view})\



@login_required(login_url='login_page')
def timesheet_approval(request):
    if request.method == 'POST':
        timesheet_approval = models.timesheet(id=request.POST['id'],emp_id=request.POST['emp_id'],username=request.POST['username'],project_name=request.POST['project_name'],project_code=request.POST['project_code'], 
                                task_name=request.POST['task_name'],
                                hours=request.POST['hours'], posting_date=request.POST['posting_date'],image=request.POST['image'], description=request.POST['description'],
                                work_status=request.POST['work_status'],today_date=request.POST['today_date'],leadname=request.POST['leadname'])
        timesheet_approval.save()
    return render(request, 'admin_templates/leave/user_leave_requests.html')



@login_required(login_url='login_page')
def timesheet_reject(request):
    if request.method == 'POST':
        leave_request_approval = models.timesheet(id=request.POST['id'],emp_id=request.POST['emp_id'],username=request.POST['username'],project_name=request.POST['project_name'],project_code=request.POST['project_code'],
                                task_name=request.POST['task_name'],
                                hours=request.POST['hours'], posting_date=request.POST['posting_date'],image=request.POST['image'], description=request.POST['description'],
                                work_status=request.POST['work_status'],today_date=request.POST['today_date'],rejected_reason=request.POST['timesheet_rejected_reason'],leadname=request.POST['leadname'])
        leave_request_approval.save()
    return render(request, 'admin_templates/leave/user_leave_requests.html')


@login_required(login_url='login_page')
def user_leave_approvals(request):
    user_leave_approvals=models.leave_apply.objects.filter(status='approved'  )
    return render(request, "admin_templates/leave/user_leave_approvals.html",{'user_leave_approvals':user_leave_approvals})


@login_required(login_url='login_page')
def view_leave_approvals(request,id):
    view_leave_approvals=models.leave_apply.objects.get(id=id)
    return render(request, "admin_templates/leave/view_leave_approvals.html",{'view_leave_approvals':view_leave_approvals})


@login_required(login_url='login_page')
def user_timesheet_approvals(request):
    user_timesheet_approvals=models.timesheet.objects.raw( "select * from attendance_tools_timesheet where  work_status='approved'   and leadname!=%s ORDER BY posting_date DESC;",['admin'])
    
    return render(request, "admin_templates/time_sheet/user_timesheet_approvals.html",{'user_timesheet_approvals':user_timesheet_approvals})


@login_required(login_url='login_page')
def total_users_leave(request):
    total_users_leave = User.objects.raw("SELECT DISTINCT * FROM attendance_tools_user where is_superuser='0'")
    return render(request, "admin_templates/leave/total_users_leave.html",{'total_users_leave':total_users_leave})


@login_required(login_url='login_page')
def view_user_leave_datas(request,id):
    view_user_leave_datas = models.leave_apply.objects.filter(username=id)
    username=id
    return render(request, "admin_templates/leave/view_user_leave_datas.html",{'view_user_leave_datas':view_user_leave_datas,'username':username})



@login_required(login_url='login_page')
def view_leave_data_details(request,id):
    view_leave_data_details = models.leave_apply.objects.get(id=id)

    return render(request, "admin_templates/leave/view_leave_data_details.html",{'view_leave_data_details':view_leave_data_details})



@login_required(login_url='login_page')
def total_user_attendance(request,id):
    total_user_attendance = models.user_time_log.objects.filter(emp_id=id,attendance_form='present')
    # username=id

    return render(request, "admin_templates/profile/total_user_attendance.html",{'total_user_attendance':total_user_attendance})


@login_required(login_url='login_page')
def user_location_requsts(request):
    user_location_requsts = models.emp_location.objects.filter(status='request')

    return render(request, "admin_templates/profile/user_location_requsts.html",{'user_location_requsts':user_location_requsts})



@login_required(login_url='login_page')
def view_location_request_details(request,id):
    view_location_request_details = models.emp_location.objects.get(id=id)

    return render(request, "admin_templates/profile/view_location_request_details.html",{'view_location_request_details':view_location_request_details})




@login_required(login_url='login_page')
def view_user_timesheets(request,id):
    view_my_timesheet = models.timesheet.objects.filter(emp_id=id,status='')
    return render(request, 'admin_templates/time_sheet/view_user_timesheets.html',{'view_my_timesheet':view_my_timesheet})


@login_required(login_url='login_page')
def announcement(request):
    return render(request, 'admin_templates/profile/announcement.html')
    
    
    
@login_required(login_url='login_page')
def emp_log(request):
    today = datetime.now().date()
    emp_log = models.user_clock_in.objects.filter(status='1',curr_date=today).order_by('curr_time')
    total_users = models.User.objects.filter(is_superuser="0").count()
    total_entries=models.user_time_log.objects.raw("select count(distinct username)as count,id from attendance_tools_user_clock_in where curr_date=DATE(NOW())")
    return render(request, 'admin_templates/profile/employee_log.html',{'total_users':total_users,'total_entries':total_entries,'emp_log':emp_log})














@login_required(login_url='login_page')
def assign_lead(request):
    assign_lead = User.objects.filter(is_lead='1')
    allusers = User.objects.filter(is_superuser='0',is_lead='0')
    allusers_assign = models.assign_lead.objects.all()

    return render(request, "admin_templates/lead/assign_lead.html",{'assign_lead':assign_lead,'allusers':allusers,'allusers_assign':allusers_assign})

@login_required(login_url='login_page')
def assign_lead_post(request):
    global x
    if request.method == 'POST':
        leadname = request.POST.get('leadname')
        lead_empid = request.POST.get('lead_empid')

        module = request.POST.get('module')
        # username = request.POST.get('username')


        username = request.POST.getlist('username[]')
        for x in range(len(request.POST.getlist('username[]'))):
            lead_post = models.assign_lead.objects.create(lead_name=leadname,module=module,lead_empid=lead_empid,
                                           username=username[x])
            # print(x)
            lead_post.save()


            # usernames = assign_project.objects.filter().exclude(project_code=project_code)
    return render(request, 'admin_templates/lead/assign_lead.html')


@login_required(login_url='login_page')
def admin_announcement(request):
  if request.method == 'POST':

        announcement_test = request.POST.get("announcement")
        announcement=announcement_test + ' | '
        today_date = request.POST.get("today_date")
        admin_anno = models.announcement.objects.create(announcement=announcement,today_date=today_date)
        admin_anno.save()
  return render(request, 'admin_templates/profile/announcement.html')

@login_required(login_url='login_page')
def user_location_approval(request):
    if request.method == 'POST':
        leave_request_rejected = models.emp_location(id=request.POST['id'],emp_id=request.POST['emp_id'],name=request.POST['username'],
                                lat=request.POST['lat'],
                                lon=request.POST['lon'], status=request.POST['status'],added_by=request.POST['added_by'])
        leave_request_rejected.save()
    return render(request, 'admin_templates/profile/view_location_request_details.html')

@login_required(login_url='login_page')
def user_location_rejected(request):
    if request.method == 'POST':
        leave_request_rejected = models.emp_location(id=request.POST['id'],emp_id=request.POST['emp_id'],name=request.POST['username'],
                                lat=request.POST['lat'],
                                lon=request.POST['lon'], status=request.POST['status'],added_by=request.POST['added_by'])
        leave_request_rejected.save()
    return render(request, 'admin_templates/profile/view_location_request_details.html')