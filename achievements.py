# Datei: achievements.py
# Beschreibung: Diese Datei verwaltet das Speichern und Laden von Achievements.

import json
import os

# Pfad zur JSON-Datei, in der Achievements gespeichert werden
ACHIEVEMENTS_FILE = "data/achievements.json"

# Sicherstellen, dass die JSON-Datei existiert, andernfalls erstellen
if not os.path.exists(ACHIEVEMENTS_FILE):
    with open(ACHIEVEMENTS_FILE, "w") as f:
        json.dump([], f)

# Funktion zum Laden der Achievements aus der JSON-Datei
def load_achievements():
    with open(ACHIEVEMENTS_FILE, "r") as f:
        return json.load(f)

# Funktion zum Hinzufügen eines neuen Achievements
def add_achievement(name, description):
    achievements = load_achievements()  # Alle bisherigen Achievements laden
    achievement = {"name": name, "description": description}
    achievements.append(achievement)  # Neues Achievement hinzufügen

    # Achievements wieder in die JSON-Datei speichern
    with open(ACHIEVEMENTS_FILE, "w") as f:
        json.dump(achievements, f)

# Funktion zum Anzeigen aller Achievements
def get_all_achievements():
    return load_achievements()

# Funktion zum Entfernen eines Achievements
def remove_achievement(name):
    achievements = load_achievements()  # Alle bisherigen Achievements laden
    achievements = [a for a in achievements if a["name"] != name]  # Achievement mit dem angegebenen Namen entfernen

    # Achievements wieder in die JSON-Datei speichern
    with open(ACHIEVEMENTS_FILE, "w") as f:
        json.dump(achievements, f)

# Funktion zum Aktualisieren eines Achievements
def update_achievement(old_name, new_name, new_description):
    achievements = load_achievements()  # Alle bisherigen Achievements laden
    for achievement in achievements:
        if achievement["name"] == old_name:
            achievement["name"] = new_name
            achievement["description"] = new_description
            break

    # Achievements wieder in die JSON-Datei speichern
    with open(ACHIEVEMENTS_FILE, "w") as f:
        json.dump(achievements, f)
