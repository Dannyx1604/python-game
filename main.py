import random
from random import randint
import colorama
import os
import time
import speech_recognition as sr
import pyaudio as pa

colorama.init()

WHITE = colorama.Fore.WHITE
GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
BLUE = colorama.Fore.BLUE
YELLOW = colorama.Fore.YELLOW
CYAN = colorama.Fore.CYAN
CLEAR = colorama.Style.RESET_ALL


class Utils:
    def clear(self):
        return os.system('cls')  # os.system('clear') Linux / MacOS

    def go_on(self):
        input('Press Enter to continue')
        self.clear()

    def is_valid(self, other, data_range=''):
        if other is None:
            print('Input error. You provided a None value.')
            return False
        if len(other) == 0:
            print('Input error. You put in an empty string.')
            return False
        elif (other not in data_range and (data_range != '')) or (other == data_range):
            print(f'Input error. Please put in a number between {data_range[0]} and {data_range[-1]}.')
            return False
        else:
            return True

    def choose_action(self, text, action_numbers='123456'):
        while True:
            choice = self.speech_recognition()
            if self.is_valid(choice, action_numbers):
                break
        return choice

    def get_list_files(self):
        return os.listdir()

    def get_numbers_string(self, num):
        return ''.join(map(str, list(range(num))))

    def speech_recognition(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language='en-US')
                print(f"You said {text}")
                return text
            except sr.UnknownValueError:
                print("I didn't understand anything, please repeat what you said")
                self.speech_recognition()
            except sr.RequestError as e:
                print(f"There was an error while processing your request: \n {e}")


Utils = Utils()


class Person:
    def __init__(self):
        self.name = ''
        self._person_class = ''
        self.health = 0
        self.attack = 0
        self.defence = 0
        self.skills = {}
        self.is_alive = True
        self.max_health = 0

    def _set_class_properties(self):
        self.health = classes[self._person_class]['health']
        self.attack = classes[self._person_class]['attack']
        self.defence = classes[self._person_class]['defense']
        self.skills = classes[self._person_class]['skills']

    def attack_enemy(self, enemy1, enemy2):
        print(f"{enemy1.name} attacks {enemy2.name}!")
        time.sleep(2)

        if random.randint(0, 9) > 6:
            self.apply_skill(enemy2)

        damage = enemy1.attack - enemy2.defence
        if damage < 0: damage = 1
        enemy2.health -= damage

        print(f"{enemy1.name} deals {damage} damaga and {enemy2.name} has {enemy2.health} health left!")
        Utils.go_on()
        time.sleep(2)

    def fight_for_the_win(self, attacker, defender):
        while attacker.is_alive and defender.is_alive:
            time.sleep(2)

            if attacker.health > 0:
                self.attack_enemy(attacker, defender)
            else:
                print(f"{attacker.name} has lost!")
                attacker.is_alive = False
                return False

            if defender.health > 0:
                self.attack_enemy(defender, attacker)
            else:
                print(f"{defender.name} has lost!")
                defender.is_alive = False
                return True

    def apply_skill(self, target):
        skill = random.choice(list(target.skills.keys()))
        if target.health + target.skills[skill] < target.max_health:
            target.health += target.skills[skill]
            print(f"{BLUE}{target.name} applies the skill {GREEN}{skill}!{WHITE}")


class Player(Person):
    def __init__(self):
        super().__init__()
        self.__set_name()
        self.__set_person_class()
        self._set_class_properties()
        self.max_health = self.health

        self.money = float(random.randint(10, 500))
        self.inventory = Inventory(APPLE, SWORD)

        Utils.go_on()
        print(f"{self.name} - {self._person_class}.")
        print("(～￣▽￣)～ He has the following characteristics:")
        print(f"\t\t health - {self.health},\n\t\t attack - {self.attack},\n\t\t defense - {self.defence}.")
        Utils.go_on()

    def __set_name(self):
        while True:
            print(f'A long time ago, there was a brave hero called... (Say your name)')
            player_name = Utils.speech_recognition()
            if Utils.is_valid(player_name):
                break

        self.name = player_name

    def __set_person_class(self):
        while True:
            print(
                f"And he had a lot of talents ... (Say the number of the role he should have): 1-Fighter, 2-Archer, 3-Wizard")
            choice = Utils.speech_recognition()
            if Utils.is_valid(choice, '123'):
                break
        self._person_class = role[choice]

    def increase_money(self, value):
        self.money += value
        print(f"Earned {value} €. There is: {round(self.money, 2)} € left.")

    def decrease_money(self, value):
        if self.money - value < 0:
            print(f"The hero can't afford that. (˘･_･˘)")
            return False
        else:
            self.money -= value
            print(f"Used {value} €. There is: {self.money} € left.")
            return True

    def increase_health(self, value):
        random_hp = value
        if self.max_health > self.health + random_hp:
            self.health += random_hp
            print(f"{self.name} regenerated {random_hp} health (^_^)")
            Utils.go_on()
        else:
            self.health = self.max_health
            print(f"{self.name} has completely restores his health! ☜(ﾟヮﾟ☜)")
            Utils.go_on()

    def increase_xp(self):
        self.max_health += random.randint(1, 10)
        self.attack += random.randint(1, 10)
        self.defence += random.randint(1, 10)
        print(f"{self.name} has gained some experience. (～￣▽￣)～")


class Item:
    def __init__(self, name):
        self.type = ''
        self.name = name
        self.__value = 0

    def use(self):
        return self.__value

    def set(self, value):
        self.__value = value


class Food(Item):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'food'
        self.set(randint(5, 30))


class BuildItem(Item):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'build'
        self.set(randint(1, 10))


class AttackItem(Item):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'attack'
        self.set(randint(50, 100))


class DefendItem(Item):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'defend'
        self.set(randint(10, 50))


APPLE = Food('apple')

WOODEN = BuildItem('wood')

SWORD = AttackItem('sword')

SHIELD = DefendItem('shield')

ARROW = AttackItem('bow')

CHICKEN = Food('chicken')

HAMMER = BuildItem('hammer')

NAILS = BuildItem('nails')

BANANA = Food('banana')

ORANGE = Food('orange')

PEAR = Food('pear')

CARROT = Food('carrot')

POTATO = Food('potato')

TOMATO = Food('tomato')

PUMPKIN = Food('pumpkin')

ONION = Food('onion')

CABBAGE = Food('cabbage')

BREAD = Food('bread')

HELMET = DefendItem('helmet')

ARMOR = DefendItem('armor')

AXE = AttackItem('axe')

DAGGER = AttackItem('dagger')

SPEAR = AttackItem('spear')

CROSSBOW = AttackItem('crossbow')

POSSIBLE_ITEMS = (
    APPLE,
    SWORD,
    SHIELD,
    ARROW,
    CHICKEN,
    BREAD,
    CABBAGE,
    CARROT,
    ONION,
    PUMPKIN,
    TOMATO,
    POTATO,
    PEAR,
    ORANGE,
    NAILS,
    BANANA,
    WOODEN,
    ARMOR,
    HELMET,
    AXE,
    DAGGER,
    SPEAR,
    CROSSBOW,
)


class Inventory:
    def __init__(self, *items):
        self.__items = list(items)
        self.sort_inventory()

    def sort_inventory(self):
        self.__items = sorted(
            self.__items,
            key=lambda item: item.name
        )

    def add_item(self, item):
        self.__items.append(item)
        self.sort_inventory()
        print(f"{WHITE}Added {item} to the inventory")

    def remove_item(self, item):
        print(f"{WHITE}Took {item.name} out of the inventory")
        self.__items.remove(item)
        self.sort_inventory()

    def show_items(self):
        print(f'{CYAN}The inventory contains the following items: ')
        for i in range(len(self.__items)):
            print(f"{i + 1}. {self.__items[i].name}")
        print(WHITE)

    def get_item(self, item_index):
        return self.__items[item_index]


class Person:
    def __init__(self):
        self.name = ''
        self._person_class = ''
        self.health = 0
        self.attack = 0
        self.defence = 0
        self.skills = {}
        self.is_alive = True
        self.max_health = 0

    def _set_class_properties(self):
        self.health = classes[self._person_class]['health']
        self.attack = classes[self._person_class]['attack']
        self.defence = classes[self._person_class]['defense']
        self.skills = classes[self._person_class]['skills']

    def attack_enemy(self, enemy1, enemy2):
        print(f"{enemy1.name} attacks {enemy2.name}!")
        time.sleep(2)

        if random.randint(0, 9) > 6:
            self.apply_skill(enemy2)

        damage = enemy1.attack - enemy2.defence
        if damage < 0: damage = 1
        enemy2.health -= damage

        print(f"{enemy1.name} deals {damage} damage and {enemy2.name} has {enemy2.health} health left!")
        Utils.go_on()
        time.sleep(2)

    def fight_for_the_win(self, attacker, defender):
        while attacker.is_alive and defender.is_alive:
            time.sleep(2)

            if attacker.health > 0:
                self.attack_enemy(attacker, defender)
            else:
                print(f"{attacker.name} has lost!")
                attacker.is_alive = False
                return False

            if defender.health > 0:
                self.attack_enemy(defender, attacker)
            else:
                print(f"{defender.name} has lost!")
                defender.is_alive = False
                return True

    def apply_skill(self, target):
        skill = random.choice(list(target.skills.keys()))
        if target.health + target.skills[skill] < target.max_health:
            target.health += target.skills[skill]
            print(f"{BLUE}{target.name} applies skill {GREEN}{skill}!{WHITE}")


role = {
    '1': 'Fighter',
    '2': 'Archer',
    '3': 'Wizard',
}

classes = {
    'Fighter': {
        'health': 100,
        'attack': 50,
        'defense': 25,
        'skills': {
            'shield': 20
        }
    },
    'Archer': {
        'health': 70,
        'attack': 80,
        'defense': 15,
        'skills': {
            'runaway': 10
        }
    },
    'Wizard': {
        'health': 50,
        'attack': 90,
        'defense': 15,
        'skills': {
            'magic shield': 45,
            'healing': 20
        }
    }
}


class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.days = random.randint(100, 200)
        self.game_loop()

    def game_loop(self):
        while self.player.is_alive:
            Utils.clear()
            print(f"There are {self.days} days left! What should {self.player.name} do?")
            print(f"Health: {self.player.health}")

            for act in range(3):
                action = Utils.choose_action(
                    f"{self.player.name} wants to do: \n 1 - Go and meet friends; \n 2 - Hang around in the taverne; \n 3 - Sleep; \n 4 - Give up; \n 5 - Check out the family; \n 6 - Go and fight;"
                    "123456"
                )
                print(type(action))
                if action == '1':
                    pass
                elif action == '2':
                    pass
                elif action == '3':
                    pass
                elif action == '4':
                    pass
                elif action == '5':
                    pass
                elif action == '6':
                    pass

                if not self.player.is_alive:
                    pass


if __name__ == '__main__':
    game = Game()
