# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 10:39:27 2021

@author: Adriano
"""

import numpy as np


class SimCells:
    """A region of the simulation area to search for neighbours.

    To save us from calculating all the pairwise distances, keep track of
    the location of atoms in "cells": for a given candidate site, we then only
    need to look within that site's cell and its immediate neighbouring cells.

    """

    def __init__(self, atom_diameter, factor=1.0):
        """Initialize the cell size and the array of cells."""
        self.factor = factor
        print()
        print("DISTANCE: ", atom_diameter)
        self.n = int((1*self.factor) / 2 / atom_diameter)
        print("N: ", self.n)
        self.a = 1 / self.n
        print(self.n)
        print("a: ", self.a)
        
        self.cell_array = [[[] for i in range(self.n)] for j in range(self.n)]
        
        print("cell_array.shape: ", np.asarray(self.cell_array).shape)
        print(np.asarray([1, 2, 3]).shape)


    def _get_cell_indexes_from_atom_coords(self, coords):
        """Return the indexes ix, iy of the cell containing point coords."""

        x, y = coords
        x = x/self.factor
        y = y/self.factor
        return int(x / self.a), int(y / self.a)


    def _get_atom_cell(self, atom):
        """Return the cell containing atom."""

        ix, iy = self._get_cell_indexes_from_atom_coords(atom.coords)
        
        print("ix, iy: ", ix, iy)
        return self.cell_array[ix][iy]


    def add_atom_to_cell(self, atom):
        """Add atom to the appropriate cell."""

        self._get_atom_cell(atom).append(atom)


    def neighbouring_atoms_generator(self, coords):
        """Return a generator yielding all atoms "near" point coords."""

        ix, iy = self._get_cell_indexes_from_atom_coords(coords)
        dxy = ((0,0), (1,0), (1,1), (0,1),
               (-1,1), (-1,0), (-1,-1), (0,-1), (-1,1))
        for dx, dy in dxy:
            ixx, iyy = ix+dx, iy+dy
            if not (0 <= ixx < self.n and 0 <= iyy < self.n):
                continue
            for atom in self.cell_array[ixx][iyy]:
                yield atom
