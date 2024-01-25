"""
\********************************************************************************
* Copyright (c) 2023 the Qrisp authors
*
* This program and the accompanying materials are made available under the
* terms of the Eclipse Public License 2.0 which is available at
* http://www.eclipse.org/legal/epl-2.0.
*
* This Source Code may also be made available under the following Secondary
* Licenses when the conditions for such availability set forth in the Eclipse
* Public License, v. 2.0 are satisfied: GNU General Public License, version 2
* with the GNU Classpath Exception which is
* available at https://www.gnu.org/software/classpath/license.html.
*
* SPDX-License-Identifier: EPL-2.0 OR GPL-2.0 WITH Classpath-exception-2.0
********************************************************************************/
"""

import numpy as np

from qrisp.qtypes.quantum_float import QuantumFloat
from qrisp.environments import invert
from qrisp.arithmetic.galois_arithmetic import (montgomery_mod_mul, 
                              montgomery_mod_semi_mul, 
                              semi_cl_inpl_mult,
                              montgomery_decoder,
                              beauregard_adder)

class QuantumGalois(QuantumFloat):
    
    def __init__(self, modulus, qs = None):
        
        self.m = int(np.ceil(np.log2(modulus)))
        
        self.modulus = modulus
        
        QuantumFloat.__init__(self, msize = self.m, qs = qs)
        self.m = 0
    
    def decoder(self, i):
        if i >= self.modulus:# or (np.gcd(i, self.modulus) != 1 and i != 0):
            return np.nan
        return montgomery_decoder(i, 2**self.m, self.modulus)
    
    def __mul__(self, other):
        if isinstance(other, QuantumGalois):
            return montgomery_mod_mul(self, other)
        elif isinstance(other, int):
            if isinstance(other, int):
                other = self.encoder(other)
            
            return montgomery_mod_semi_mul(self, other)
        else:
            raise Exception("Quantum modular multiplication with type {type(other)} not implemented")
            
    __rmul__ = __mul__
    
    def __imul__(self, other):
        if isinstance(other, int):
            
            other = self.encoder(other)
            
            return semi_cl_inpl_mult(self, other%self.modulus)
        else:
            raise Exception("Quantum modular multiplication with type {type(other)} not implemented")
    
    def __add__(self, other):
        if isinstance(other, int):
            other = self.encoder(other)
        
        res = self.duplicate(init = True)
        
        beauregard_adder(res, other, self.modulus)
        
        return res
    
    __radd__ = __mul__
    
    
    def __iadd__(self, other):
        if isinstance(other, int):
            other = self.encoder(other)
        
        beauregard_adder(self, other, self.modulus)
        return self
    
    
    def __sub__(self, other):
        if isinstance(other, int):
            other = self.encoder(other)
        
        res = self.duplicate(init = True)
        
        with invert():
            beauregard_adder(res, other, self.modulus)
        
        return res
    
    def __rsub(self, other):
        if isinstance(other, int):
            other = self.encoder(other)
        res = self.duplicate()
        
        res -= self
        
        beauregard_adder(res, other, self.modulus)
        
        return res
        
    
    def __isub__(self, other):
        if isinstance(other, int):
            other = self.encoder(other)
        
        with invert():
            beauregard_adder(self, other, self.modulus)
        
        return self



        