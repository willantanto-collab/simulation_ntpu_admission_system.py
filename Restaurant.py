# A-Level 9618 Revision: 为了复习即将到来的考试，而做出的练习。
# 文件内的格式，学校出的历年卷子。练习题2024-2025 年。文件本身学校文件里有提供。
# B01,Coffee,2.5 
# B02,Tea,1.5
#...... 到B10,Smoothie,2.0
# 学校课上有做，在实践课上，电脑室里写的一部分。目的是为了稳固基础和推进逻辑思维，改进自已欠缺的地方

# *这是关于file handling,以及其中的逻辑思维在现实中的生活当中。这次模拟的是叫餐，和将客人叫的餐以及要求，通过代码送到另一个窗口送达信息。

#a
BeverageQueue = [""] * 10
BeverageFrontPointer = 0
BeverageRearPointer = 0

#b(i)
def DisplayMenu():
    try:
        file = open("BeverageData.txt","r")
        for line in file:
            Beverage = line.strip() # strip() remove specific character in the bracket(),if none mean remove white space
            print(Beverage)
        file.close()
    except FileNotFoundError:
        print("Not found,error")
#b(ii)
def TakeOrder():
    global BeverageRearPointer,BeverageQueue
    num = int(input("Number of beverage: "))
    file = open("BeverageData.txt","r")
    menu_list = []
    for line in file:
        clean_file = line.strip() 
        parts = clean_file.split(",") #split (",") 将其用， 分开，并弄成array。比如[a b c d] 变成["a","b","c","d"]
        if len(parts) > 1:
            menu_list.append(parts[1]) # 由于格式是B01,Coffee,2.5 这样的情况下，Beverage is Coffee.So append(parts[1]),if B01 mean append(parts[0])
    file.close()
    for i in range(num):
        item_input = input（f"Enter beverage {i + 1}: ")
        clean_item = item_input.strip()
        if clean_item in menu_list:
            if BeverageRearPointer <10:
                BeverageQueue [BeverageRearPointer] = clean_item
                BeverageRearPointer += 1
                order file = open ("Order.txt", "a")
                order_file.write (clean_item + "\n")
                order_file.close ()
                print(f"Added {clean_item} to order")
            else:
                print("Queue is full")
        else:
            print(f"Error : {clean_item} is not on the menu")
#b(iii)
def EnqueueBeverage(DataToEnqueue : str):
    global BeverageRaerPointer,BeverageQueue
    if BeverageRaerPointer == 10:
        return False
    else:
        BeverageQueue[BeverageRearPointer] = DataToEnqueue
        BeverageRearPointer += 1
        return True
#b(iv) 
def ReadOrderData():
    try: 
        order_file = open("Order.txt","r")
        for line in order_file:
            item = line.strip()
            success = EnqueueBeverage(item)
            if success:
                print(f"Added {item} to queue.")
            else:
                print("Queue is full.More item will not be added.")
                break
        order_file.close()
    except FileNotFoundError:
        print("Error,order_file not found")
