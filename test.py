import os

import xlsxwriter
names = ["Moayed","Mazen","Ali"]
money = [34,90,70]
def testFun(param,**kwargs):
    # for i in kwargs["names"]:
    #     print(i)
    x_position = -1
    for key, value in kwargs.items():
        x_position = x_position + 1
        for item in range(len(value)):
            print(item + 1, x_position, value[item])

if __name__ == "__main__":
    # dir = os.path.abspath('.').split(os.path.sep)[0]+os.path.sep
    # print(dir)
    # print(os.path.expanduser("~/Desktop"))
    desktop_dir = os.path.expanduser("~/Desktop")
    # creating Reports directory
    reports_dir = "Reports"
    # create reports directory in desktop directory
    path = os.path.join(desktop_dir, reports_dir)
    from datetime import date

    today = date.today()
    print("Today's date:", today)
    from datetime import datetime

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)



