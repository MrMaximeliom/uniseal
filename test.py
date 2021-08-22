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
    #create file (workbook) and worksheet
    # testWorkBok = xlsxwriter.Workbook("test.xlsx")
    # testSheet = testWorkBok.add_worksheet()
    # # create headers
    # testSheet.write("A1","Names")
    # testSheet.write("B1","Money")
    # # write data to file
    # for item in range(len(names)):
    #     testSheet.write(item+1,0,names[item])
    #     testSheet.write(item+1,1,money[item])
    # testWorkBok.close()
    # namesAndCols = {
    #     0:"Names",
    #     1:"Money"
    # }
    # from string import ascii_uppercase
    # loop = 0
    # AlphabetLetters =  ''.join(c for c in ascii_uppercase)
    # print(AlphabetLetters[1])
    #
    # for c in range(len(namesAndCols)):
    #     print(f"{AlphabetLetters[c]}1",namesAndCols[c])

    # testFun("s",data=names,money=money)
    # headers = []
    # headers.append("df")
    # print(headers[0])
    for page in range(1,1):
        print(page)