# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 10:27:00 2021

@author: Adriano
"""




class Atom:
    """A simple atom in a 2-D crystal grain, with its coordinates."""


    """Cada grao eh um Atom. """

    def __init__(self, grain, coords):
        print("Atom: ", grain.grain_id , coords)
        self.grain = grain
        self.coords = coords