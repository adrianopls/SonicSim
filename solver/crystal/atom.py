
class Atom:
    """A simple atom in a 2-D crystal grain, with its coordinates."""

    """Cada grao que compoe o modelo eh um Atom. """

    def __init__(self, grain, coords):
        self.grain = grain
        self.coords = coords