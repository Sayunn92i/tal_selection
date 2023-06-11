import tools
import re

class Edit:
    def __init__(self, map):

        # Application et carte
        self.app = map.app
        self.map = map

        # Attributs
        self.edit_region = [0, 0, 0, 0]

        # Initialisation
        self.configuration()

    """
    Configuration de la classe.
    """
    def configuration(self):
        # Barre d'outils
        self.app.edit_button.config(command=self.activate)

        # Barre d'édition
        self.app.edit_type.trace_add("write", self.check_edit_type)
        self.app.edit_valid_button.config(command=self.validate)

    """
    Active l'outil d'édition.
    """
    def activate(self):
        # Barre d'outils
        self.app.move_button.config(state="normal")
        self.app.edit_button.config(state="disabled")

        # Barre d'édition
        self.app.editbar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Canevas
        self.app.canvas.bind("<ButtonPress-1>", self.start)
        self.app.canvas.bind("<B1-Motion>", lambda event: (self.move(event), self.map.update_latlon(event)))
        self.app.canvas.bind("<ButtonRelease-1>", self.end)
        self.app.canvas.config(cursor="crosshair")

    """
    Agrandit visuellement la zone d'édition.
    """
    def scale_up(self):
        self.app.canvas.scale("edit", 0, 0, 2, 2)
        

    """
    Rétrécit visuellement la zone d'édition.
    """
    def scale_down(self):
        self.app.canvas.scale("edit", 0, 0, 0.5, 0.5)

    """
    Initialise la zone d'édition au moment d'un clique gauche sur le canevas.
    """
    def start(self, event):
        # Point initial de la zone d'édition
        x, y = self.app.canvas.canvasx(event.x), self.app.canvas.canvasy(event.y)
        self.edit_region = [x, y, x, y]

        # Suppression de la zone d'édition précédente
        self.app.canvas.delete("edit")

    """
    Déplace la zone d'édition avec un maintien du clique gauche sur le canevas.
    """
    def move(self, event):
        # Point mouvant de la zone d'édition
        x, y = self.app.canvas.canvasx(event.x), self.app.canvas.canvasy(event.y)
        self.edit_region[2] = x
        self.edit_region[3] = y

        # Création ou modification de la zone d'édition
        if not self.app.canvas.find_withtag("edit"):
            self.app.canvas.create_rectangle(self.edit_region, fill="#3d9ccc", outline="#3588b2", stipple="gray25", tag="edit")
        else:
            self.app.canvas.coords("edit", self.edit_region)

        # Affichage des coordonnées de la zone d'édition
        x1, y1, x2, y2 = self.app.canvas.coords("edit")
        min_latitude, min_longitude = tools.pixels_to_latlon(self.map.tiles_size, self.map.zoom_level, x1, y2)
        max_latitude, max_longitude = tools.pixels_to_latlon(self.map.tiles_size, self.map.zoom_level, x2, y1)
        self.app.min_latitude_value.config(text=min_latitude)
        self.app.min_longitude_value.config(text=min_longitude)
        self.app.max_latitude_value.config(text=max_latitude)
        self.app.max_longitude_value.config(text=max_longitude)

    """
    Contrôle la zone d'édition après un relâchement du clique gauche sur le canevas.
    """
    def end(self, event):
        # Si c'est un seul point
        if self.edit_region[0] == self.edit_region[2] and self.edit_region[1] == self.edit_region[3]:
            self.app.min_latitude_value.config(text="")
            self.app.min_longitude_value.config(text="")
            self.app.max_latitude_value.config(text="")
            self.app.max_longitude_value.config(text="")

            # Désactivation du bouton de validation
            self.app.edit_valid_button.config(state="disabled")
        else:
            # Activation du bouton de validation
            self.app.edit_valid_button.config(state="normal")

    """
    Contrôle les changements de valeur sur le type d'édition.
    """
    def check_edit_type(self, *args):
        # Supression du bouton de remplacement de l'édition si vitesse en pourcentage
        if self.app.edit_type.get() == "Vitesse (%)":
            self.app.edit_is_offset.set(True)
            self.app.edit_replace_button.grid_remove()
            self.app.edit_add_button.grid(row=6, column=0)
        else:
            self.app.edit_replace_button.grid()
            self.app.edit_add_button.grid(row=6, column=1)

    """
    Valide les modifications de l'édition actuelle.
    """
    def validate(self):
            input_value = self.app.edit_input_value.get()
            numeric = "^[\-+]?[0-9]*\.?[0-9]+$"

            # On vérifie si la valeur en entrée est bien numérique
            if re.match(numeric, input_value):
                self.app.edit_input_value.config(bg="#ffffff")

                # On vérifie si la zone d'édition existe
                if self.app.canvas.find_withtag("edit"):

                    # Création d'une commande pour l'édition
                    step = self.app.timeline_step.get()
                    min_latitude = self.app.min_latitude_value.cget("text")
                    min_longitude = self.app.min_longitude_value.cget("text")
                    max_latitude = self.app.max_latitude_value.cget("text")
                    max_longitude = self.app.max_longitude_value.cget("text")
                    type = self.app.edit_type_list.get(self.app.edit_type.get())
                    is_offset = self.app.edit_is_offset.get()
                    input_value = self.app.edit_input_value.get()
                    command = [step, min_latitude, min_longitude, max_latitude, max_longitude, type, is_offset, input_value]

                    # On exécute la commande
                    self.map.history.execute(command)
            else:
                self.app.edit_input_value.config(bg="#ff7f7e")

    """
    Restaure les informations de l'édition.

    @param min_latitude: latitude minimale de la zone
    @param min_longitude: longitude minimale de la zone
    @param max_latitude: latitude maximale de la zone
    @param max_longitude: longitude maximale de la zone
    @param type: type de modification
    @param is_offset: True si ajout, False si remplacement
    @param input_value: valeur en entrée pour la modification
    """
    def restore(self, min_latitude, min_longitude, max_latitude, max_longitude, type, is_offset, input_value):
        if min_latitude and min_longitude and max_latitude and max_longitude:
            # Restauration des points
            x1, y1 = tools.latlon_to_pixels(self.map.tiles_size, self.map.zoom_level, min_latitude, max_longitude)
            x2, y2 = tools.latlon_to_pixels(self.map.tiles_size, self.map.zoom_level, max_latitude, min_longitude)
            self.edit_region = [x1, y1, x2, y2]

            # Création ou modification de la zone d'édition
            if not self.app.canvas.find_withtag("edit"):
                self.app.canvas.create_rectangle(self.edit_region, fill="#3d9ccc", outline="#3588b2", stipple="gray25", tag="edit")
            else:
                self.app.canvas.coords("edit", self.edit_region)

            # Activation du bouton de validation
            self.app.edit_valid_button.config(state="normal")
        else:
            # Suppression de la zone d'édition
            self.app.canvas.delete("edit")

            # Désactivation du bouton de validation
            self.app.edit_valid_button.config(state="disabled")

        # Affichage des coordonnées de la zone d'édition
        self.app.min_latitude_value.config(text=min_latitude)
        self.app.min_longitude_value.config(text=min_longitude)
        self.app.max_latitude_value.config(text=max_latitude)
        self.app.max_longitude_value.config(text=max_longitude)

        # Modification du type d'édition
        self.app.edit_type.set([k for k, v in self.app.edit_type_list.items() if v == type][0])

        # Modification de si l'édition est un remplacement ou un ajout
        self.app.edit_is_offset.set(is_offset)

        # Modification de la valeur en entrée
        self.app.edit_input_value.delete(0, "end")
        self.app.edit_input_value.insert(0, input_value)
