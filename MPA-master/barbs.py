from PIL import Image, ImageDraw
from pathlib import Path
import random
import time



class Barbs:
    """
    Affichage optimise des barbules
    """



    def __init__(self):


        self.barb_size = 20
        self.barbs_image = []
        self.layer = None
        self.load_barb()



    def load_barb(self):
        for speed in range (0, 150, 5):
            barb_path = Path(__file__).parent.absolute() / "images" / "barbs" / f"{speed}.png"
            self.barbs_image.append(
                Image.open(barb_path).resize((self.barb_size, self.barb_size)))
            
    """
        generate barbs layer
    """
    def create_barbs_layer(self, layer_width, layer_height):
        # clean if a layer already exist
        self.layer_with = layer_width
        self.layer_height = layer_height
        # creation d un layer
        # visible_bbox (0,0,0,0) 
        self.layer = Image.new("RGBA", (layer_width, layer_height), (0,0,0,0))

    def add_barb_on_layer(self, position, size, speed, direction):
        # check if a layer already exist 
        if self.layer is None :
            return
        # retrouver la barbule correspondant a la vitesse
        barb = self.barbs_image[int(speed/5)]

        barb = barb.rotate(direction)

        self.layer.paste(barb, position)

    def get_layer(self):
        return self.layer
    