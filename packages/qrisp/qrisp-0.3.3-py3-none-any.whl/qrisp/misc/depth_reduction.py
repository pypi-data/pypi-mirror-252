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


# Modification to Kahns algorithm to reduce the depth of general circuits by applying
# trivial and non-trivial commutation relations based on the dag representation of
# unqomp.

import networkx as nx
import numpy as np
from numba import njit

from qrisp.uncomputation.unqomp import dag_from_qc

def qb_set_to_int(qubits, qc):
    res = 0
    for qb in qubits:
        res |= 1 << qc.qubits.index(qb)
    return res

def qb_set_to_int(qubits, qc):
    qb_indices = [qc.qubits.index(qb) for qb in qubits]
    return split_integer(qb_indices, int(np.ceil(qc.num_qubits()/64)))

def split_integer(digit_list, k):
    
    digit_list.sort()
    
    if k <= 0:
        raise ValueError("Parameter k must be greater than zero")

    result = [0]*k
    i = 0
    for d in digit_list:
        if d > 64*(i+1):
            i += 1
        result[i] |= (1<<(d%64))
        if result[i] >= 1<<64:
            raise
        
    return result


# Kahns Algorithm based on
# https://www.geeksforgeeks.org/topological-sorting-indegree-based-solution/
def depth_sensitive_topological_sort(indices, indptr, int_qc, num_qubits, depth_indicators):
    # Create a vector to store indegrees of all
    # vertices. Initialize all indegrees as 0.
    n = len(indptr) - 1
    in_degree = np.zeros(n, dtype=np.int32)

    depths = np.zeros(num_qubits, dtype=np.int32)
    # Traverse adjacency lists to fill indegrees of
    # vertices.  This step takes O(V + E) time

    for i in range(n):
        for j in indices[indptr[i] : indptr[i + 1]]:
            in_degree[j] += 1

    # Create a queue and enqueue all vertices with
    # indegree 0
    queue = []

    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)

    # Initialize count of visited vertices
    cnt = 0

    # Create a vector to store result (A topological
    # ordering of the vertices)
    top_order = np.zeros(n, dtype=np.int32)

    # One by one dequeue vertices from queue and enqueue
    # adjacents if indegree of adjacent becomes 0

    while queue:
        # The depth sensitive part is now to deque the node with the least depth
        node_costs = np.zeros(len(queue))

        for i in range(len(queue)):
            node = queue[i]

            qubits = int_qc[node]

            depth_sum = 0
            
            for j in range(num_qubits):
                if qubits[j//64] & 1 << (j%64):
                    depth_sum += depths[j]

            node_costs[i] = depth_sum

        u = queue.pop(np.argmin(node_costs))

        top_order[cnt] = u

        # Update depths array
        max_depth = 0

        for i in range(num_qubits):
            if int_qc[u, i//64] & 1 << (i%64):
                if depths[i] > max_depth:
                    max_depth = depths[i]

        for i in range(num_qubits):
            if int_qc[u, i//64] & 1 << (i%64):
                depths[i] = max_depth + depth_indicators[u]

        # Update in degree array
        for i in indices[indptr[u] : indptr[u + 1]]:
            in_degree[i] -= 1
            if in_degree[i] == 0:
                queue.append(i)

        cnt += 1

    return top_order


depth_sensitive_topological_sort_jitted = njit(cache=True)(
    depth_sensitive_topological_sort
)


def parallelize_qc(qc, depth_indicator = None):
    if len(qc.data) <= 1:
        return qc.copy()
    
    if depth_indicator is None:
        depth_indicator = lambda x : 1

    dag = dag_from_qc(qc, remove_init_nodes=True)

    sprs_mat = nx.to_scipy_sparse_array(dag, format="csr")

    node_list = list(dag.nodes())
    
    qubit_ints = []
    depth_indicators = []
    for n in node_list:
        qubit_ints.append(qb_set_to_int(n.instr.qubits, qc))
        depth_indicators.append(depth_indicator(n.instr.op))
    
    qubit_ints = np.array(qubit_ints, dtype = np.uint64)

    res = depth_sensitive_topological_sort_jitted(
        sprs_mat.indices, sprs_mat.indptr, qubit_ints, num_qubits=qc.num_qubits(), depth_indicators = np.array(depth_indicators)
    )

    qc_new = qc.clearcopy()

    for i in range(len(res)):
        qc_new.append(node_list[res[i]].instr)

    return qc_new
