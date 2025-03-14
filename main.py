# Datei: main.py
# Beschreibung: Die Haupt-GUI für die Game Achievement Tracker Anwendung.

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QListWidget, QFileDialog, QInputDialog
from PyQt6.QtCore import Qt
import sys
import json
import csv
from achievements import add_achievement, get_all_achievements, remove_achievement, update_achievement

class AchievementTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Achievement Tracker")  # Setzt den Fenstertitel
        self.setGeometry(200, 200, 800, 600)  # Setzt die Fenstergröße und Position

        # Hauptlayout für die GUI
        layout = QVBoxLayout()

        # Begrüßungstext für die App
        label = QLabel("Willkommen zum Game Achievement Tracker!")
        layout.addWidget(label)

        # Button, um ein Achievement hinzuzufügen
        self.add_button = QPushButton("Add Achievement")
        self.add_button.clicked.connect(self.add_achievement)
        layout.addWidget(self.add_button)

        # Button, um das ausgewählte Achievement zu bearbeiten
        self.edit_button = QPushButton("Edit Achievement")
        self.edit_button.clicked.connect(self.edit_achievement)
        layout.addWidget(self.edit_button)

        # Button, um das ausgewählte Achievement zu löschen
        self.delete_button = QPushButton("Delete Achievement")
        self.delete_button.clicked.connect(self.delete_achievement)
        layout.addWidget(self.delete_button)

        # Button, um Achievements aus einer externen Datei zu importieren
        self.import_button = QPushButton("Import Achievements")
        self.import_button.clicked.connect(self.import_achievements)
        layout.addWidget(self.import_button)

        # Liste der Achievements anzeigen
        self.achievements_list = QListWidget()
        layout.addWidget(self.achievements_list)

        # Zentrales Widget mit Layout setzen
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Alle Achievements laden und anzeigen
        self.load_achievements()

    def add_achievement(self):
        # Hier fügen wir ein Beispiel-Achievement hinzu
        add_achievement("First Achievement", "Dies ist dein erstes Achievement!")
        self.load_achievements()

    def edit_achievement(self):
        # Das ausgewählte Achievement abrufen
        selected_item = self.achievements_list.currentItem()
        if selected_item:
            current_name, current_description = selected_item.text().split(": ", 1)

            # Neues Achievement bearbeiten (Name und Beschreibung)
            new_name, ok = QInputDialog.getText(self, "Edit Achievement", "Enter new name:", text=current_name)
            if ok:
                new_description, ok = QInputDialog.getText(self, "Edit Achievement", "Enter new description:", text=current_description)
                if ok:
                    update_achievement(current_name, new_name, new_description)
                    self.load_achievements()

    def delete_achievement(self):
        # Das ausgewählte Achievement löschen
        selected_item = self.achievements_list.currentItem()
        if selected_item:
            achievement_name = selected_item.text().split(": ", 1)[0]
            remove_achievement(achievement_name)
            self.load_achievements()

    def load_achievements(self):
        # Alle Achievements laden und in der ListBox anzeigen
        achievements = get_all_achievements()
        self.achievements_list.clear()  # Liste zuerst leeren
        for achievement in achievements:
            self.achievements_list.addItem(f"{achievement['name']}: {achievement['description']}")

    def import_achievements(self):
        # Datei öffnen, um Achievements zu importieren
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Achievements File", "", "CSV Files (*.csv);;JSON Files (*.json)")

        if file_path:
            if file_path.endswith(".csv"):
                self.import_from_csv(file_path)
            elif file_path.endswith(".json"):
                self.import_from_json(file_path)

    def import_from_csv(self, file_path):
        # Achievements aus einer CSV-Datei importieren
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:  # Sicherstellen, dass die Zeile 2 Spalten hat (Name und Beschreibung)
                    add_achievement(row[0], row[1])
        self.load_achievements()

    def import_from_json(self, file_path):
        # Achievements aus einer JSON-Datei importieren
        with open(file_path, mode='r') as file:
            achievements = json.load(file)
            for achievement in achievements:
                if "name" in achievement and "description" in achievement:
                    add_achievement(achievement["name"], achievement["description"])
        self.load_achievements()

# Funktion zum Laden des Stylesheets für ein modernes Design
def load_stylesheet():
    with open("styles.qss", "r") as f:
        return f.read()

# Startpunkt der Anwendung
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())  # Wendet das Dark Theme aus styles.qss an
    window = AchievementTracker()
    window.show()
    sys.exit(app.exec())
