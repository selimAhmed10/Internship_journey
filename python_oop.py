#Class and the Object 

class Person:   #create class using the by class 
    species="Homo sapiens"  #class attribute
    
    #its mainly works for constructor. Uswed to initiliaze the object data 
    #dunder method 
    def __init__(self,name,age):  #self refers to the current object
        self.name=name  #instance attribute
        self.age=age
        
    #display function    
    def display(self):
        return f"Name: {self.name}, Age: {self.age} ,species{self.species}"
     
#Object -instance of a class    
person1=Person("Selim Ahmed",23)
person2=Person("Al Jaber Vaiea",29)
print(person1.name)
print(person1.age)
print(person1.species)

print(person2.name)
print(person2.age)
print(person2.species)

print(person1.display())
print(person2.display())
        


#Encapsulation binds( method and the data unsing access modifier)

class Bankaccount:
    def __init__(self,owner_name,account_num,balance):   #dunder method
        self.owner_name=owner_name   #public
        self._account_num=account_num  #protected
        self.__balance=balance #private 
        
    def get_balance(self):   #for get the value of the private 
        return self.__balance
    
    def deposit(self,amount):  #normal a deposit method
        if amount>0:
            self.__balance +=amount
 
            return f"{amount} add so total : {self.__balance}"
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return f"Withdrew: ${amount}, New balance: ${self.__balance}"
        return "Insufficient funds"

account1=Bankaccount("selim",12343,1000)

print(f"Name:{account1.owner_name}")
print(f"Account:{account1._account_num}")
print(f"Balance:{account1.get_balance()}")
print(account1.deposit(300))
print()



account2=Bankaccount("Al Jaber Bhaiea",12343,100000000000)

print(f"Name:{account2.owner_name}")
print(f"Account:{account2._account_num}")
print(f"Balance:{account2.get_balance()}")
print(account2.deposit(99999999))
print()

#--------------------------
#Inheritence
#--------------------------
class Savings(Bankaccount):  # inherit from Bankaccount class
    def __init__(self, owner_name, account_num, balance, interest_rate):  #dunder method its use for print the object into string 
        super().__init__(owner_name, account_num, balance)  # call parent class
        self.interest_rate = interest_rate
    
    def interest_add(self):
        interest = self.get_balance() * self.interest_rate / 100
        self.deposit(interest)
        return f"Added interest ${interest:.2f}, Now total: ${self.get_balance()}"

class StudentAccount(Bankaccount):
    def __init__(self, own_name, account_num, balance, student_id):
        super().__init__(own_name, account_num, balance)   # inherit from Bankaccount class
        self.student_id = student_id


inherit1 = StudentAccount("Selim", 12343, 1000, 300)

print(f"Name:{inherit1.owner_name}")
print(f"Account:{inherit1._account_num}")
print(f"Balance:{inherit1.get_balance()}")
print(inherit1.deposit(300))
print(inherit1.withdraw(200))  
print(inherit1.withdraw(600))  
print()

inheri2 = Savings("Al Jaber Bhaiya", 54321, 10000, 5)  

print(f"Name:{inheri2.owner_name}")
print(f"Account:{inheri2._account_num}")
print(f"Balance: {inheri2.get_balance()}")
print(inheri2.deposit(5000))
print(inheri2.interest_add())
print(inheri2.withdraw(2000))


#Abstractions : 

from abc import ABC, abstractmethod

class AccountRules(ABC):     
    @abstractmethod
    def rules(self):   #pass the value for future implement
        pass

class NewSavings(Savings, AccountRules):
    def rules(self):
        return f"Rule: {self.interest_rate} interest, max withdraw can 500"

test= NewSavings("check",99999,5000,5)
print()
print(test.rules())
print(f"Name:{test.owner_name}")
print(f"Balance:{test.get_balance()}")
print(test.interest_add())



#Decorators -- mainly take a functions then add their some more functionality then return it with new behaviours

def transaction_logger(func):  #receive the main function element and wrap it 


    def wrapper(self, amount):   

        print("The transaction started --- ")
        print(f"Account Holder: {self.owner_name}")
        print(f"Current Balance: ${self.get_balance()}")

        result = func(self, amount)  # is the main functiom 

        print(result)
        print(f"Updated Balance: ${self.get_balance()}")
        print("Transaction Completed successfully --- ")

        return result

    return wrapper
        

class EmergencyBank(Bankaccount):
    
    @transaction_logger
    def emergency_deposit(self,amount):
        return self.deposit(amount)
    
    @transaction_logger
    def emergency_withdraw(self,amount):
        return self.withdraw(amount)
    
emergency_user=EmergencyBank("Al Jaber Bhaiya",1234567,10000000)
emergency_user.emergency_deposit(20000000)
print()
emergency_user.emergency_withdraw(177)