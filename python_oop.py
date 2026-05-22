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
        


