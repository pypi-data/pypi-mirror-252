# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Fake Boeblingen device (20 qubit).
"""

import os
from qiskit.providers.fake_provider import fake_pulse_backend, fake_backend


class FakeBoeblingenV2(fake_backend.FakeBackendV2):
    """A fake Boeblingen V2 backend.

    .. code-block:: text

        00 ↔ 01 ↔ 02 ↔ 03 ↔ 04
              ↕         ↕
        05 ↔ 06 ↔ 07 ↔ 08 ↔ 09
         ↕         ↕         ↕
        10 ↔ 11 ↔ 12 ↔ 13 ↔ 14
              ↕         ↕
        15 ↔ 16 ↔ 17 ↔ 18 ↔ 19
    """

    dirname = os.path.dirname(__file__)
    conf_filename = "conf_boeblingen.json"
    props_filename = "props_boeblingen.json"
    defs_filename = "defs_boeblingen.json"
    backend_name = "fake_boeblingen"


class FakeBoeblingen(fake_pulse_backend.FakePulseBackend):
    """A fake Boeblingen backend.

    .. code-block:: text

        00 ↔ 01 ↔ 02 ↔ 03 ↔ 04
              ↕         ↕
        05 ↔ 06 ↔ 07 ↔ 08 ↔ 09
         ↕         ↕         ↕
        10 ↔ 11 ↔ 12 ↔ 13 ↔ 14
              ↕         ↕
        15 ↔ 16 ↔ 17 ↔ 18 ↔ 19
    """

    dirname = os.path.dirname(__file__)
    conf_filename = "conf_boeblingen.json"
    props_filename = "props_boeblingen.json"
    defs_filename = "defs_boeblingen.json"
    backend_name = "fake_boeblingen"
