#defining the class for the first Time
class car:
    def __init__(self,brand,model):#init is the constructor
        self.brand=brand
        self.model=model

    def fullname(self):#addition of method to display full name
        return f"{self.brand} {self.model}"
'''now defining an inherited class which is electric car class this
is called inheritence'''

class electric_car:
    def __init__(self,brand,model,battery_size):#self is just for connecting 
        super().__init__(brand,model)  #inhereting the brand and model from the class of cars
        self.battery_size=battery_size
    
    def fueltype(self):
        return "this is electric type fuel"
    




'''my_car=car("maruti","suzuki")
print(my_car.brand)       #printing individual values or accessing it
print(my_car.model)
#now priting full name
print(my_car.fullname()) '''#to display the full name with proper spacing and to print any method

myelectriccar=electric_car("hero","moto","85 kwh")
'''print(myelectriccar.brand)
print(myelectriccar.model)
print(myelectriccar.battery_size)
print(myelectriccar.fullname())
print(myelectriccar.fueltype())'''
