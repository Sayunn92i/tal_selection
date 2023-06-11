import tools
from move import Move
from edit import Edit
from grib import Grib
from geojson import Geojson
from history import History
from pathlib import Path
from PIL import Image, ImageTk, ImageFilter


class Map:
    def __init__(self, app):

        # Application
        self.app = app

        # Attributs
        self.tiles_ref = {}
        self.based_tiles_size = 256
        self.scale = 1
        self.tiles_size = self.based_tiles_size * self.scale
        self.zoom_level = 2
        self.max_zoom_level = 12
        self.min_zoom_level = 2
        self.max_zoom_scale = 6
        self.min_zoom_scale = 1
        

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
        self.app.canvas.update()  # a voir si necessaire
        self.app.canvas.scan_dragto(int(self.app.canvas.winfo_width() / 2 - 2 ** self.zoom_level * self.tiles_size / 2), int(
            self.app.canvas.winfo_height() / 2 - 2 ** self.zoom_level * self.tiles_size / 2), gain=1)

        self.mark_center()
        self.draw_tiles()

        # just for the test draw a rectangle at the center

        self.app.canvas.update()
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
        smoother = True # ANTIALIAS

        # tile_path = Path(__file__).parent.absolute() / "images" / "tiles" / f"{self.zoom_level}" / f"{column}" / f"{row}.png"
        tile_path = Path(
            f"/media/jmaxime/data-a/tal-projet/map/rasterTile/{self.zoom_level}/{column}/{row}.png")

        # On vérifie si l'image existe avant d'ouvrir le fichier
        if tile_path.exists():

            new_size = (int(self.tiles_size), int(self.tiles_size) )
            tile_open = Image.open(tile_path).resize(new_size)

            # Objet image
            tile_image = ImageTk.PhotoImage(tile_open)

            # Ajout de la tuile sur le canevas
            tile = self.app.canvas.create_image(
                tile_bbox[0], tile_bbox[1], anchor="nw", image=tile_image, tag="tile")
            border = self.app.canvas.create_rectangle(
                tile_bbox[0], tile_bbox[1], tile_bbox[2], tile_bbox[3], fill="", outline="#000000", tag="border")

            # Sauvegarde des informations de la tuile, on inclut l'objet image pour qu'il ne soit pas supprimé par le garbage collector
            # ATTENTION LIGNE INUTILE :  => confusion 
            self.tiles_ref[tile_bbox] = (tile, border, tile_image)
            self.tiles_ref[tile_bbox] = (tile, tile_image, tile_open)
            


    """
    Dessine toutes les tuiles dans la zone visible.
    """

    def draw_tiles(self):

        self.tiles_size = int(self.based_tiles_size * self.scale)

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
                # self.app.canvas.delete(value[1])
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
        x, y = self.app.canvas.canvasx(
            event.x), self.app.canvas.canvasy(event.y)
        latitude, longitude = tools.pixels_to_latlon(
            self.tiles_size, self.zoom_level, x, y)
        self.app.coordinates.config(
            text=f"Latitude : {latitude}\nLongitude : {longitude}")

    """
    Change le niveau de zoom OU de scale après un défilement de la molette.
    """

    def zoom(self, event):
        # COnverstion des coordoner de l'évenement, 
        # En latitude et longitude
        latitude, longitude = self.app.canvas.canvasx(
            event.x), self.app.canvas.canvasy(event.y)

        # Positionne un marqueur sur le canvas
        self.app.canvas.scan_mark(0, 0)

        # Evenement : zoom ou zoom_out
        if event.delta > 0 or event.num == 4:
            self.zoom_in(latitude, longitude)
        else:
            self.zoom_out(latitude,longitude)

        # Supression de la cartes du canvas
        self.clean_map()

        # Affichage de la carte
        self.draw_tiles()
        self.geojson.draw_features()
        self.grib.draw_barbs()

    # Zoom * 2 à la position (latitude longitude)
    def zoom_in(self, latitude , longitude):
        if self.zoom_level < self.max_zoom_level:
            self.zoom_level += 1
            self.app.canvas.scan_dragto(int(-latitude), int(-longitude), gain=1)
        elif self.scale < self.max_zoom_scale : 
            self.scale = self.scale * 2
            self.app.canvas.scan_dragto(int(-latitude), int(-longitude), gain=1)
    
    # Zoom / 2 à la position (latitude longitude)
    def zoom_out(self, latitude, longitude):
        if self.scale > self.min_zoom_scale:
            self.scale = self.scale / 2
            self.app.canvas.scan_dragto(int(latitude/2), int(longitude/2), gain=1)
        elif self.zoom_level > self.min_zoom_level:
            self.zoom_level -= 1
            self.app.canvas.scan_dragto(int(latitude / 2), int(longitude / 2), gain=1)
        
    # Netoyage des éléments graphique lié à la carte :
    def clean_map(self):
        self.app.canvas.delete("tile")
        self.app.canvas.delete("border")
        self.app.canvas.delete("barb")
        self.app.canvas.delete("features")

        self.tiles_ref = {}
        self.grib.barbs_ref = {}
    
    """
    Charge ou supprime les tuiles en fonction de la taille du canevas.
    """

    def resize(self, event):
        self.app.canvas.scan_dragto(
            int(event.width / 2), int(event.height / 2), gain=1)
        self.draw_tiles()
        self.clear()