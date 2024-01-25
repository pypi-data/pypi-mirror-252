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


from qrisp.interface import BackendServer, BackendClient
from qrisp import QuantumVariable, QuantumCircuit, h, x, cx


def test_interface():
    def run_func(qc, shots, token):
        print("Recieved query")

        # Convert to qiskit
        from qrisp.interface.circuit_converter import convert_circuit
        
        qiskit_qc = convert_circuit(qc, "qiskit")

        print(qiskit_qc)

        from qiskit import Aer

        qiskit_backend = Aer.get_backend("qasm_simulator")

        # Run Circuit on the Qiskit backend
        return qiskit_backend.run(qiskit_qc, shots=shots).result().get_counts()

    # socket_ip = "::"
    socket_ip = "127.0.0.1"
    port = 9123

    test_server = BackendServer(run_func, socket_ip_address=socket_ip, port=port)

    test_server.start()

    qv1 = QuantumVariable(2)
    qv2 = QuantumVariable(2)

    h(qv1[0])
    x(qv1[1])
    cx(qv1[0], qv2[1])

    test_client = BackendClient(socket_ip, port)

    res = qv1.get_measurement(backend=test_client)
    assert "01" in res.keys() and "11" in res.keys()
