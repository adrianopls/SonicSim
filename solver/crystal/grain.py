# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 10:36:42 2021

@author: Adriano
"""

import numpy as np



class Grain:
    """A grain in a 2-D (poly-)crystal.

    grain_id is the unique ID of the grain, seed is the (x,y) coordinates of
    the first atom placed in the grain, and lattice is a string identifying
    which kind of crystal lattice to use ('hex' or 'square').

    """

    def __init__(self, grain_id, origin, lattice='hex'):
        #print()
        #print("Grain: ", grain_id, origin, lattice)
        
        self.grain_id = grain_id
        self.origin = origin
        self.lattice = lattice
        
        # Initialize the displacements for other atoms around a reference atom,
        # and the maximum rotation angle, phi, to obtain all orientations.
        if lattice == 'hex':
            # Hexagonal lattice: 6 other atoms in a hexagonal pattern.
            a, b = 0.5, np.sqrt(3)/2
            self.lattice_disp = np.array(
                    [[a,-b],[1,0],[a,b],[-a,b],[-1,0],[-a,-b]]).T
            self.phi = np.pi / 3
        elif lattice == 'square':
            # Square lattice: 4 other atoms placed orthogonally.
            self.lattice_disp = np.array([[1.,0],[0,1.],[-1.,0],[0,-1.]]).T
            self.phi = np.pi / 2
        else:
            raise Exception('Undefined lattice type: {}'.format(lattice))

        # Rotate the displacements by some random angle up to phi.
        self.setup_rotated_displacements()

    def setup_rotated_displacements(self):
        """Rotate atom displacements at random to change the orientation."""

        def _make_rot_matrix(alpha):
            return np.array([[np.cos(alpha), -np.sin(alpha)],
                             [np.sin(alpha), np.cos(alpha)]])
        
        
        #theta = np.random.rand() * self.phi
        theta = 0.0 # No rotation!
        
        # Two-dimensional rotation matrix.
        self.rot = _make_rot_matrix(theta)
        self.lattice_disp = (self.rot @ self.lattice_disp).T
        patch_rot = _make_rot_matrix(self.phi/2)
        if self.lattice == 'hex':
            a = 1 / np.sqrt(3)
        else:
            a = 1 / np.sqrt(2)
        self.patch_disp = a * (patch_rot @ self.lattice_disp.T).T
        
        
        
        
        
        
        
        