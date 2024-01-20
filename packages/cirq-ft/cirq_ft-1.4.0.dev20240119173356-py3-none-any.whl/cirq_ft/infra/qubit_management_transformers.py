# Copyright 2023 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional

import cirq


@cirq._compat.deprecated(deadline="v1.4", fix="Use cirq.map_clean_and_borrowable_qubits instead.")
def map_clean_and_borrowable_qubits(
    circuit: cirq.AbstractCircuit, *, qm: Optional[cirq.QubitManager] = None
) -> cirq.Circuit:
    """This method is deprecated. See docstring of `cirq.map_clean_and_borrowable_qubits`"""
    return cirq.map_clean_and_borrowable_qubits(circuit, qm=qm)
