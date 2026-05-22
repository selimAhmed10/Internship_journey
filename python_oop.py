#Class and the Object 

class Person:   #create class using the by class 
    species="Homo sapiens"  #class attribute
    
    #its mainly works for constructor. Uswed to initiliaze the object data 
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
    def __init__(self,owner_name,account_num,balance):
        self.owner_name=owner_name   #public
        self._account_num=account_num  #protected
        self.__balance=balance #private 
        
    def get_balance(self):   #for get the value of the private 
        return self.__balance
    
    def deposit(self,amount):  #normal a deposit method
        if amount>0:
            self.__balance +=amount
 
            return f"${amount} add so total : {self.__balance}"


account1=Bankaccount("selim",12343,1000)

print(f"Name: {account1.owner_name}")
print(f"Account: {account1._account_num}")
print(f"Balance: ${account1.get_balance()}")
print(account1.deposit(300))
print()



account1=Bankaccount("Al Jaber Bhaiea",12343,100000000000)

print(f"Name: {account1.owner_name}")
print(f"Account: {account1._account_num}")
print(f"Balance: ${account1.get_balance()}")
print(account1.deposit(99999999))
print()