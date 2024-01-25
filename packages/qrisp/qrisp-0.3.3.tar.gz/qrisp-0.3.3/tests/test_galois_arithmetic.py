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


from qrisp import QuantumGalois, h, multi_measurement, cx
import numpy as np

def test_galois_arithmetic():
    
    #Test In-Place addition
    N = 13
    a = QuantumGalois(N)
    b = QuantumGalois(N)

    a[:] = 4
    h(b)
    a += b

    mes_res = multi_measurement([a,b])

    for k in mes_res.keys():
        if k[0] is np.nan or k[1] is np.nan:
            continue
        assert (4 + k[1])%N == k[0]
        
        
    a = QuantumGalois(N)
    b = 12

    h(a)
    temp = a.duplicate(init = True)
    a += b

    mes_res = multi_measurement([temp,a])

    for k in mes_res.keys():
        if k[0] is np.nan:
            continue
        assert (12 + k[0])%N == k[1]


        
    #Test In-Place subtraction
    a = QuantumGalois(N)
    b = QuantumGalois(N)

    a[:] = 4
    h(b)

    a -= b

    mes_res = multi_measurement([a,b])

    for k in mes_res.keys():
        if k[0] is np.nan or k[1] is np.nan:
            continue
        assert (4 - k[1])%N == k[0]


    a = QuantumGalois(N)
    b = 12

    h(a)
    temp = a.duplicate(init = True)
    a -= b

    mes_res = multi_measurement([temp,a])

    for k in mes_res.keys():
        if k[0] is np.nan:
            continue
        assert (-12 + k[0])%N == k[1]


        
    #Test Out-of-place addition
    a = QuantumGalois(N)
    b = QuantumGalois(N)

    h(a)
    h(b)

    res = a + b

    mes_res = multi_measurement([a,b, res])

    for k in mes_res.keys():
        if k[0] is np.nan or k[1] is np.nan:
            continue
        assert (k[0] + k[1])%N == k[2]
        

    a = QuantumGalois(N)

    a[:] = 9

    res = a + 10

    mes_res = multi_measurement([res])

    for k in mes_res.keys():
        if k[0] is np.nan:
            continue
        assert (9+10)%N == k[0]


    #Test Out-of-place subtraction
    a = QuantumGalois(N)
    b = QuantumGalois(N)

    h(a)
    h(b)

    res = a - b

    mes_res = multi_measurement([a,b, res])

    for k in mes_res.keys():
        if k[0] is np.nan or k[1] is np.nan:
            continue
        assert (k[0] - k[1])%N == k[2]
        

    a = QuantumGalois(N)
    a[:] = 2
    b = 7

    res = a - b

    mes_res = multi_measurement([res])

    for k in mes_res.keys():
        if k[0] is np.nan:
            continue
        assert (2-7)%N == k[0]

    #Test multiplication
    a = QuantumGalois(N)
    b = QuantumGalois(N)

    h(a)
    h(b)

    res = a*b

    mes_res = multi_measurement([a,b, res])

    for k in mes_res.keys():
        if k[0] is np.nan or k[1] is np.nan:
            continue
        assert (k[0]*k[1])%N == k[2]

    a = QuantumGalois(N)

    h(a)
    b = 5

    res = a*b

    mes_res = multi_measurement([a,res])

    for k in mes_res.keys():

        if k[0] is np.nan:
            continue
        assert (k[0]*5)%N == k[1]
    #Test in-place multiplication

    
    
    for i in range(1, N):
        a = QuantumGalois(N)
        h(a)
        b = a.duplicate()
        cx(a, b)
    
        a *= i
        print(i)
    
        mes_res = multi_measurement([b,a])
    
        for k in mes_res.keys():
            if k[1] is np.nan or k[0] is np.nan:
                continue
            assert (k[0]*i)%N == k[1]
