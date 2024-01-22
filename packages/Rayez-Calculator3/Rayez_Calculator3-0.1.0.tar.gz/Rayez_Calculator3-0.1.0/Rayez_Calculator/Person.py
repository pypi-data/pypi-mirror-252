class Person:
    def __init__(self, _name, _age):
        self.name = _name
        self.age = _age

    def sayHi(self):
        print('Hello, my name is ' + self.name + ' and I am ' + str(self.age) + ' years old!')


class Vote_machine:
    def __init__(self):
        self.trump_vote_count = 0
        self.biden_vote_count = 0

    def vote_trump(self):
        self.trump_vote_count += 1
        self.vote_count()

    def vote_biden(self):
        self.biden_vote_count += 1
        self.vote_count()

    def give_info(self):
        print('the current candidates are X')
    
    def vote_count(self):
        print('Trump votes: ', str(self.trump_vote_count), 'Biden votes: ', str(self.biden_vote_count))


class Calculator:
    def __init__(self, num, num2):
        self.num = num
        self.num2 = num2

    def add(self):
        print(self.num + self.num2)
     
    def subtract(self):
        print(self.num - self.num2)

    def multiply(self):
        print(self.num * self.num2)

    def division(self):
        print(self.num / self.num2)



class SwordFighter:

    def __init__(self):
        self.name = 'SwordFighter'
        self.hp = 100
        self.attack = 50
        self.defense = 5
        self.speed = 20
        self.exp = 0
        self.level = 0


    def attack_target(self, target):
        target.hp -= self.attack
        print(target.hp)
        if target.hp <= 0:
            self.handle_exp(target)


    def increase_health(self):
        self.hp += 20
        print(self.hp)

    def handle_exp(self, target):
        if target.hp <= 0:
            self.exp += 100
        
        if self.exp >= 100:
            self.exp = 0
            self.level += 1
            self.level_up()

    def level_up(self):
        self.hp += 10
        self.attack += 5
        self.defense += 2
        self.speed += 5

    def print_character_stats(self):

        attributes = vars(self)
        print("Attribute values:")
        for attr, value in attributes.items():
            print(f"{attr}: {value}")



class EnemyMage:
    
    def __init__(self):
        self.hp = 50
        self.attack = 10
        self.defense = 5
        self.speed = 20

    def attack(self):
        pass

