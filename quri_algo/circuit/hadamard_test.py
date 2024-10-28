# Licensed under the MIT License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      https://mit-license.org/
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from typing import Any, Optional

from quri_parts.circuit import NonParametricQuantumCircuit, QuantumCircuit

from quri_algo.circuit.interface import ProblemCircuitFactory
from quri_algo.circuit.utils.transpile import apply_transpiler
from quri_algo.problem import ProblemT


@dataclass
class HadamardTestCircuitFactory(ProblemCircuitFactory[ProblemT]):
    test_real: bool
    controlled_circuit_factory: ProblemCircuitFactory[ProblemT]

    @apply_transpiler  # type: ignore
    def __call__(self, *args: Any, **kwds: Any) -> NonParametricQuantumCircuit:
        return construct_hadamard_circuit(
            self.controlled_circuit_factory(*args, **kwds), self.test_real
        )


def construct_hadamard_circuit(
    time_evolution_circuit: NonParametricQuantumCircuit,
    test_real: bool,
    preprocess_circuit: Optional[NonParametricQuantumCircuit] = None,
    postprocess_circuit: Optional[NonParametricQuantumCircuit] = None,
) -> NonParametricQuantumCircuit:
    circuit = QuantumCircuit(time_evolution_circuit.qubit_count)
    circuit.add_H_gate(0)
    if preprocess_circuit is not None:
        circuit += preprocess_circuit
    circuit += time_evolution_circuit
    if postprocess_circuit is not None:
        circuit += postprocess_circuit
    if not test_real:
        circuit.add_Sdag_gate(0)
    circuit.add_H_gate(0)
    return circuit
