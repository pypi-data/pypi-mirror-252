# MIT License
#
# Copyright (c) [2023] [son pham, tien nguyen, bach bao]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Backend of the VM that can be used to simulate the Quantum Circuit
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List
from numpy.typing import NDArray
from src.quantumcircuit.QC import Qutrit_circuit
from src.quantumcircuit.qc_utility import statevector_to_state
from src.quantumcircuit.instruction_structure import Instruction


class QASM_Simulator:
    """
    The class is used to represent a vm_backend simulator in VM,
    A Quantum Circuit is given as input to the vm_backend and the final result is returned.
    """

    def __init__(self, qc: Qutrit_circuit) -> None:
        """

        :param qc:
        """
        self.circuit = qc
        self.n_qutrit = qc.n_qutrit
        self.initial_state = qc.initial_state
        self.state = self.initial_state
        self._measurement_flag = qc.measurement_flag
        self._operation_set = qc.operation_set
        self._SPAM_error = None
        self._error_meas: List = []
        self._measurement_result: List = []
        self._simulation_flag = False

    def add_SPAM_noise(self, p_prep: float, p_meas: float, error_type: str = 'Pauli_error') -> None:
        """

        Args:
            p_prep: Probability of preparation error
            p_meas: Probability of measurement error
            error_type: The type of error

        Adding State Preparation and Measurement noise to the backend

        """
        if error_type == 'Pauli_error':
            self._error_meas = [('x+', p_meas / 2), ('x-', p_meas / 2), ('I', 1 - p_meas)]
            error_prep = [('x+', p_prep / 2), ('x-', p_prep / 2), ('I', 1 - p_prep)]
            """
            Adding preparation error
            """
            probs_prep = [error_prep[i][1] for i in range(len(error_prep))]
            for i in range(self.n_qutrit):
                choice = np.random.choice(range(len(error_prep)), p=probs_prep)
                error_effect = Instruction(gate_type=error_prep[choice][0], n_qutrit=self.n_qutrit, first_qutrit_set=i,
                                           second_qutrit_set=None, parameter=None)
                self._operation_set.insert(__index=0, __object=error_effect)
            """
            Adding measurement error
            """
            self._SPAM_error = True
        else:
            pass

    def _simulation(self) -> None:
        """

        The simulation process of the vm_backend

        """

        if self._measurement_flag:
            for i in range(len(self._operation_set)-1):
                self.state = np.einsum('ij,jk', self._operation_set[i].effect_matrix, self.state)
        else:
            for i in self._operation_set:
                self.state = np.einsum('ij,jk', i.effect_matrix, self.state)
        self._simulation_flag = True

    def run(self, num_shots: int = 1024) -> None:
        """

        Args:
            num_shots: Number of shots

        Performs measurement through the defined amount of shots.

        """

        if self._simulation_flag is False:
            self._simulation()
        if self._measurement_flag:
            if self._SPAM_error:
                probs_prep = [self._error_meas[i][1] for i in range(len(self._error_meas))]
                for i in range(self.n_qutrit):
                    choice = np.random.choice(range(len(self._error_meas)), p=probs_prep)
                    error_effect = Instruction(gate_type=self._error_meas[choice][0], n_qutrit=self.n_qutrit,
                                               first_qutrit_set=i,
                                               second_qutrit_set=None, parameter=None)
                    self._operation_set.insert(__index=0, __object=error_effect)
            state_coeff, state_construction = statevector_to_state(self.state, self.n_qutrit)
            probs = [np.abs(i) ** 2 for i in state_coeff]
            for i in range(num_shots):
                measure = np.random.choice(range(len(state_construction)), p=probs)
                self._measurement_result.append(state_construction[measure])
        else:
            raise Exception("Your circuit does not contains measurement.")

    def get_counts(self) -> Dict:
        """

        Returns: count of each state

        """
        if self._measurement_result is not None:
            return dict((x, self._measurement_result.count(x)) for x in set(self._measurement_result))
        else:
            raise Exception("You have not made measurement yet.")

    def return_final_state(self) -> NDArray:
        """

        Returns: Final state of the quantum circuit

        """
        if self._simulation_flag is False:
            self._simulation()
        return self.state

    def result(self) -> List:
        """

        Returns: Measurement result

        """
        if self._measurement_result is not None:
            return self._measurement_result
        else:
            raise Exception("You have not made measurement yet.")

    def density_matrix(self) -> NDArray:
        """

        Returns: Density matrix of the current state of the quantum circuit

        """
        if self._simulation_flag is False:
            self._simulation()
        return self.state @ np.transpose(self.state)

    def plot(self, plot_type: str) -> None:
        """

        Args:
            plot_type: Type of plotting

        Returns: Draw graph

        """
        result_dict = self.get_counts()
        if plot_type == "histogram":
            plt.bar(result_dict.keys(), result_dict.values())
        elif plot_type == "line":
            plt.plot(result_dict.keys(), result_dict.values())
        elif plot_type == "dot":
            plt.scatter(result_dict.keys(), result_dict.values())
        else:
            raise Exception("Invalid plotting type!")
        plt.show()
