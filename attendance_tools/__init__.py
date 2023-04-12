# # import time
# # from datetime import datetime
#
# # while (True):
#     # now = datetime.now()
#     # intime = '10:10:00'
#     # current_time = now.strftime("%H:%M:%S")
#     # timenow = str(current_time)
#     #
#     # t1 = datetime.strptime(intime, "%H:%M:%S")
#     #
#     # t2 = datetime.strptime(timenow, "%H:%M:%S")
#     #
#     # delta = t2 - t1
#     # seconds = int(delta.total_seconds())
#     # sec_diff = seconds % 60
#     # if sec_diff < 10:
#     #     sec_diff = '0' + str(sec_diff)
#     # sec_difference = str(sec_diff)
#     #
#     # minutes = (int(seconds) - int(sec_diff)) / 60
#     # min_diff = int(minutes % 60)
#     # if min_diff < 10:
#     #     min_diff = '0' + str(min_diff)
#     # min_difference = str(min_diff)
#     #
#     # hour_diff = int((minutes - min_diff) / 60)
#     # if hour_diff < 10:
#     #     hour_diff = '0' + str(hour_diff)
#     # hour_difference = str(hour_diff)
#     # print(hour_difference + ':' + min_difference + ':' + sec_difference)
#     # time.sleep(1)
#
# import MySQLdb
#
# # Connecting to the Database
# mydb = MySQLdb.connect(
#     host='localhost',
#     database='attendance',
#     user='root',
# )
#
# cs = mydb.cursor()
# id=1
# # drop clause
# fetch_all = cs.execute("SELECT id,current_date,current_time,username,emp_id,button_color,button_id,button_name,location,status FROM  attendance_tools_user_clock_in where status=1 and username=%s",['user2'])
# for x in cs.fetchall():
#     id = x[0]
#     date = x[1]
#     timess = x[2]
#     username = x[3]
#     emp_id = x[4]
#     button_color = x[5]
#     button_id = x[6]
#     button_name = x[7]
#     location = x[8]
#     status = [9]
#     print(timess)
# try:
#  cs.execute(statement)
#  mydb.commit()
#  print("succes")
# except:
#  mydb.rollback()
#  print("error")
# # cs.execute(statement)
# # mydb.commit()
# #
# # # Disconnecting from the database
# # mydb.close()
#
