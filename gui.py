import tkinter as tk
from tkinter import ttk
from threading import Thread
import time


class PetGUI:
    def __init__(self, pet):
        self.pet = pet

        self.root = tk.Tk()
        self.root.title(self.pet.name)

        center_frame = tk.Frame(self.root)
        center_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.health_label = tk.Label(center_frame, text="Health:")
        self.health_label.grid(row=0, column=0, padx=10)
        self.health_progress = ttk.Progressbar(center_frame, orient="horizontal", length=200, mode="determinate")
        self.health_progress.grid(row=0, column=1, pady=10)

        self.happiness_label = tk.Label(center_frame, text="Happiness:")
        self.happiness_label.grid(row=1, column=0, padx=10)
        self.happiness_progress = ttk.Progressbar(center_frame, orient="horizontal", length=200, mode="determinate")
        self.happiness_progress.grid(row=1, column=1, pady=10)

        self.hunger_label = tk.Label(center_frame, text="Hunger:")
        self.hunger_label.grid(row=2, column=0, padx=10)
        self.hunger_progress = ttk.Progressbar(center_frame, orient="horizontal", length=200, mode="determinate")
        self.hunger_progress.grid(row=2, column=1, pady=10)

        self.status_label = tk.Label(center_frame, text="", font=("Helvetica", 12))
        self.status_label.grid(row=3, column=0, columnspan=2, pady=10)

        button_frame = tk.Frame(center_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=5)

        self.feed_button = tk.Button(button_frame, text="Feed", command=self.feed_pet)
        self.feed_button.pack(side=tk.LEFT, padx=5)

        self.play_button = tk.Button(button_frame, text="Play", command=self.play_pet)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.sleep_button = tk.Button(button_frame, text="Sleep", command=self.sleep_pet)
        self.sleep_button.pack(side=tk.LEFT, padx=5)

        self.heal_button = tk.Button(button_frame, text="Heal", command=self.heal_pet)
        self.heal_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(center_frame, text="Exit", command=self.exit_program)
        self.exit_button.grid(row=7, column=0, columnspan=2, pady=5)

        self.update_status_thread = Thread(target=self.update_status_thread)
        self.update_status_thread.start()

        self.root.mainloop()

    def update_status_thread(self):
        while True:
            time.sleep(1)
            self.pet.update_stats()
            self.show_status()

    def show_status(self):
        self.health_progress["value"] = self.pet.health
        self.happiness_progress["value"] = self.pet.happiness
        self.hunger_progress["value"] = self.pet.hunger

        self.health_label["text"] = f"Health: {int(self.pet.health)}"
        self.happiness_label["text"] = f"Happiness: {int(self.pet.happiness)}"
        self.hunger_label["text"] = f"Hunger: {int(self.pet.hunger)}"

        status_text = "Status: "
        if self.pet.sick:
            status_text += " |Sick| "
        if self.pet.hunger >= 90:
            status_text += " |Hungry| "
        if self.pet.happiness <= 10:
            status_text += " |Sad| "

        self.status_label.config(text=status_text)

    def feed_pet(self):
        self.pet.feed()

    def play_pet(self):
        self.pet.play()

    def sleep_pet(self):
        self.pet.sleep()

    def heal_pet(self):
        self.pet.heal()

    def exit_program(self):
        self.pet.save_state()
        self.root.destroy()


def start_gui(pet):
    pet.load_state()
    gui = PetGUI(pet)
