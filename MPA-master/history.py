import tools
import shutil
import subprocess
from pathlib import Path
from tkinter import filedialog as fd, messagebox as mb

class History:
    def __init__(self, map):

        # Application et carte
        self.app = map.app
        self.map = map

        # Attributs
        self.temp_file_path = None
        self.temp_data_u = None
        self.temp_data_v = None
        self.position = None
        self.save_position = None
        self.history = None

        # Initialisation
        self.configuration()

        # Évènements
        self.app.history_list.bind("<<ListboxSelect>>", self.select)

    """
    Configuration de la classe.
    """
    def configuration(self):
        self.app.save_button.config(command=self.save)
        self.app.save_as_button.config(command=self.save_as)
        self.app.undo_button.config(command=self.undo)
        self.app.redo_button.config(command=self.redo)
        self.app.history_button.config(command=self.activate)
        self.app.history_close_button.config(command=self.deactivate)

    """
    Active la barre d'historique.
    """
    def activate(self):
       # Barre d'outils
       self.app.history_button.config(state="disabled")

       # Barre d'historique
       self.app.historybar.grid(row=0, column=2, rowspan=2, sticky="nsew")

    """
    Désactive la barre d'historique.
    """
    def deactivate(self):
       # Barre d'outils
       self.app.history_button.config(state="normal")

       # Barre d'historique
       self.app.historybar.grid_remove()

    """
    Initialise l'historisation.
    """
    def set(self):
        # Obtention du dossier temporaire
        temp_path = Path(__file__).parent.absolute() / "temp"
        temp_path.mkdir(parents=True, exist_ok=True)

        # Suppression du fichier temporaire précédent
        for path in temp_path.iterdir():
            if path.is_file():
                path.unlink()

        # Ajout du fichier temporaire
        suffix = self.map.grib.file_path.suffix
        self.temp_file_path = temp_path / f"file{suffix}"
        shutil.copy(self.map.grib.file_path, self.temp_file_path)

        # Ajout des composantes u et v temporaires
        self.temp_data_u = self.map.grib.data_u.copy()
        self.temp_data_v = self.map.grib.data_v.copy()

        # Réinitialisation de l'historisation
        self.position = 0
        self.save_position = 0
        self.history = [[]]

        # Désactivation des boutons de sauvegarde, annulation, restauration, validation
        self.app.save_button.config(state="disabled")
        self.app.undo_button.config(state="disabled")
        self.app.redo_button.config(state="disabled")
        self.app.edit_valid_button.config(state="disabled")

        # Premier élément dans l'historique
        self.app.history_list.insert(self.position, "[ Fichier de base ]")

        # Mise à jour de la position dans la liste de l'historique
        self.app.history_list.selection_set(self.position)

    """
    Nettoie l'historisation.
    """
    def unset(self):
        self.temp_file_path = None
        self.temp_data_u = None
        self.temp_data_v = None
        self.position = None
        self.save_position = None
        self.history = None
        self.app.history_list.delete(0, "end")

    """
    Écrit dans un fichier les éditions effectuées.
    """
    def write(self, destination_path):
        # On copie le fichier temporaire vers un chemin destination
        shutil.copy(self.temp_file_path, destination_path)

        # On exécute toutes les éditions sur le fichier
        api_path = Path(__file__).parent.absolute() / "api" / "prog"
        for i in range(1, self.position + 1):
            date, time = tools.datetime64_to_params(self.map.grib.data_time + self.map.grib.data_step[self.history[i][0]])
            min_latitude = str(self.history[i][1])
            min_longitude = str(self.history[i][2])
            max_latitude = str(self.history[i][3])
            max_longitude = str(self.history[i][4])
            type = self.history[i][5]
            is_offset = str(self.history[i][6])
            input_value = self.history[i][7]

            subprocess.run([api_path, destination_path, date, time, min_latitude, min_longitude, max_latitude, max_longitude, type, is_offset, input_value])

    """
    Sauvegarde l'édition.
    """
    def save(self):
        if self.save_position != self.position:
            # Changement de position de sauvegarde
            self.save_position = self.position

            # Écriture dans le fichier
            self.write(self.map.grib.file_path)

            # Suppression de l'astérisque de modification
            self.app.title(self.map.grib.file_path.name)

            # Désactivation du bouton de sauvegarde
            self.app.save_button.config(state="disabled")

    """
    Sauvegarde l'édition sous un autre fichier.
    """
    def save_as(self):
        # Navigateur de fichiers
        file_types = [("GRIB file", ".gb .grb .grib .gb2 .grb2 .grib2")]
        file_path = fd.asksaveasfilename(title="Enregistrer sous", filetypes=file_types, initialfile=self.map.grib.file_path.name)

        if file_path:
            # Ecriture dans le fichier
            self.write(file_path)

            # Ouverture du fichier
            self.map.grib.open(file_path)

    """
    Affiche une popup de sauvegarde et retourne la réponse.

    @return: True si "Oui", False si "Non", None si "Annuler"
    """
    def save_popup(self):
        # La réponse par défaut est "Non"
        answer = False

        if self.save_position != self.position:
            # Popup
            answer = mb.askyesnocancel("Sauvegarder", f"Sauvegarder le fichier \"{self.map.grib.file_path.name}\" ?")
            if answer:
                self.save()

        return answer

    """
    Charge divers éléments liés à l'historisation suite à un changement de position.

    @param from_start: True si on re-dessine les barbules depuis le début de l'historisation, False sinon
    """
    def load(self, from_start):
        # Gestion du nom du fichier et de l'état du bouton de sauvegarde
        if self.save_position == self.position:
            self.app.title(self.map.grib.file_path.name)
            self.app.save_button.config(state="disabled")
        else:
            self.app.title(f"*{self.map.grib.file_path.name}")
            self.app.save_button.config(state="normal")

        # Gestion de l'état du bouton annuler
        if self.position == 0:
            self.app.undo_button.config(state="disabled")
        else:
            self.app.undo_button.config(state="normal")

        # Gestion de l'état du bouton restaurer
        if self.position + 1 == len(self.history):
            self.app.redo_button.config(state="disabled")
        else:
            self.app.redo_button.config(state="normal")

        # Mise à jour du pas de la ligne temporelle et restauration de l'édition
        if self.position > 0:
            self.app.timeline.set(self.history[self.position][0])
            self.map.grib.update_datetime(self.history[self.position][0])
            self.map.edit.restore(*self.history[self.position][1:])
        else:
            self.app.timeline.set(0)
            self.map.grib.update_datetime(0)
            self.map.edit.restore("", "", "", "", "VAL_ANGLE", False, "")
        self.map.grib.update_step(None)

        if from_start:
            # Réinitialisation des composantes u et v
            self.map.grib.data_u = self.temp_data_u.copy()
            self.map.grib.data_v = self.temp_data_v.copy()

            # Suppression des images
            self.app.canvas.delete("barb")
            self.map.grib.barbs_ref = {}

            # Re-dessine les barbules depuis le début de l'historisation
            for i in range(1, self.position + 1):
                self.map.grib.update_barbs(*self.history[i])
        else:
            # Re-dessine les barbules pour la position actuelle
            self.map.grib.update_barbs(*self.history[self.position])

        # Mise à jour de la position dans la liste de l'historique
        self.app.history_list.selection_clear(0, "end")
        self.app.history_list.selection_set(self.position)

        # Ce qui se trouve au dessus de la position dans la liste de l'historique est grisé
        for i in range (1, len(self.history)):
            if i > self.position:
                self.app.history_list.itemconfig(i, bg="#a6b8c2")
            else:
                self.app.history_list.itemconfig(i, bg="")

    """
    Annule l'édition.
    """
    def undo(self):
        if self.position > 0:
            # Changement de position
            self.position -= 1
            self.load(True)

    """
    Restaure l'édition.
    """
    def redo(self):
        if self.position + 1 < len(self.history):
            # Changement de position
            self.position += 1
            self.load(False)

    """
    Lance une édition.
    """
    def execute(self, command):
        # Changement de position
        self.position += 1

        if len(self.history) == self.position:
            # Nouvelle édition
            self.history.append(command)
            self.app.history_list.insert("end", f"{self.app.edit_is_offset_icons.get(command[6])} {self.app.edit_type.get()} {command[7]}")
        else:
            # Nouvelle édition mais écrase ce qui se trouve après la position
            self.history = self.history[:self.position + 1]
            self.history[self.position] = command
            self.app.history_list.delete(self.position, "end")
            self.app.history_list.insert(self.position, f"{self.app.edit_is_offset_icons.get(command[6])} {self.app.edit_type.get()} {command[7]}")

        self.load(False)

    """
    Change la position dans l'historique.
    """
    def select(self, event):
        # Changement de position
        self.position = self.app.history_list.curselection()[0]
        self.load(True)
