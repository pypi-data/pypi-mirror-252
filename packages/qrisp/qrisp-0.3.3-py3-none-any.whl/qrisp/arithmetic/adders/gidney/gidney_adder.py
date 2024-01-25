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

from qrisp.arithmetic.adders.gidney.cq_gidney_adder import *
from qrisp.arithmetic.adders.gidney.qq_gidney_adder import *
from qrisp.environments import custom_control

def gidney_adder(a, b, c_in = None, c_out = None, ctrl = None):
    
    if isinstance(a, (int, str)):
        return custom_control(cq_gidney_adder)(a, b, c_in = c_in, c_out = c_out, ctrl = ctrl)
    else:
        return qq_gidney_adder(a, b, c_in = c_in, c_out = c_out)
        
    