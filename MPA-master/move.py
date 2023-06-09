class Move:
    def __init__(self, map):

        # Application et carte
        self.app = map.app
        self.map = map

        # Initialisation
        self.configuration()

    """
    Configuration de la classe.
    """
    def configuration(self):
        # Barre d'outils
        self.app.move_button.config(command=self.activate)

        # Activation de l'outil de déplacement par défaut
        self.activate()

    """
    Active l'outil de déplacement.
    """
    def activate(self):
        # Barre d'outils
        self.app.move_button.config(state="disabled")
        self.app.edit_button.config(state="normal")

        # Barre d'édition
        self.app.editbar.grid_remove()

        # Canevas
        self.app.canvas.bind("<ButtonPress-1>", self.start)
        self.app.canvas.bind("<B1-Motion>", self.move)
        self.app.canvas.bind("<ButtonRelease-1>", self.end)
        self.app.canvas.config(cursor="fleur")

    """
    Marque le début du déplacement au moment d'un clique gauche sur le canevas.
    """
    def start(self, event):
        # Positionne un marqueur sur l'emplacement initiale du curseur
        self.app.canvas.scan_mark(event.x, event.y)

    """
    Effectue un déplacement avec un maintien du clique gauche sur le canevas.
    """
    def move(self, event):
        self.app.canvas.scan_dragto(event.x, event.y, gain=1)
        self.map.draw_tiles()

    """
    Marque la fin du déplacement après un relâchement du clique gauche sur le canevas.
    """
    def end(self, event):
        self.map.mark_center()
        self.map.clear()
