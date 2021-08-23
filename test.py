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
    print("Hi")

