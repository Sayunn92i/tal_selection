import tools
from move import Move
from edit import Edit
from grib import Grib
from geojson import Geojson
from history import History
from pathlib import Path
from PIL import Image, ImageTk

class Map:
    def __init__(self, app):

        # Application
        self.app = app

        # Attributs
        self.tiles_ref = {}
        self.tiles_size = 256
        self.zoom_level = 2
        self.max_zoom_level = 12
        self.min_zoom_level = 2

        # Initialisation
        self.configuration()

        # Évènements
        self.app.canvas.bind("<Motion>", self.update_latlon)
        self.app.canvas.bind("<MouseWheel>", self.zoom)
        self.app.canvas.bind("<Button-4>", self.zoom)
        self.app.canvas.bind("<Button-5>", self.zoom)
        self.app.canvas.bind("<Configure>", self.resize)

        # Fonctionnalités
        self.move = Move(self)
        self.edit = Edit(self)
        self.grib = Grib(self)
        self.geojson = Geojson(self)
        self.history = History(self)

    """
    Configuration de la classe.
    """
    def configuration(self):
        # Mise à jour et centrage du canevas
        self.app.canvas.update()
        self.app.canvas.scan_dragto(int(self.app.canvas.winfo_width() / 2 - 2 ** self.zoom_level * self.tiles_size / 2), int(self.app.canvas.winfo_height() / 2 - 2 ** self.zoom_level * self.tiles_size / 2), gain=1)

        self.mark_center()
        self.draw_tiles()

    """
    Positionne un marqueur au centre de la partie visible du canevas,
    utile lorsqu'il s'agit de redimensionner la fenêtre.
    """
    def mark_center(self):
        w, h = self.app.canvas.winfo_width(), self.app.canvas.winfo_height()
        self.app.canvas.scan_mark(int(w / 2), int(h / 2))

    """
    Charge l'image d'une tuile via un chemin donné par les paramètres column et row,
    on ajoute ensuite la tuile sur le canevas tout en conservant ses informations dans un dictionnaire.

    @param tile_bbox: boîte englobante de l'image
    @param column: colonne de la tuile
    @param row: ligne de la tuile
    """
    def load_tile(self, tile_bbox, column, row):
        """tile_path = Path(__file__).parent.absolute() / "images" / "tiles" / f"{self.zoom_level}" / f"{column}" / f"{row}.png" """

        tile_path = Path(f"/home/clement/TAL/map/rasterTile/{self.zoom_level}/{column}/{row}.png")
        # On vérifie si l'image existe avant d'ouvrir le fichier
        if tile_path.exists():
            tile_open = Image.open(tile_path)

            # Objet image
            tile_image = ImageTk.PhotoImage(tile_open)

            # Ajout de la tuile sur le canevas
            tile = self.app.canvas.create_image(tile_bbox[0], tile_bbox[1], anchor="nw", image=tile_image, tag="tile")
            #border = self.app.canvas.create_rectangle(tile_bbox[0], tile_bbox[1], tile_bbox[2], tile_bbox[3], fill="", outline="#000000", tag="border")

            # Sauvegarde des informations de la tuile, on inclut l'objet image pour qu'il ne soit pas supprimé par le garbage collector
            #self.tiles_ref[tile_bbox] = (tile, border, tile_image)
            self.tiles_ref[tile_bbox] = (tile, tile_image)

    """
    Dessine toutes les tuiles dans la zone visible.
    """
    def draw_tiles(self):
        # Obtention de l'intervalle des tuiles pour la zone visible
        visible_bbox = tools.get_visible_bbox(self.app.canvas, self.zoom_level)
        tiles_range = tools.get_tiles_range(visible_bbox, self.tiles_size)

        # Pour chaque colonne et ligne visible on charge l'image associée
        for column in range(tiles_range[0], tiles_range[1]):
            for row in range(tiles_range[2], tiles_range[3]):

                # Obtention de la boîte englobante de l'image
                x1, y1 = column * self.tiles_size, row * self.tiles_size
                x2, y2 = x1 + self.tiles_size, y1 + self.tiles_size
                z = self.zoom_level
                tile_bbox = (x1, y1, x2, y2, z)

                if tile_bbox not in self.tiles_ref:
                    self.load_tile(tile_bbox, column, row)

    """
    Supprime les tuiles et les barbules qui ne sont plus dans la zone visible.
    """
    def clear(self):
        # Obtention de la zone visible
        visible_bbox = tools.get_visible_bbox(self.app.canvas, self.zoom_level)

        # Supprime les tuiles en dehors de la zone visible
        for tile_bbox, value in list(self.tiles_ref.items()):
            if not tools.is_intersection(visible_bbox, tile_bbox):
                self.app.canvas.delete(value[0])
                #self.app.canvas.delete(value[1])
                del self.tiles_ref[tile_bbox]

        # Supprime les barbules en dehors de la zone visible
        for barb_bbox, value in list(self.grib.barbs_ref.items()):
            if not tools.is_intersection(visible_bbox, barb_bbox):
                self.app.canvas.delete(value[0])
                del self.grib.barbs_ref[barb_bbox]

    """
    Met à jour la latitude et la longitude en fonction de la position de la souris.
    """
    def update_latlon(self, event):
        x, y = self.app.canvas.canvasx(event.x), self.app.canvas.canvasy(event.y)
        latitude, longitude = tools.pixels_to_latlon(self.tiles_size, self.zoom_level, x, y)
        self.app.coordinates.config(text=f"Latitude : {latitude}\nLongitude : {longitude}")

    """
    Change le niveau de zoom après un défilement de la molette.
    """
    def zoom(self, event):
        x, y = self.app.canvas.canvasx(event.x), self.app.canvas.canvasy(event.y)

        # Positionne un marqueur sur le coin haut gauche de la partie visible du canevas
        self.app.canvas.scan_mark(0, 0)

        if event.delta > 0 or event.num == 4:
            # Zoom sur la carte
            if self.zoom_level < self.max_zoom_level:
                self.zoom_level += 1
                self.app.canvas.scan_dragto(int(-x), int(-y), gain=1)
                self.edit.scale_up()
        else:
            # Dézoom sur la carte
            if self.zoom_level > self.min_zoom_level:
                self.zoom_level -= 1
                self.app.canvas.scan_dragto(int(x / 2), int(y / 2), gain=1)
                self.edit.scale_down()

        self.app.canvas.delete("tile")
        #self.app.canvas.delete("border")
        self.app.canvas.delete("barb")
        self.app.canvas.delete("features")
        self.tiles_ref = {}
        self.grib.barbs_ref = {}
        self.mark_center()
        self.draw_tiles()
        self.geojson.draw_features()

    """
    Charge ou supprime les tuiles en fonction de la taille du canevas.
    """
    def resize(self, event):
        self.app.canvas.scan_dragto(int(event.width / 2), int(event.height / 2), gain=1)
        self.draw_tiles()
        self.clear()
