#!/usr/bin/python3
# Nicholas M. Rathmann <rathmann@nbi.ku.dk>, 2022-2024

import copy, sys, time, code # code.interact(local=locals())
import numpy as np

from .. import constants as sfconst
from .CPO import *
from .enhancementfactor import *

class IceFabric(CPO):

    def __init__(self, mesh, boundaries, L=8, nu_realspace=1e-3, nu_multiplier=1, modelplane='xz', ds=None, nvec=None, \
                        Eij_grain=(1,1), alpha=0, n_grain=1, \
                        Cij=sfconst.ice['elastic']['Bennett1968'], rho=sfconst.ice['density']): 

        super().__init__(mesh, boundaries, L, nu_multiplier=nu_multiplier, nu_realspace=nu_realspace, modelplane=modelplane, ds=ds, nvec=nvec)
        self.initialize(wr=None) # isotropic
        self.set_BCs([], [], []) # no BCs

        self.grain_params = (Eij_grain, alpha, n_grain)
        self.Lame_grain = self.sf.Cij_to_Lame_tranisotropic(Cij) 
        self.rho = rho

        self.enhancementfactor = EnhancementFactor(mesh, L, modelplane=modelplane)
        self.update_Eij()
                
    def get_state(self, *args, **kwargs): 
        return self.get_nlm(*args, **kwargs) # alias
        
    def evolve(self, *args, **kwargs):
        super().evolve(*args, **kwargs)
        self.update_Eij()

    def solvesteady(self, u, S, **kwargs):
        super().evolve(u, S, 1, steadystate=True, **kwargs)
        self.update_Eij()
        
    def update_Eij(self):
        self.mi, self.Eij, self.ai = self.enhancementfactor.Eij_tranisotropic(self.w, *self.grain_params, ei_arg=())
        self.xi, self.Exij, _      = self.enhancementfactor.Eij_tranisotropic(self.w, *self.grain_params, ei_arg=np.eye(3))
        # ... unpack
        self.m1, self.m2, self.m3 = self.mi # <c^2> eigenvectors (presumed fabric and rheological symmetry directions)
        self.E11, self.E22, self.E33, self.E23, self.E31, self.E12 = self.Eij  # eigenenhancements
        self.Exx, self.Eyy, self.Ezz, self.Eyz, self.Exz, self.Exy = self.Exij # Cartesian enhancements
        self.a1, self.a2, self.a3 = self.ai # <c^2> eigenvalues (fabric eigenvalues)
            
    def get_elastic_velocities(self, x,y, theta,phi, alpha=1):
        nlm = self.get_state(x,y)
        vS1, vS2, vP = sf__.Vi_elastic_tranisotropic(nlm, alpha,self.Lame_grain,self.rho, theta,phi) # calculate elastic phase velocities using specfab
        return (vP, vS1, vS2)
        
    def Gamma0_Lilien(self, u, T, A=4.3e7, Q=3.36e4):
        # DDRX rate factor from Dome C ice-core calibration experiment (Lilien et al., 2023, p. 7)
        R = Constant(8.314) # gas constant (J/mol*K)
        D = sym(grad(u))
        epsE = sqrt(inner(D,D)/2)
        return project(epsE*Constant(A)*exp(-Constant(Q)/(R*T)), self.R)

# @TODO
#    def Gamma0_Richards(self, ):
#        # DDRX rate factor from lab calibration experiments (Richards et al, 2021)
        
        
