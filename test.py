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
    # desktop_dir = os.path.expanduser("~/Desktop")
    # # creating Reports directory
    # reports_dir = "Reports"
    # # create reports directory in desktop directory
    # path = os.path.join(desktop_dir, reports_dir)
    # from datetime import date
    #
    # today = date.today()
    # print("Today's date:", today)
    # from datetime import datetime
    #
    # now = datetime.now()
    #
    # current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)
    # print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # import tempfile
    # import shutil
    #
    # # tempfile.TemporaryDirectory(dir=os.getcwd())
    #
    # op = tempfile.TemporaryDirectory(dir=os.getcwd())
    # dd = "lolp"
    # path = os.path.join(op.name, dd)
    # os.mkdir(path)
    # tempDir = tempfile.mkdtemp('tmplnqjxx1q2sss')
    # print(tempDir," --- ---- -- ")
    # remove temprorary directory
    # shutil.rmtree(tempDir)
    # import re

    # initializing string
    # test_string = input("Enter a sentence now\n")

    # # printing original string
    # print("The original string is : " + test_string)
    # # removing all leading and spaces in beginning and endings
    # tito = test_string.strip()
    # tito2 = tito.replace(" ", "")
    # print("The original string without spaces : " + tito2)
    #
    # search_phrase = re.findall(r'\w+', test_string)
    # special_char = re.findall(r'\W', test_string.replace(" ", ""))
    # if len(special_char) > 0 :
    #     print("You have special chars in your sentence")
    # else:
    #     print("Your sentence is ready to be used in db connection")
    # print("original words are: ",search_phrase)
    # print("special words are: ",special_char)
    # isOK,phone_number = check_phone_number(test_string)
    # if isOK:
    #     print(phone_number)
    # main directory for reports
    # os.path.dirname(os.path.abspath(__file__)) + "/Reports"
    # import os, re, os.path
    # delete all files inside directory

    # mypath = "/home/moayed/PycharmProjects/uniseal/Util/Reports"
    # print("deleting all files")
    # for root, dirs, files in os.walk(mypath):
    #     for file in files:
    #         os.remove(os.path.join(root, file))
    # from datetime import datetime
    # now = datetime.now()
    # current_time = now.strftime("%H_%M_%S")
    # print(current_time)
    path = os.path.dirname(os.path.abspath(__file__)) + "/Reports"
    # selected_pages = ['1','2']
    # for i in selected_pages:
    #     print("hi")
    # must end with colon
    # selected_images = '/media/project_images/temp_1_AuGu1HL.png',
    # for i in selected_images:
    #     print(i)
#    /media/product_images/ehab_1.jpg
    if os.path.exists("/media/product_images/ehab_1.jpg"):
        print("yeah it is")
    print(os.path.dirname(os.path.abspath(__file__)))
        # os.remove("demofile.txt")








