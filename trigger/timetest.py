# from datetime import datetime
from datetime import datetime
import MySQLdb
# import datetime

db = MySQLdb.connect(host="localhost",
                     user="cbainruy_inno_attendance",
                     passwd="innoattendance",
                     db="cbainruy_inno_attendance")

cur = db.cursor()
usernames = cur.execute("SELECT username,id FROM  attendance_tools_user_clock_in ")

aa = datetime.now()
user_current_time=aa.strftime("%H:%M:%S")
print(user_current_time)
for a in cur.fetchall():
    data = a[0]
    # print(str(data))

    fetch_all = cur.execute("SELECT * FROM attendance_tools_user_clock_in where status=1 and username=%s",[data])
    for x in cur.fetchall():
        id = x[0]
        date = x[1]
        timess = x[2]
        username1 = x[3]
        emp_id = x[4]
        button_color = x[5]
        button_id = x[6]
        button_name = x[7]
        location = x[8]
        status = [9]
        print("x[2]")
        print(timess)
        calender_form='warning'
        s1 = timess
        s2 = user_current_time
        FMT = '%H:%M:%S'
        frmt=datetime.strptime('00:00:00', FMT)
        total_hour = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        total_hours = (frmt+total_hour).time()
        print(total_hours)
        attendance_form='non_clockout_absent'

        sql = ("""INSERT INTO attendance_tools_user_time_log(username,emp_id,user_clockin_time,user_clockout_time,user_current_date,user_total_hours,attendance_form,calender_form)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""")
        data = (username1,emp_id,timess,user_current_time,date,total_hours,attendance_form,calender_form)
        cur.execute(sql, data)
        db.commit()


        code=("UPDATE attendance_tools_user_clock_in SET id=id,curr_time='',curr_date='',username=username,emp_id=emp_id,button_color='#6610f2',button_id='clock_in',button_name='clock in',location ='location1',status='0' WHERE id='%s'")

        cur.execute(code, (id,))
        db.commit()
        # print("succes")
        fetch_all = cur.execute("SELECT * FROM  attendance_tools_overall_work_hours where dates=DATE(NOW()) and emp_id= %s ",[emp_id])
        if fetch_all:
            for a in cur.fetchall():
                id = a[0]
                emp_ids = a[1]
                username = a[2]
                datess = a[3]
                hours = a[4]
                locations = a[5]
                hrs=str(total_hours)
                print('aa')
                if emp_id == emp_ids and datess == date:
                    print('ff')
                    t1 = datetime.strptime(hours, '%H:%M:%S')
                    t2 = datetime.strptime(hrs, '%H:%M:%S')
                    time_zero = datetime.strptime('00:00:00', '%H:%M:%S')
                    cal = (t1 - time_zero + t2).time()

                    code = ("UPDATE attendance_tools_overall_work_hours SET id=%s,emp_id=%s,username=%s,dates=%s,hours=%s,location=%s where dates=DATE(NOW()) and emp_id=%s")
                    val = (id, emp_ids, username, datess,cal, locations,emp_ids)
                    cur.execute(code, val)
                    db.commit()
                    print('if')



        else:
            print('else')
            sql = ("INSERT INTO attendance_tools_overall_work_hours (username,emp_id,dates,hours,location)VALUES(%s,%s,%s,%s,%s)")
            data = (username1, emp_id, date, total_hours, location)
            cur.execute(sql, data)
            db.commit()
            print('elseif')
db.close()