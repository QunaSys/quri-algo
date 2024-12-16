# Licensed under the MIT License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      https://mit-license.org/
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import unittest.mock
from typing import NamedTuple

import numpy as np
from quri_parts.core.operator import PAULI_IDENTITY, Operator
from quri_parts.core.state import CircuitQuantumState, quantum_state

import quri_algo.algo.phase_estimation.spe as spe
from quri_algo.core.estimator import OperatorPowerEstimatorBase
from quri_algo.core.estimator.time_evolution_estimator import (
    TimeEvolutionExpectationValueEstimator,
)
from quri_algo.problem import Problem, QubitHamiltonianInput


class _Estimate(NamedTuple):
    value: complex
    error: float = np.nan


class TestGaussianPhaseEstimation(unittest.TestCase):
    gaussian_algo: spe.GaussianFittingPhaseEstimation[Problem, CircuitQuantumState]
    gaussian_param: spe.GaussianParam
    a: float

    @classmethod
    def setUpClass(cls) -> None:
        int_boundary = 100
        n_discretize = 10000
        sigma = 1 / (np.sqrt(2 * np.pi))
        n_sample = 10000
        cls.gaussian_param = spe.GaussianParam(
            int_boundary, n_discretize, sigma, n_sample
        )

        cls.a = np.pi / 4

        estimator = unittest.mock.Mock(
            spec=OperatorPowerEstimatorBase[Problem, CircuitQuantumState],
            side_effect=lambda state, operator_power, n_shots: _Estimate(
                value=np.exp(-1j * operator_power * 2 * np.pi * cls.a)
            ),
        )
        cls.gaussian_algo = spe.GaussianFittingPhaseEstimation(estimator)

    def test_gaussian(self) -> None:
        search_range = np.linspace(self.a - np.pi * 3, self.a + np.pi * 3, 10000)
        input_state = quantum_state(1)
        result = self.gaussian_algo(input_state, self.gaussian_param, search_range, 0.8)
        assert np.isclose(result.value, self.a, atol=1e-8)


class TestGaussianGSEE(unittest.TestCase):
    gaussian_algo: spe.GaussianFittingPhaseEstimation[
        QubitHamiltonianInput, CircuitQuantumState
    ]
    gaussian_param: spe.GaussianParam
    shift: float
    tau: float

    @classmethod
    def setUpClass(cls) -> None:
        int_boundary = 100
        n_discretize = 10000
        sigma = 1 / (np.sqrt(2 * np.pi))
        n_sample = 10000
        cls.gaussian_param = spe.GaussianParam(
            int_boundary, n_discretize, sigma, n_sample
        )
        cls.shift = np.pi / 4

        time_evo_estimator = unittest.mock.Mock(
            spec=TimeEvolutionExpectationValueEstimator[
                QubitHamiltonianInput, CircuitQuantumState
            ],
            side_effect=lambda state, evolution_time, n_shots: _Estimate(
                value=np.exp(-1j * evolution_time * cls.shift)
            ),
        )
        time_evo_estimator.encoded_problem = QubitHamiltonianInput(
            1, Operator({PAULI_IDENTITY: 1})
        )

        cls.tau = 1 / 20
        cls.gaussian_algo = spe.GaussianFittingGSEE(time_evo_estimator, cls.tau)

    def test_gaussian_gsee(self) -> None:
        search_range = np.linspace(
            self.shift - np.pi * 3, self.shift + np.pi * 3, 10000
        )
        input_state = quantum_state(1)
        result = self.gaussian_algo(input_state, self.gaussian_param, search_range, 0.8)
        assert np.isclose(result.value, self.shift * self.tau, atol=1e-8)