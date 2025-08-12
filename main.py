import json
import random
import string
from pathlib import Path
import os

class Bank:
    database = 'data.json'
    data =[]
    
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("no such file exist")        
            
    except   Exception as err:
        print(f"an erroe accured {err}") 
        
        
    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(Bank.data))
            
    @classmethod
    def __accountgenrate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%&",k=1)
        id = alpha + num +spchar
        random.shuffle(id)
        return "".join(id)        
            
                     
    def Createaccount(self):
        info = {
            "name":input("tell your name :-"),
            "age":int(input("tell your age :-")),
            "email":input("tell your email :-"),
            "pin":int(input("tell your pin :-")),
            "accountNo.":Bank.__accountgenrate(),
            "Balance":0
        }
        if info['age'] <18 or len(str(info['pin'])) !=4:
            print("sorry you cann't create your account")
        else:
            print("ACCOUNT HAS BEEN CREATED SUCCESSFULLY....")
            for i in info:
                print(f"{i} : {info [i]}")
            print("Please note down the account number")
            
            Bank.data.append(info)
            Bank.__update()
            
    def Depositmoney(self):
        accnumber = input("please tell your account number :-")
        pin = int(input("please tell your pin :-"))
        
        userdata =[i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] ==pin ]
        
        if userdata == False:
            print("Sorry..! No data found")
        else:
            amount = int(input("How much you want to deposit :-"))
            if amount >10000 or amount <0:
                print("Sorry the amount is too much you can deposit below 10,000 and above 0")
            else:
                print(userdata)
                userdata[0]['Balance'] += amount
                Bank.__update()
                print("Amount deposit successfully...")    
                           
    def withdrawmoney(self):
        accnumber = input("please tell your account number :-")
        pin = int(input("please tell your pin :-"))
        
        userdata =[i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] ==pin ]
        
        if userdata == False:
            print("Sorry..! No data found")
        else:
            amount = int(input("How much you want to withdraw :-"))
            if userdata [0]['Balance'] < amount:
                print("Sorry you don't have much money")
            else:
                # print(userdata)
                userdata[0]['Balance'] -= amount
                Bank.__update()
                print("Amount withdrew successfully...") 
                
    def showdetails(self):
        accnumber = input("please tell your number :-")
        pin = int(input("please tell your pin :-"))
        userdata =[i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] ==pin ]
        print("your information are \n\n\n")
        for i in userdata[0]:
            print(f"{i} : {userdata [0][i]}")
            
    def updatedetials(self):
        accnumber = input("please tell your account number :-")
        pin = int(input("please tell your pin :-"))
        userdata =[i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] ==pin ]
        
        if userdata == False:
            print("No such user found")
        else:
            print("You can not change the age,account number, balane")            
            print("Fill the details for change or leave it empty if no change")
            
            newdata = {
                "name":input("Please tell your new name and press enter :"),
                "email":input("please tell your new email id and press enter :"),
                "pin":input("please tell your new pin and press enter to skip :")
                
            }
            
            if newdata["name"] == "":
                newdata["name"]=userdata[0]['name']            
            if newdata["email"] == "":
                newdata["email"]=userdata[0]['email']            
            if newdata["pin"] == "":
                newdata["pin"]=userdata[0]['pin']            
                   
            newdata["age"]=userdata[0]['age']            
            newdata["accountNo."]=userdata[0]['accountNo.']            
            newdata["Balance"]=userdata[0]['Balance']  
            
            if type(newdata['pin'])==str:
                newdata['pin'] = int(newdata['pin'])
                
                
            for i in newdata:
                if newdata[i]== userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newdata[i]
                    
            Bank.__update()
            print("Details updated successfully...") 
            
    def deleteaccount(self):
        accnumber = input("please tell your account number :-")
        pin = int(input("please tell your pin :-"))
        userdata =[i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] ==pin ]
        
        if userdata== False:
            print("Sorry no such data found")
        else:
            check = input("press y if you want to delete account or press n :")    
            if check == 'n' or check =="N":
                print("bypassed")
            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Your account has been delete successfully")
                Bank.__update()               
                        
                      

user = Bank()

print("Press 1 for crerating an account")
print("Press 2 for Depositing the money")
print("Press 3 for withdrwaing the money")
print("Press 4 for details")
print("Press 5 for updatings the details")
print("Press 6 for deleting an account")

check = int(input("Tell your response :-"))

if check ==1:
    user.Createaccount()

if check ==2:
    user.Depositmoney()

if check ==3:
    user.withdrawmoney()

if check ==4:
    user.showdetails()

if check ==5:
    user.updatedetials()

if check ==6:
    user.deleteaccount()
