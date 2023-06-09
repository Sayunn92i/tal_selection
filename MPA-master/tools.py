import math
import numpy as np


"""
Calcule la direction du vent à partir des composantes u et v.

@param u: direction ouest/est (positif depuis l'ouest et négatif depuis l'est)
@param v: direction sud/nord (positif depuis le sud et négatif depuis le nord)

@return: la direction du vent en degrés
"""
def wind_uv_to_direction(u, v):
    return (270 - math.atan2(v, u) * 180 / math.pi) % 360

"""
Calcule la vitesse du vent à partir des composantes u et v.

@param u: direction ouest/est (positif depuis l'ouest et négatif depuis l'est)
@param v: direction sud/nord (positif depuis le sud et négatif depuis le nord)

@return: la vitesse du vent en mètres par seconde
"""
def wind_uv_to_speed(u, v):
    return math.sqrt(u * u + v * v)

"""
Converti un point en pixels (x, y) en point géographique (latitude, longitude).

@param tiles_size: taille des tuiles
@param zoom_level: niveau de zoom
@param x: coordonnée x
@param y: coordonnée y

@return: le point géographique au format (latitude, longitude)
"""
def pixels_to_latlon(tiles_size, zoom_level, x, y):
    C = (tiles_size / (2 * math.pi)) * 2 ** zoom_level
    M = (x / C) - math.pi
    N = -(y / C) + math.pi
    latitude = math.degrees((math.atan(math.e ** N) - (math.pi / 4)) * 2)
    longitude = math.degrees(M)
    return latitude, longitude

"""
Converti un point géographique (latitude, longitude) en point en pixels (x, y).

@param tiles_size: taille des tuiles
@param zoom_level: niveau de zoom
@param latitude: coordonnée de la latitude
@param longitude: coordonnée de la longitude

@return: le point en pixels au format (x, y)
"""
def latlon_to_pixels(tiles_size, zoom_level, latitude, longitude):
    C = (tiles_size / (2 * math.pi)) * 2 ** zoom_level
    x = C * (math.radians(longitude) + math.pi)
    y = C * (math.pi - math.log(math.tan((math.pi / 4) + math.radians(latitude) / 2)))
    return x, y

"""
Converti un objet Datetime64 en paramètres pour l'API (date, time).

@param datetime: objet Datetime64

@return: les paramètres pour l'API au format (date, time)
"""
def datetime64_to_params(datetime):
    Y, M, D, h, m = [datetime.astype("datetime64[%s]" % kind) for kind in "YMDhm"]
    years = Y.astype(int) + 1970
    months = M.astype(int) % 12 + 1
    days = (D - M).astype(int) + 1
    hours = (h - D).astype(int)
    minutes = (m - h).astype(int)
    date = f"{days:02d}/{months:02d}/{years}"
    time = f"{hours:02d}:{minutes:02d}"
    return (date, time)

"""
Confirme s'il y a une intersection entre deux boîtes englobantes en pixels (x1, y1, x2, y2, z).

@bbox1: première boîte englobante
@bbox2: deuxième boîte englobante

@return: True si intersection, False sinon
"""
def is_intersection(bbox1, bbox2):
    return bbox1[0] <= bbox2[2] and bbox1[1] <= bbox2[3] and bbox1[2] >= bbox2[0] and bbox1[3] >= bbox2[1] and bbox1[4] == bbox2[4]

"""
Retourne la boîte englobante en pixels (x1, y1, x2, y2, z) de la zone visible.

@param canvas: widget canevas

@return: la boîte englobante en pixels de la zone visible au format (x1, y1, x2, y2, z)
"""
def get_visible_bbox(canvas, zoom_level):
    w, h = canvas.winfo_width(), canvas.winfo_height()
    x1, y1 = canvas.canvasx(0), canvas.canvasy(0) # Point en pixels en haut à gauche
    x2, y2 = canvas.canvasx(w), canvas.canvasy(h) # Point en pixels en bas à droite
    z = zoom_level
    return (x1, y1, x2, y2, z)

"""
Retourne l'intervalle des tuiles à partir d'une boîte englobante en pixels (x1, y1, x2, y2, z).

@param bbox: boîte englobante
@param tiles_size: taille des tuiles

@return: l'intervalle des tuiles pour la boîte englobante au format (start_column, end_column, start_row, end_row)
"""
def get_tiles_range(bbox, tiles_size):
    start_column = int(bbox[0] // tiles_size)
    end_column = int(bbox[2] // tiles_size) + 1 # +1 pour obtenir la tuile qui dépasse
    start_row = int(bbox[1] // tiles_size)
    end_row = int(bbox[3] // tiles_size) + 1 # +1 pour obtenir la tuile qui dépasse
    return (start_column, end_column, start_row, end_row)

"""
Retourne l'intervalle des données des latitudes et longitudes à partir d'une boîte englobante en pixels (x1, y1, x2, y2, z).
On notera que le résultat est approximatif, l'intervalle pouvant potentiellement sortir de la boîte englobante.

@param bbox: boîte englobante
@param tiles_size: taille des tuiles
@param zoom_level: niveau de zoom
@param data_frequency: fréquence d'affichage des données
@param data_latitudes: données des latitudes
@param data_longitudes: données des longitudes

@return: l'intervalle des données des latitudes et longitudes pour la boîte englobante au format (start_latitude, end_latitude, start_longitude, end_longitude)
"""
def get_data_range(bbox, tiles_size, zoom_level, data_frequency, data_latitudes, data_longitudes):
    min_latitude, min_longitude = pixels_to_latlon(tiles_size, zoom_level, bbox[0], bbox[3])
    max_latitude, max_longitude = pixels_to_latlon(tiles_size, zoom_level, bbox[2], bbox[1])

    # Recherche de l'indice de la latitudes minimale et maximale la plus proche dans les données
    start_latitude = np.argmin(np.abs(data_latitudes - min_latitude))
    end_latitude = np.argmin(np.abs(data_latitudes - max_latitude))
    if data_latitudes[0] > data_latitudes[-1]:
        start_latitude, end_latitude = end_latitude, start_latitude

    start_latitude = (start_latitude - 1) // data_frequency * data_frequency + data_frequency # Arrondissement vers le multiple le plus haut
    end_latitude = end_latitude // data_frequency * data_frequency # Arrondissement vers le multiple le plus bas
    end_latitude = end_latitude + 1 # +1 pour compter le dernier indice

    # Recherche de l'indice de la longitudes minimale et maximale la plus proche dans les données
    start_longitude = np.argmin(np.abs(data_longitudes - min_longitude))
    end_longitude = np.argmin(np.abs(data_longitudes - max_longitude))
    if data_longitudes[0] > data_longitudes[-1]:
        start_longitude, end_longitude = end_longitude, start_longitude

    start_longitude = (start_longitude - 1) // data_frequency * data_frequency + data_frequency # Arrondissement vers le multiple le plus haut
    end_longitude = end_longitude // data_frequency * data_frequency # Arrondissement vers le multiple le plus bas
    end_longitude = end_longitude + 1 # +1 pour compter le dernier indice

    return (start_latitude, end_latitude, start_longitude, end_longitude)

"""
Bloque l'exécution et attend qu'un thread donné finisse sa tâche.
On utilise cette fonction pour remplacer Thread.join() qui fige la fenêtre sur Tkinter.
"""
def wait(root, thread):
    while thread.is_alive():
        root.update()
