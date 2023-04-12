from datetime import datetime
import datetime
import MySQLdb
# import datetime

db = MySQLdb.connect(host="localhost",
                     user="cbainruy_emp_attendance",
                     passwd="empattendance",
                     db="cbainruy_emp_attendance")

cur = db.cursor()


sql = ("INSERT INTO attendance_tools_attendance_mail_table(emp_id, username, in_time, out_time, status)VALUES(%s,%s,%s,%s,%s)")
data = ('emp_id','emp_id','timess','user_current_time','total_hours')
cur.execute(sql, data)
db.commit()


db.close()



# from win10toast import ToastNotifier
#     # Example
# toaster = ToastNotifier()
# toaster.show_toast(

#     "Hello All...!!!",
#     "Please Submit Your Timesheet...!",
#     duration=10)
# toaster.show_toast(
#       "Thank You...")










