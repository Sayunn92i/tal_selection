import tkinter as tk
from map import Map
from pathlib import Path
from PIL import Image, ImageTk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Attributs
        self.file_menu = None
        self.grib_icon_image = None
        self.geojson_icon_image = None
        self.save_icon_image = None
        self.save_as_icon_image = None
        self.move_icon_image = None
        self.edit_icon_image = None
        self.undo_icon_image = None
        self.redo_icon_image = None
        self.history_icon_image = None
        self.grib_button = None
        self.geojson_button = None
        self.save_button = None
        self.save_as_button = None
        self.move_button = None
        self.edit_button = None
        self.undo_button = None
        self.redo_button = None
        self.history_button = None
        self.canvas = None
        self.editbar = None
        self.min_latitude_value = None
        self.min_longitude_value = None
        self.max_latitude_value = None
        self.max_longitude_value = None
            
        self.edit_type_list = None
        self.edit_type = None

        self.edit_rect_button = None
        self.edit_oval_button = None
        self.edit_mouse_button = None
        self.edit_selection_type = None

        self.edit_input_value = None
        self.edit_is_offset_icons = None
        self.edit_is_offset = None
        self.edit_replace_button = None
        self.edit_add_button = None
        self.edit_valid_button = None
        self.datetime = None
        self.coordinates = None
        self.historybar = None
        self.history_list = None
        self.history_close_button = None
        self.timeline_step = None
        self.timeline = None

        # Initialisation
        self.configuration()
        self.init_menu()
        self.init_toolbar()
        self.init_canvas()
        self.init_editbar()
        self.init_datetime()
        self.init_coordinates()
        self.init_historybar()
        self.init_timeline()

        # Fonctionnalités
        self.map = Map(self)

    """
    Configuration de la fenêtre Tkinter.
    """
    def configuration(self):
        self.title("Éditeur de vents marins")
        self.geometry("854x480")
        self.minsize(854, 480)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    """
    Création du menu.
    """
    def init_menu(self):
        menu = tk.Menu(self)
        self.file_menu = tk.Menu(menu, tearoff=False)

        # Actions du sous-menu fichier
        self.file_menu.add_command(label="Ouvrir GRIB...")
        self.file_menu.add_command(label="Ouvrir GeoJSON...")
        self.file_menu.add_command(label="Fermer GRIB", state="disabled")
        self.file_menu.add_command(label="Fermer GeoJSON", state="disabled")
        self.file_menu.add_command(label="Quitter", command=self.destroy)

        # Actions du menu
        menu.add_cascade(label="Fichier", menu=self.file_menu)

        # Ajout du menu
        self.config(menu=menu)

    """
    Création de la barre d'outils.
    """
    def init_toolbar(self):
        toolbar = tk.Frame(self, bg="#85caf2", padx=10, pady=10)
        toolbar.grid(row=0, column=0, sticky="ew")

        # Bouton du fichier GRIB
        grib_icon_open = Image.open(Path(__file__).parent.absolute() / "images" / "icons" / "grib_open.png").resize((32,32))
        self.grib_icon_image = ImageTk.PhotoImage(grib_icon_open)
        self.grib_button = tk.Button(toolbar, activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0, image=self.grib_icon_image)
        self.grib_button.grid(row=0, column=0, padx=(0, 10), ipadx=5, ipady=5)

        # Bouton du fichier GeoJSON
        geojson_icon_open = Image.open(Path(__file__).parent.absolute() / "images" / "icons" / "geojson_open.png").resize((32,32))
        self.geojson_icon_image = ImageTk.PhotoImage(geojson_icon_open)
        self.geojson_button = tk.Button(toolbar, activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0, image=self.geojson_icon_image)
        self.geojson_button.grid(row=0, column=1, padx=(0, 10), ipadx=5, ipady=5)

        # Bouton enregistrer
        save_icon_open = Image.open(Path(__file__).parent.absolute() / "images" / "icons" / "save.png").resize((32,32))
        self.save_icon_image = ImageTk.PhotoImage(save_icon_open)
        self.save_button = tk.Button(toolbar, activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0, image=self.save_icon_image)

        # Bouton enregistrer sous...
        save_as_icon_open = Image.open(Path(__file__).parent.absolute() / "images" / "icons" / "save_as.png").resize((32,32))
        self.save_as_icon_image = ImageTk.PhotoImage(save_as_icon_open)
        self.save_as_button = tk.Button(toolbar, activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0, image=self.save_as_icon_image)

        # Bouton de déplacement
        move_icon_open = Image.open(Path(__file__).parent.absolute() / "images" / "icons" / "move.png").resize((32,32))
        self.move_icon_image = ImageTk.PhotoImage(move_icon_open)
        self.move_button = tk.Button(toolbar, activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0, image=self.move_icon_image)

        # Bouton d'édition
        edit_icon_open = Image.open(Path(__file__).parent.absolute() / "images" / "icons" / "edit.png").resize((32,32))
        self.edit_icon_image = ImageTk.PhotoImage(edit_icon_open)
        self.edit_button = tk.Button(toolbar, activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0, image=self.edit_icon_image)

        # Bouton annuler
        undo_icon_open = Image.open(Path(__file__).parent.absolute() / "images" / "icons" / "undo.png").resize((32,32))
        self.undo_icon_image = ImageTk.PhotoImage(undo_icon_open)
        self.undo_button = tk.Button(toolbar, activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0, image=self.undo_icon_image)

        # Bouton refaire
        redo_icon_open = Image.open(Path(__file__).parent.absolute() / "images" / "icons" / "redo.png").resize((32,32))
        self.redo_icon_image = ImageTk.PhotoImage(redo_icon_open)
        self.redo_button = tk.Button(toolbar, activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0, image=self.redo_icon_image)

        # Bouton historique
        history_icon_open = Image.open(Path(__file__).parent.absolute() / "images" / "icons" / "history.png").resize((32,32))
        self.history_icon_image = ImageTk.PhotoImage(history_icon_open)
        self.history_button = tk.Button(toolbar, activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0, image=self.history_icon_image)

    """
    Création du canevas.
    """
    def init_canvas(self):
        self.canvas = tk.Canvas(self, bg="#ffffff", highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.rowconfigure(1, weight=1)
        self.canvas.columnconfigure(1, weight=1)

    """
    Création de la barre d'édition.
    """
    def init_editbar(self):
        self.editbar = tk.Frame(self.canvas, bg="#a6b8c2", cursor="arrow", padx=10, pady=10)
        self.editbar.rowconfigure(10, weight=1)
        self.editbar.columnconfigure(0, weight=1, uniform="column")
        self.editbar.columnconfigure(1, weight=1, uniform="column")

        self.edit_selection_type = tk.StringVar(value="rect")
        select_label = tk.Label(self.editbar, bd=0, bg="#a6b8c2", text="Selection :")
        select_label.grid(row=0, column=0, sticky="w", ipadx=5, ipady=5)

        # Bouton de selection rectangulaire de l'édition
        self.edit_rect_button = tk.Radiobutton(self.editbar, activebackground="#a6b8c2", bd=0, bg="#a6b8c2", highlightthickness=0, text="Rectangle",value="rect",variable=self.edit_selection_type)
        self.edit_rect_button.grid(row=1, column=0, sticky="w", pady=(0, 10), ipadx=5, ipady=5)

        # Bouton de selection circulaire de l'édition
        self.edit_oval_button = tk.Radiobutton(self.editbar, activebackground="#a6b8c2", bd=0, bg="#a6b8c2", highlightthickness=0, text="Ellipse",value="oval",variable=self.edit_selection_type)
        self.edit_oval_button.grid(row=1, column=1, sticky="w", pady=(0, 10), ipadx=5, ipady=5)

        # Bouton de selection avec la souris de l'édition
        self.edit_mouse_button = tk.Radiobutton(self.editbar, activebackground="#a6b8c2", bd=0, bg="#a6b8c2", highlightthickness=0, text="Souris",value="mouse",variable=self.edit_selection_type)
        self.edit_mouse_button.grid(row=2, column=0, sticky="w", pady=(0, 10), ipadx=5, ipady=5)

 

        # Affichage de la latitude minimale
        min_latitude_label = tk.Label(self.editbar, bd=0, bg="#a6b8c2", text="Min latitude :")
        min_latitude_label.grid(row=3, column=0, sticky="w", ipadx=5, ipady=5)
        self.min_latitude_value = tk.Label(self.editbar, bd=0, bg="#a6b8c2")
        self.min_latitude_value.grid(row=3, column=1, sticky="w", ipadx=5, ipady=5)

        # Affichage de la longitude minimale
        min_longitude_label = tk.Label(self.editbar, bd=0, bg="#a6b8c2", text="Min longitude :")
        min_longitude_label.grid(row=4, column=0, sticky="w", ipadx=5, ipady=5)
        self.min_longitude_value = tk.Label(self.editbar, bd=0, bg="#a6b8c2")
        self.min_longitude_value.grid(row=4, column=1, sticky="w", ipadx=5, ipady=5)

        # Affichage de la latitude maximale
        max_latitude_label = tk.Label(self.editbar, bd=0, bg="#a6b8c2", text="Max latitude :")
        max_latitude_label.grid(row=5, column=0, sticky="w", ipadx=5, ipady=5)
        self.max_latitude_value = tk.Label(self.editbar, bd=0, bg="#a6b8c2")
        self.max_latitude_value.grid(row=5, column=1, sticky="w", ipadx=5, ipady=5)

        # Affichage de la longitude maximale
        max_longitude_label = tk.Label(self.editbar, bd=0, bg="#a6b8c2", text="Max longitude :")
        max_longitude_label.grid(row=6, column=0, sticky="w", pady=(0, 10), ipadx=5, ipady=5)
        self.max_longitude_value = tk.Label(self.editbar, bd=0, bg="#a6b8c2")
        self.max_longitude_value.grid(row=6, column=1, sticky="w", pady=(0, 10), ipadx=5, ipady=5)

        # On conserve le type d'édition
        self.edit_type_list = {
            "Angle (°)" : "VAL_ANGLE",
            "Vitesse (nd)" : "VAL_SPEED",
            "Vitesse (%)" : "VAL_POURC"
        }
        self.edit_type = tk.StringVar()
        self.edit_type.set(next(iter(self.edit_type_list)))

        # Menu déroulant du type d'édition
        edit_type_label = tk.Label(self.editbar, bd=0, bg="#a6b8c2", text="Modification :")
        edit_type_label.grid(row=7, column=0, sticky="w", pady=(0, 10), ipadx=5, ipady=5)
        edit_type_option = tk.OptionMenu(self.editbar, self.edit_type, *self.edit_type_list.keys())
        edit_type_option.config(activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0)
        edit_type_option.grid(row=7, column=1, sticky="ew", pady=(0, 10), ipadx=5, ipady=5)

        # Champ de saisie de la valeur d'édition
        edit_input_label = tk.Label(self.editbar, bd=0, bg="#a6b8c2", text="Valeur :")
        edit_input_label.grid(row=8, column=0, sticky="w", pady=(0, 10), ipadx=5, ipady=5)
        self.edit_input_value = tk.Entry(self.editbar)
        self.edit_input_value.grid(row=8, column=1, sticky="w", pady=(0, 10), ipadx=5, ipady=5)

        # On conserve si l'édition est un remplacement ou un ajout
        self.edit_is_offset_icons = {
            False : "\u27f3",
            True : "\u002b"
        }
        self.edit_is_offset = tk.BooleanVar()
        self.edit_is_offset.set(False)

        # Bouton de remplacement de l'édition
        self.edit_replace_button = tk.Radiobutton(self.editbar, activebackground="#a6b8c2", bd=0, bg="#a6b8c2", highlightthickness=0, text=f"{self.edit_is_offset_icons.get(False)} Remplacer", value=False, variable=self.edit_is_offset)
        self.edit_replace_button.grid(row=9, column=0, sticky="w", pady=(0, 10), ipadx=5, ipady=5)

        # Bouton d'ajout de l'édition
        self.edit_add_button = tk.Radiobutton(self.editbar, activebackground="#a6b8c2", bd=0, bg="#a6b8c2", highlightthickness=0, text=f"{self.edit_is_offset_icons.get(True)} Ajouter", value=True, variable=self.edit_is_offset)
        self.edit_add_button.grid(row=9, column=1, sticky="w", pady=(0, 10), ipadx=5, ipady=5)

        # Bouton de validation de l'édition
        self.edit_valid_button = tk.Button(self.editbar, activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0, text="Valider")
        self.edit_valid_button.grid(row=10, column=0, columnspan=2, sticky="sew", padx=10, ipadx=5, ipady=5)

    """
    Création de la date et de l'heure.
    """
    def init_datetime(self):
        self.datetime = tk.Label(self.canvas, bg="#ffffff", justify="left")

    """
    Création des coordonnées.
    """
    def init_coordinates(self):
        self.coordinates = tk.Label(self.canvas, bg="#ffffff", justify="left", text="Latitude : 0.0\nLongitude : 0.0")
        self.coordinates.grid(row=1, column=1, sticky="sw", padx=(10, 0), pady=(0, 10), ipadx=5, ipady=5)

    """
    Création de la barre d'historique.
    """
    def init_historybar(self):
        self.historybar = tk.Frame(self.canvas, bg="#a6b8c2", cursor="arrow", padx=10, pady=10)
        self.historybar.rowconfigure(0, weight=1)

        # Liste de l'historique
        self.history_list = tk.Listbox(self.historybar, exportselection=False, selectbackground="#3d9ccc", selectforeground="#000000")
        self.history_list.grid(row=0, column=0, sticky="nsew", pady=10, ipadx=5, ipady=5)

        # Bouton de fermeture de l'historique
        self.history_close_button = tk.Button(self.historybar, activebackground="#3588b2", bg="#3d9ccc", highlightthickness=0, text="Fermer")
        self.history_close_button.grid(row=1, column=0, sticky="sew", padx=10, ipadx=5, ipady=5)

    """
    Création de la ligne temporelle.
    """
    def init_timeline(self):
        # On conserve le pas de la ligne temporelle
        self.timeline_step = tk.IntVar()

        # Ligne temporelle
        self.timeline = tk.Scale(self, activebackground="#3588b2", bg="#85caf2", highlightbackground="#85caf2", highlightthickness=10, orient="horizontal", showvalue=False, troughcolor="#ffffff", variable=self.timeline_step)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
