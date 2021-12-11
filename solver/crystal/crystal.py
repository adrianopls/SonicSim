
"""
https://scipython.com/blog/simulating-two-dimensional-polycrystals/

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
from matplotlib.patches import Polygon
import random


# from .atom import Atom
# from .grain import Grain
# from .sim_cells import SimCells


from atom import Atom
from grain import Grain
from sim_cells import SimCells


DEFAULT_DPI=100.0



def distance(p, q):
    """Return the Euclidean distance between points p and q."""
    return np.hypot(*(p-q))



class Crystal:
    """A simulation of a two-dimensional polycrystal."""

    def __init__(self, ngrains=5, seed_minimum_distance=0.2, lattice='hex',
                 atom_diameter=0.02, xsize=1000.0, ysize=1000.0):
        """Initialise the polycrystal.

        ngrains is the number of grains, to be placed randomly on the unit
        square with a minumum distance, seed_minimum_distance, between them.
        hex = 'hex' or 'square' is the crystalline lattice type and d is the
        atom diameter.

        """

        """
            Lattice - arranjo do modelo (hexagonal ou quadrangular)
            atom_diameter (d) eh o diametro de cada circulo que compoe o modelo 
        """


        self.ngrains = ngrains
        self.seed_minimum_distance = seed_minimum_distance
        self.lattice = lattice
        self.atom_diameter = atom_diameter
        self.atoms, self.grains = [], []
        self.xsize = xsize
        self.ysize = ysize


        print("\n\nCrystal")
        print("ngrains: ", ngrains)
        print("seed_minimum_distance", seed_minimum_distance)
        print("lattice: " , lattice)
        print("diameter: " , atom_diameter)      
        print("xsize: " , xsize)
        print("ysize: " , ysize)
        print()
        print() 

        
        
    def seed_grains(self):
        """Place the ngrain seeds randomly, a minimum distance apart."""
        
        """De acordo com o critério de validação de distancia minima entre os 
        seeds (Origens) dos Grains, obtém o ponto de origem de cada um dos 
        Grains e os instancia."""
        
        print("seed_grains")

        # Reset the crystal.
        self.atoms, self.grains = [], []
        self.sim_cells = SimCells(self.atom_diameter, factor=self.xsize)

        for i in range(self.ngrains):
            while True:
                grain_origin_atom_coord = np.random.random((2,))
                grain_origin_atom_coord[0] = grain_origin_atom_coord[0] * self.xsize
                grain_origin_atom_coord[1] = grain_origin_atom_coord[1] * self.ysize
                print("\ngrain_origin_atom_coord: ", grain_origin_atom_coord)
                print("len(self.atoms): ", len(self.atoms))
                
                for atom in self.atoms:
                    #print()
                    print("atom grain_origin_atom_coord: ", grain_origin_atom_coord)
                    print("atom coords: ", atom.coords)
                    print("atom distance: ", distance(grain_origin_atom_coord, atom.coords))
                    print("atom seed_minimum_distance: ", self.seed_minimum_distance)
                    
                    if distance(grain_origin_atom_coord, atom.coords) < self.seed_minimum_distance:
                        # Seed atom too close to another: go back and try again
                        break
                else:
                    # Initialise a grain and add its seed atom.
                    grain = Grain(i, grain_origin_atom_coord, self.lattice)
                    self.grains.append(grain)
                    print("Atom 001")
                    atom = Atom(grain, grain_origin_atom_coord)
                    self.atoms.append(atom)
                    self.sim_cells.add_atom_to_cell(atom)
                    break


    def grow_crystal(self):
        """Grow a new polycrystal."""

        print("\ngrow_crystal")

        self.seed_grains()

        # i_active is a list of the indices of atoms whcih have space next
        # to them to place a new atom.
        i_active = list(range(self.ngrains))
        while i_active:
            # Pick a random "active" atom, and get its neighbouring lattice
            # sites with enough space to place a new atom
            i = np.random.choice(i_active)
            candidate_sites = self.get_neighbour_candidate_sites(self.atoms[i])
            if not candidate_sites:
                # No candidate site was found: the atom is no longer active.
                i_active.remove(i)
                continue
            # Add the atom and mark it as active (until we know better).
            n = len(self.atoms)
            #print("Atom 002")
            atom = Atom(self.atoms[i].grain, random.choice(candidate_sites))
            self.atoms.append(atom)
            self.sim_cells.add_atom_to_cell(atom)
            i_active.append(n)

        #print(len(self.atoms), 'atoms placed')



    def get_neighbour_candidate_sites(self, atom):
        """Return candidate locations next to atom to place a new atom.

        Look for sites on the crystal lattice of the grain of the provided
        atom with enough space to locate a new atom and return a list of
        the site coordinates.

        """
        
#        print("\nget_neighbour_candidate_sites")
        
        neighbour_sites = atom.coords + self.atom_diameter * atom.grain.lattice_disp
        candidate_sites = []
        
        for site in neighbour_sites:

            if not (0 <= site[0] < self.xsize and 0 <= site[1] < self.ysize):
#                print("neighbour_site: ", site, " - RUIM")
                continue
#            print("neighbour_site: ", site, " - OK")
            
            # neighbouring_atoms_generator spits out atoms in the
            # vicinity of site, using our array of "SimCells".
            neighbouring_atoms_generator = self.sim_cells.neighbouring_atoms_generator(site)

            #print(len(neighbouring_atoms_generator))
            
            #raise Exception("")

            for other_atom in neighbouring_atoms_generator:         # TODO: 0.99 ?????
                
#                print()
#                print(0.99)
#                print(self.atom_diameter)
#                print(self.atom_diameter * 0.99)
#                print("zzz site: ", site)
                # print("zzz coords: ", other_atom.coords)
#                print("zzz distance: ", distance(site, other_atom.coords))
                # print("zzz seed_minimum_distance: ", self.seed_minimum_distance)               
                
                #if 1==1:
                if distance(site, other_atom.coords) < self.atom_diameter * 0.99:
#                    print("BREAKOUUUUUUUUUUUUUUUUUU: ")
                    break
            else:
                candidate_sites.append(site)
        return candidate_sites


    def save_atom_positions(self, filename='crystal.out'):
        """Save the atom diameter and all atom locations to filename."""

        with open(filename, 'w') as fo:
            print('d =', self.atom_diameter, file=fo)
            for atom in self.atoms:
                print(atom.coords[0], atom.coords[1], file=fo)

    def _get_patch_vertices(self, atom):
        return atom.coords + self.atom_diameter * atom.grain.patch_disp


    def plot_crystal(self, filename='crystal_007.png', circular_atoms=True,
                     colours=None, **kwargs):
        """Create a Matplotlib image of the polycrystal as filename.

        If colours is None, use a single colour for all atoms; otherwise
        a sequence of colours to cycle through for each grain can be
        provided. Additional kwargs are passed straight to the PatchCollection
        call that controls the drawing style of the atoms.
        If circular_atoms is not True, each atom is represented by the shape of
        its lattice (square or hexagon).

        """

        if not colours:
            # Atoms are boring grey if no alternative is provided.
            colours = ['#444444']
            #colours = ['#000000']
        ncolours = len(colours)

        if not kwargs:
            kwargs = {'linewidth': 1, 'edgecolor': 'k'}


        

        fig, ax = plt.subplots(figsize=[self.xsize/DEFAULT_DPI, 
                                        self.ysize/DEFAULT_DPI], 
                               dpi=DEFAULT_DPI)

        

        # We have a bit of book-keeping to do: group the atoms into their
        # grains in this dictionary, keyed by the grain_id.
        grains = {}
        for atom in self.atoms:
            grains.setdefault(atom.grain.grain_id, []).append(atom)

        for j, atoms in grains.items():
            #print("j: ", j)
            if circular_atoms:
                # center = atom.coords
                #print(atom.coords)
                #patches = [Circle(atom.coords, radius=self.atom_diameter/2) for atom in atoms]
                patches = []
                for atom in atoms:
#                    print("atom.coords: ", atom.coords)
                    patches.append(Circle(atom.coords, radius=self.atom_diameter/2) )
            else:
                patches = [Polygon(self._get_patch_vertices(atom)) for atom in atoms]
                
            c = PatchCollection(patches, facecolor=colours[j % ncolours],
                                **kwargs)
            ax.add_collection(c)
            
        # Ensure the Axes are square and remove the spines, ticks, etc.

        ax.set_xlim((0.0, self.xsize))
        ax.set_ylim((0.0, self.ysize))
        
        #ax.set_aspect('equal', 'box')
        
        rect = [0.0, 0.0, 1.0, 1.0]
        ax.set_position(rect)
        plt.axis('off')



        plt.savefig(filename)
        plt.show()
        
        #arr = plt.gcf().canvas.tostring_rgb()

        #print(arr)        
        

# Lattice - arranjo
# ngrains = ngrains=5, seed_minimum_distance=0.2, lattice='hex',              atom_diameter=0.02

# crystal = Crystal(ngrains=1, 
#                    seed_minimum_distance=0.01, 
#                    #lattice='hex', 
#                    lattice = 'square',
#                    atom_diameter=0.5,
#                    xsize=1.0, 
#                    ysize=1.0)

crystal = Crystal(ngrains=1, 
                  seed_minimum_distance=10.0, 
                  #lattice='hex', 
                  lattice = 'square',
                  atom_diameter=100.0,
                  xsize=1000.0, 
                  ysize=1000.0)

crystal.grow_crystal()
crystal.plot_crystal(linewidth=0, filename='crystal_008_5.png')
