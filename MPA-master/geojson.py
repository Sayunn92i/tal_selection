import tools
import json
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import filedialog as fd

class Geojson:
    def __init__(self, map):

        # Application et carte
        self.app = map.app
        self.map = map

        # Attributs
        self.data_features = None

        # Initialisation
        self.configuration()

    """
    Configuration de la classe.
    """
    def configuration(self):
        # Menu
        self.app.file_menu.entryconfig(1, command=self.open)
        self.app.file_menu.entryconfig(3, command=self.close)

        # Barre d'outils
        self.app.geojson_button.config(command=self.open)

    """
    Active les fonctionnalités du fichier GeoJSON.
    """
    def activate(self):
        # Menu
        self.app.file_menu.entryconfig(3, state="normal")

        # Barre d'outils
        geojson_icon_open = Image.open(Path(__file__).parent.absolute() / "images" / "icons" / "geojson_close.png").resize((32,32))
        self.app.geojson_icon_image = ImageTk.PhotoImage(geojson_icon_open)
        self.app.geojson_button.config(command=self.close, image=self.app.geojson_icon_image)

    """
    Désactive les fonctionnalités du fichier GeoJSON.
    """
    def deactivate(self):
        # Menu
        self.app.file_menu.entryconfig(3, state="disabled")

        # Barre d'outils
        geojson_icon_open = Image.open(Path(__file__).parent.absolute() / "images" / "icons" / "geojson_open.png").resize((32,32))
        self.app.geojson_icon_image = ImageTk.PhotoImage(geojson_icon_open)
        self.app.geojson_button.config(command=self.open, image=self.app.geojson_icon_image)

    """
    Récupère les informations du fichier GeoJSON.

    @param file: fichier GeoJSON en lecture seule
    """
    def get_data(self, file):
        self.data_features = json.load(file)["features"]

    """
    Réinitialise les informations du fichier GeoJSON.
    """
    def reset_data(self):
        self.data_features = None

    """
    Ouvre le fichier GeoJSON.
    """
    def open(self):
        # Navigateur de fichiers
        file_types = [("GeoJSON file", ".json .geojson")]
        file = fd.askopenfile(title="Ouvrir un fichier GeoJSON", filetypes=file_types)

        if file:
            # Fermeture du fichier précédent
            self.close()

            # Obtention des informations du fichier
            self.get_data(file)

            # Activation des fonctionnalités du fichier
            self.activate()

            # Dessine les caractéristiques géographiques
            self.draw_features()

    """
    Ferme le fichier GeoJSON.
    """
    def close(self):
        # Réinitialisation des informations du fichier
        self.reset_data()

        # On désactive les fonctionnalités du fichier
        self.deactivate()

        # Suppression des caractéristiques géographiques
        self.app.canvas.delete("features")

    """
    Dessine à partir du fichier GeoJSON toutes les caractéristiques géographiques
    """
    def draw_features(self):
        if self.data_features is not None:
            for feature in self.data_features:

                # Type de caractéristique géographique
                match feature["geometry"]["type"]:
                    case "LineString":
                        segments = []
                        for longitude, latitude in feature["geometry"]["coordinates"]:
                            x, y = tools.latlon_to_pixels(self.map.tiles_size, self.map.zoom_level, latitude, longitude)
                            segments.append((x, y))
                        self.app.canvas.create_line(segments, tag="features")
                    case "MultiLineString":
                        for line in feature["geometry"]["coordinates"]:
                            segments = []
                            for longitude, latitude in line:
                                x, y = tools.latlon_to_pixels(self.map.tiles_size, self.map.zoom_level, latitude, longitude)
                                segments.append((x, y))
                            self.app.canvas.create_line(segments, tag="features")
                    case "Polygon":
                        for contour in feature["geometry"]["coordinates"]:
                            segments = []
                            for longitude, latitude in contour:
                                x, y = tools.latlon_to_pixels(self.map.tiles_size, self.map.zoom_level, latitude, longitude)
                                segments.append((x, y))
                            self.app.canvas.create_line(segments, tag="features")
                    case "MultiPolygon":
                        for polygon in feature["geometry"]["coordinates"]:
                            for contour in polygon:
                                segments = []
                                for longitude, latitude in contour:
                                    x, y = tools.latlon_to_pixels(self.map.tiles_size, self.map.zoom_level, latitude, longitude)
                                    segments.append((x, y))
                                self.app.canvas.create_line(segments, tag="features")
