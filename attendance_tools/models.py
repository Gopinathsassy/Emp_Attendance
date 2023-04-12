from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, User


class User(AbstractUser):
    is_lead = models.BooleanField(default=0)
    emp_id = models.CharField(max_length=50, default="", unique=True)
    # username = models.CharField(max_length=50, default="", unique=True)
    # first_name = models.CharField(max_length=50, default="", unique=True)
    gender = models.CharField(max_length=50, default="")
    job_role = models.CharField(max_length=50, default="")
    blood_group = models.CharField(max_length=50, default="")
    module = models.CharField(max_length=50, default="")
    date_of_join = models.CharField(max_length=50, default="")
    date_of_birth = models.CharField(max_length=50, default="")
    official_email_id = models.CharField(max_length=50, default="")
    personal_email_id = models.CharField(max_length=50, default="")
    dob = models.CharField(max_length=50, default="")
    adhar_no = models.CharField(max_length=50, default="")
    mobile_no = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=500, default="")
    acc_no = models.CharField(max_length=50, default="")
    ifsc_code = models.CharField(max_length=50, default="")
    branch = models.CharField(max_length=50, default="")
    user_image = models.ImageField(upload_to="user_images/", null=True)
    user_password = models.CharField(max_length=50, default="")



class attendance_mail_table(models.Model):
    emp_id = models.CharField(max_length=50, default="")
    username = models.CharField(max_length=50, default="")
    in_time = models.CharField(max_length=50, default="")
    out_time = models.CharField(max_length=50, default="")
    # current_date = models.CharField(max_length=50, default="")
    status = models.CharField(max_length=50, default="")

class clockin(models.Model):
    current_date =models.CharField(max_length=50, default="")
    current_time =models.CharField(max_length=50, default="")
    username=models.CharField(max_length=50, default="")
    emp_id= models.CharField(max_length=50, default="")
    update_current_time= models.CharField(max_length=50, default="")
    update_current_date= models.CharField(max_length=50, default="")
    duration = models.CharField(max_length=50, default="")

class clockout(models.Model):
    current_date =models.CharField(max_length=50, default="")
    clockout_time =models.CharField(max_length=50, default="")
    username=models.CharField(max_length=50, default="")
    emp_id=models.CharField(max_length=50, default="")
     # = models.CharField(max_length=50, default="")


class user_clock_in(models.Model):
    curr_date =models.CharField(max_length=50, default="")
    curr_time =models.CharField(max_length=50, default="")
    username=models.CharField(max_length=50, default="")
    emp_id= models.CharField(max_length=50, default="")
    button_id=models.CharField(max_length=50, default="")
    button_name = models.CharField(max_length=50, default="")
    button_color = models.CharField(max_length=50, default="")
    status=models.CharField(max_length=50, default="")
    location = models.CharField(max_length=50, default="")

class user_time_log(models.Model):
    username=models.CharField(max_length=50, default="")
    emp_id= models.CharField(max_length=50, default="")
    user_clockin_time= models.CharField(max_length=50, default="")
    user_clockout_time= models.CharField(max_length=50, default="")
    user_current_date= models.CharField(max_length=50, default="")
    user_total_hours = models.CharField(max_length=50, default="")
    attendance_form = models.CharField(max_length=50, default="")
    calender_form = models.CharField(max_length=50, default="")
    



class leave_apply(models.Model):
    username=models.CharField(max_length=50, default="")
    emp_id= models.CharField(max_length=50, default="")
    reason=models.CharField(max_length=255, default="")
    leave_days= models.CharField(max_length=50, default="")
    start_date= models.CharField(max_length=50, default="")
    end_date= models.CharField(max_length=50, default="")
    # description  = models.CharField(max_length=50, default="")
    lead_name= models.CharField(max_length=50, default="")
    leave_apply_time= models.CharField(max_length=50, default="")
    status= models.CharField(max_length=50, default="")
    rejected_reason=models.CharField(max_length=255, default="")


class Image(models.Model):
    image = models.CharField(max_length=50, default="")
    current_time = models.CharField(max_length=50, default="")
    user_current_date = models.CharField(max_length=50, default="")



class timesheet(models.Model):
    username = models.CharField(max_length=150, default="")
    emp_id= models.CharField(max_length=150, default="")
    module= models.CharField(max_length=150, default="")
    project_name = models.CharField(max_length=150, default="")
    project_code = models.CharField(max_length=150, default="")
    # job_name = models.CharField(max_length=150, default="")
    status= models.CharField(max_length=150, default='')
    work_status = models.CharField(max_length=150, default='')
    posting_date= models.DateField(default=datetime.now)

    task_name= models.CharField(max_length=150, default="")
    hours = models.CharField(max_length=150, default="")
    today_date = models.CharField(max_length=150, default="")
    description= models.CharField(max_length=500, default="")
    image = models.ImageField(upload_to="images_timesheet/", null=True)
    rejected_reason = models.CharField(max_length=500, default="") 
    leadname = models.CharField(max_length=500, default="")


class timesheet_option_val(models.Model):
    project_name = models.CharField(max_length=150, default="")
    project_code = models.CharField(max_length=150, default="")
    job_name = models.CharField(max_length=150, default="")


class emp_location(models.Model):
    emp_id = models.CharField(max_length=150, default="")
    name = models.CharField(max_length=150, default="")
    lat = models.CharField(max_length=150, default="")
    lon = models.CharField(max_length=150, default="")
    added_by = models.CharField(max_length=150, default="")
    status = models.CharField(max_length=150, default="")

class project(models.Model):
    project_name = models.CharField(max_length=150, default="")
    project_code= models.CharField(max_length=150, default="")
    job_name = models.CharField(max_length=150, default="")


class assign_project(models.Model):

    project_code = models.CharField(max_length=150, default="")
    job_name = models.CharField(max_length=150, default="")
    project_name = models.CharField(max_length=150, default="")
    username_assign= models.CharField(max_length=150, default="")
    # job_name = models.CharField(max_length=150, default="")


class announcement(models.Model):
    announcement = models.CharField(max_length=500, default="")
    today_date = models.CharField(max_length=50, default="")
    
    
    
class overall_work_hours(models.Model):
        emp_id = models.CharField(max_length=50, default="")
        username = models.CharField(max_length=50, default="")
        dates = models.CharField(max_length=50, default="")
        hours = models.CharField(max_length=50, default="")
        location = models.CharField(max_length=50, default="")
        note2 = models.CharField(max_length=50, default="")
        note3 = models.CharField(max_length=50, default="")
   
    
class assign_lead(models.Model):
    lead_name = models.CharField(max_length=150, default="")
    lead_empid = models.CharField(max_length=150, default="")
    module = models.CharField(max_length=150, default="")
    username = models.CharField(max_length=150, default="")
    
    