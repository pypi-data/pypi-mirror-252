# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

import importlib
from pathlib import Path
import types

from specker.loader import SpecLoader

class StaticSpecker:
    """Static Specker Instance for Performance
    """
    _specker:SpecLoader
    instance:"StaticSpecker"

    @property
    def specker_instance(self) -> SpecLoader:
        """Specker Instance
        @retval SpecLoader Specker Instance
        """
        return self._specker

    def __init__(self) -> None:
        StaticSpecker.instance = self
        self._specker = SpecLoader(Path(__file__).resolve().parent.joinpath("specs"),False)
        StaticSpecker.load_specs()

    @staticmethod
    def load_specs() -> None:
        """Scan Common Modules for Specs
        @retval None Nothing
        """
        modules:list[str] = [ "convection.shared", "convection.secrets.client", "convection.secrets.server", "convection_core" ]
        for m_name in modules:
            try:
                m_obj:types.ModuleType = importlib.import_module(m_name)
                p:Path  = Path(m_obj.__path__[0]).resolve().joinpath("specs")
                StaticSpecker.instance.specker_instance.load_specs(p)
            except ModuleNotFoundError:
                continue
