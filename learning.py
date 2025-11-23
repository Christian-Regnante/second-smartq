class Car:

    def __init__(self, name, brand, engine, owner):
        self.name = name
        self.brand = brand
        self.engine = engine
        self.owner = owner

    
    def buy(self):
        return f"Owner {self.owner} is selling a car with this specs: ( car_name => {self.name}, Brannd => {self.brand}, and Engine => {self.engine} )"
    

Car1 = Car("AMG", "Mercedes", "Turbo_V8 Engine", "Semana")
Car2 = Car("Corosta BMW", "BMW", "Turbo_V6 Engine", "Gilbert")
Car3 = Car("VS60 Model", "Aston Maltin", "ASton_turbo Jet", "Christian")

print(Car1.buy())
print(Car2.buy())
print(Car3.buy())