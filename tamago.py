import streamlit as st
import time
import random
import pickle
import os

STATE_FILE = "tamagotchi_state.pkl"

class Tamagotchi:
    def __init__(self, name):
        self.name = name
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.age = 0
        self.is_alive = True
        self.is_dark_mode = False
        self.load_state()

    def get_face(self):
        if not self.is_alive:
            return "💀 (x_x)"
        if self.is_dark_mode:
            return "☠️ (>_<)"
        elif self.hunger < 30 or self.happiness < 30 or self.energy < 30:
            return "😢 (；一_一)"
        elif self.hunger > 70 and self.happiness > 70 and self.energy > 70:
            return "😄 (•‿•)"
        elif self.age > 30:
            return "😎 (⌐■_■)"
        else:
            return "🙂 (•_•)"

    def feed(self):
        if not self.is_alive: return
        self.hunger = min(100, self.hunger + 20)

    def play(self):
        if not self.is_alive or self.energy < 20: return
        self.happiness = min(100, self.happiness + 20)
        self.energy = max(0, self.energy - 20)

    def sleep(self):
        if not self.is_alive: return
        self.energy = min(100, self.energy + 30)

    def decay(self):
        self.age += 1
        if self.age % 5 == 0:
            self.hunger = max(0, self.hunger - 5)
            self.happiness = max(0, self.happiness - 5)
            self.energy = max(0, self.energy - 5)

        if self.hunger == 0 or self.happiness == 0 or self.energy == 0:
            self.is_alive = False

    def random_event(self):
        if random.random() < 0.3:
            events = [
                ("Found a shiny rock 🪨", "happiness", +10),
                ("Existential crisis 😵", "happiness", -15),
                ("Chased a butterfly 🦋", "happiness", +5),
                ("Ate a rotten pixel 🤢", "hunger", -10),
                ("Listened to dissonant jazz 🎷", "energy", -5),
                ("Had a beautiful dream 🌈", "happiness", +15),
                ("Read Kant 📖", "energy", -15),
                ("Watched Matrix 🕶️", "happiness", -10),
            ]
            event = random.choice(events)
            attr = event[1]
            delta = event[2]
            setattr(self, attr, max(0, min(100, getattr(self, attr) + delta)))
            if not self.is_dark_mode and random.random() < 0.01:
                self.is_dark_mode = True
            return event[0]
        return None

    def save_state(self):
        with open(STATE_FILE, "wb") as f:
            pickle.dump(self.__dict__, f)

    def load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "rb") as f:
                state = pickle.load(f)
                self.__dict__.update(state)

# Streamlit app
if "pet" not in st.session_state:
    name = st.text_input("Name your Tamagotchi", "")
    if name:
        st.session_state.pet = Tamagotchi(name)
        st.experimental_rerun()
else:
    pet = st.session_state.pet

    st.title(f"Tamagotchi - {pet.name}")
    st.markdown(f"### {pet.get_face()}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Hunger", f"{pet.hunger}/100")
    col2.metric("Happiness", f"{pet.happiness}/100")
    col3.metric("Energy", f"{pet.energy}/100")
    st.markdown(f"**Age:** {pet.age}")

    if not pet.is_alive:
        st.error(f"{pet.name} has passed away. 💀 Game over.")
    else:
        if st.button("🍗 Feed"):
            pet.feed()
        if st.button("🎾 Play"):
            pet.play()
        if st.button("💤 Nap"):
            pet.sleep()
        if st.button("⏩ Time passes"):
            pet.decay()
            event = pet.random_event()
            if event:
                st.info(f"Random Event: {event}")

        pet.decay()
        pet.save_state()
