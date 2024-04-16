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
        self.health = 100
        self.happiness = 100
        self.hunger = 0
        self.sick = False
        self.last_update_time = time.time()

        self.load_state()
        self.update_stats()
        self.save_state()

    def stats(self, outer_call: bool = False):
        if outer_call:
            self.update_stats()
        print(f"\n{self.name}'s status:")
        print(f"Health: {self.health}")
        print(f"Happiness: {self.happiness}")
        print(f"Hunger: {self.hunger}")
        if self.sick:
            print(f"{self.name} is sick")
        if self.hunger >= 90:
            print(f"{self.name} is hungry")
        if self.happiness <= 10:
            print(f"{self.name} is sad")

    def update_stats(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time
        negative_factor = 0.0
        if self.sick:
            negative_factor += 0.03
        if self.hunger >= 90:
            negative_factor += 0.02
        if self.happiness <= 10:
            negative_factor += 0.02

        self.happiness -= time_elapsed * 0.01
        self.hunger += time_elapsed * 0.01
        if negative_factor > 0:
            self.health -= time_elapsed * negative_factor
        else:
            self.health += time_elapsed * 0.05

        self.health = max(0, min(self.health, 100))
        self.happiness = max(0, min(self.happiness, 100))
        self.hunger = max(0, min(self.hunger, 100))

        if random.random() < 0.01:
            self.handle_random_event()

        if self.health <= 0:
            print(f"{self.name} dead!")
            self.delete_pet_file()
            exit()

        self.last_update_time = current_time

    def handle_random_event(self):
        event_type = random.choice(["sickness", "bonus"])

        if event_type == "sickness" and not self.sick:
            print(f"{self.name} is sick!")
            self.health -= 10
            self.sick = True
        elif event_type == "bonus":
            print(f"{self.name} got a bonus!")
            # self.happiness += 15
            # self.happiness = max(0, min(self.happiness, 100))

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
            print("Pet cured")
            self.sick = False
            self.health += 10
            self.happiness += 5
        else:
            print("Pet is not sick")

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
            print("Status file not found. New pet created.")
            pet_name = input("What is your pet's name: ")
            self.name = pet_name
            self.save_state()


def start():
    pet = Pet()
    pet.load_state()

    while True:
        pet.update_stats()
        pet.stats()

        action = input("Choose action (feed/play/sleep/heal/status/exit): ").lower()

        if action == "feed":
            pet.feed()
        elif action == "play":
            pet.play()
        elif action == "sleep":
            pet.sleep()
        elif action == "heal":
            pet.heal()
        elif action == "status":
            pet.stats(True)
        elif action == "exit":
            pet.save_state()
            print("Bye!")
            break
        else:
            print("Wrong action. Please try again.")

        pet.save_state()
        time.sleep(1)
