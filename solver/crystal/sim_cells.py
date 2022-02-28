

class SimCells:
    """A region of the simulation area to search for neighbours.

    To save us from calculating all the pairwise distances, keep track of
    the location of atoms in "cells": for a given candidate site, we then only
    need to look within that site's cell and its immediate neighbouring cells.

    """

    """A 
    """


    def __init__(self, atom_diameter, factor=1.0):
        """Initialize the cell size and the array of cells."""
        self.factor = factor
        
        """ n representa o tamanho do vetor de dados nas direções X e Y. """
        self.n = int((self.factor / 2) / atom_diameter)
        
        """ a representa a resolução do modelo. """
        self.a = factor / self.n
        
        """ cell_array é o vetor de dados (Atoms) organizado em forma de uma 
        matriz (2D) de vetores para facilitar a localizacão em relação a 
        vizinhança. """
        self.cell_array = [[[] for i in range(self.n)] for j in range(self.n)]
        
        #TODO: Alertar sobre uso da memória ram de acordo com tamanho de cell_array


    def _get_cell_indexes_from_atom_coords(self, coords):
        """Return the indexes ix, iy of the cell containing point coords."""
        
        """Retorna o índice do vetor de dados que representa uma determinada
        coordenada."""
        
        x, y = coords
        return int(x / self.a), int(y / self.a)


    def _get_atom_cell(self, atom):
        """Return the cell containing atom."""

        ix, iy = self._get_cell_indexes_from_atom_coords(atom.coords)

        return self.cell_array[ix][iy]



    def add_atom_to_cell(self, atom):
        """Add atom to the appropriate cell."""
        self._get_atom_cell(atom).append(atom)



    def neighbouring_atoms_generator(self, coords):
        """Return a generator yielding all atoms "near" point coords."""

        """ A partir de um par de coordenadas, obtém um generator contendo a 
        os Atoms da celula de indice associada as coordenadas e também das
        outras 8 células vizinhos, caso eles estejam dentro dos limites
        do cell_array."""

        ix, iy = self._get_cell_indexes_from_atom_coords(coords)       
        dxy = ((0,0), (1,0), (1,1), (0,1),
               (-1,1), (-1,0), (-1,-1), (0,-1), (-1,1))       
        for dx, dy in dxy:
            ixx, iyy = ix+dx, iy+dy
            if not (0 <= ixx < self.n and 0 <= iyy < self.n):
                continue
            for atom in self.cell_array[ixx][iyy]:
                yield atom




















