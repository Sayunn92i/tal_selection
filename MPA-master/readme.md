# Etat avencement branche MAP :
- Exception à traiter => quand aucun fichier grib n est chargé :  exception lors du zoom et déplacement sur la carte, car la méthode draw_barbs (class grib) est appelé dans la méthode move.end et map.zoom .
- Placement des barbules a revoir : méthode get_barb_position à revoir, il y a un léger décalage. 
- La gestion de la taille/densité des barbules peut être amélioré 

# Avant de merge avec les autres branches :
- verifier qu'il n'y a pas de conflit avec la méthode draw_barbs de la class grib