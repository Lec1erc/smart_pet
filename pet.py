import os
import inspect
import time
import pickle
import random

CURR_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PET_STATE = os.path.join(CURR_DIR, "pet_state.pkl")


class Pet:
    def __init__(self):
        self.name = ""
        self.health = 99
        self.happiness = 99
        self.hunger = 1
        self.sick = False
        self.last_update_time = time.time()

        self.load_state()
        self.update_stats()
        self.save_state()

    def stats(self):
        self.update_stats()
        print(f"\n{self.name}'s статус:")
        print(f"Здоровье: {self.health}")
        print(f"Счастье: {self.happiness}")
        print(f"Голод: {self.hunger}")
        if self.sick:
            print("Питомец болен")

    def update_stats(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time

        if not self.sick:
            self.health += int(time_elapsed * 0.01)
        else:
            self.health -= int(time_elapsed * 0.2)
        self.happiness -= int(time_elapsed * 0.01)
        self.hunger += int(time_elapsed * 0.01)

        self.health = max(0, min(self.health, 100))
        self.happiness = max(0, min(self.happiness, 100))
        self.hunger = max(0, min(self.hunger, 100))

        if random.random() < 0.1:
            self.handle_random_event()

        if self.health <= 0:
            print(f"{self.name} умер!")
            self.delete_pet_file()
            exit()

        self.last_update_time = current_time

    def handle_random_event(self):
        event_type = random.choice(["sickness", "bonus"])

        if self.hunger <= 0:
            self.health -= 10
            self.sick = True
            print(f"{self.name} заболел от переедания!")
        elif event_type == "sickness" and not self.sick:
            print(f"{self.name} заболел!")
            self.health -= 10
            self.sick = True
        elif event_type == "bonus":
            print(f"{self.name} получил бонус!")
            self.happiness += 15
            self.happiness = max(0, min(self.happiness, 100))

    def feed(self):
        self.hunger -= 10
        self.health += 5
        self.happiness += 5

    def play(self):
        self.hunger += 5
        self.health += 5
        self.happiness += 10

    def sleep(self):
        self.hunger += 5
        self.health += 10
        self.happiness += 5

    def heal(self):
        if self.sick:
            print("Питомец вылечен")
            self.sick = False
            self.health += 10
            self.happiness += 5
        else:
            print("Питомец не болен")

    @staticmethod
    def delete_pet_file(file_name=PET_STATE):
        try:
            os.remove(file_name)
        except FileNotFoundError:
            pass

    def save_state(self, file_name=PET_STATE):
        with open(file_name, 'wb') as file:
            pickle.dump(self.__dict__, file)

    def load_state(self, file_name=PET_STATE):
        try:
            with open(file_name, 'rb') as file:
                state = pickle.load(file)
                self.__dict__.update(state)
        except FileNotFoundError:
            print("Файл состояния не найден. Создан новый питомец.")
            pet_name = input("Введите имя своего питомца: ")
            self.name = pet_name
            self.save_state()


def start():
    pet = Pet()
    pet.load_state()

    while True:
        pet.update_stats()
        pet.stats()

        action = input("Выберите действие (кормить/играть/спать/лечить/состояние/выйти): ").lower()

        if action == "кормить":
            pet.feed()
        elif action == "играть":
            pet.play()
        elif action == "спать":
            pet.sleep()
        elif action == "лечить":
            pet.heal()
        elif action == "состояние":
            pet.stats()
        elif action == "выйти":
            pet.save_state()
            print("До свидания!")
            break
        else:
            print("Неверное действие. Попробуйте еще раз.")

        pet.save_state()
        time.sleep(1)
