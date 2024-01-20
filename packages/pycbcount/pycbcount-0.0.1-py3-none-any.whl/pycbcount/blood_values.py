"""Reference Ranges for Complete Blood Count.

This module defines the reference ranges for various complete blood count
metrics across different age groups.

| Metrics     | Units            |
| :---------- | :--------------- |
| WBC         | cells/µL         |
| RBC         | cells/µL         |
| HGB         | g/L              |
| HCT         | decimal fraction |
| HB          | g/dL             |
| MCV         | fL               |
| MCH         | pg               |
| MCHC        | g/dL             |
| RDW         | decimal fraction |
| PLT         | cells/µL         |
| Neutrophils | cells/µL         |
| Lymphocytes | cells/µL         |
| Monocytes   | cells/µL         |
| Eosinophils | cells/µL         |
| Basophils   | cells/µL         |
"""
from typing import Any, Union


class AgeGroupDict(dict):
    """A dictionary class that categorizes age-related data into age groups.

    This class extends the standard dictionary and allows accessing values by
    specifying either an age as an integer or an age group as a string.
    The age groups are defined as:

    `Neonate` (`age` <= 1), `Pediatric` (1 < `age` <= 7), `Adult` (`age` > 7).
    """

    def __getitem__(self, key: Union[int, str]) -> Any:
        """Get the item corresponding to the given age or age group.

        :param key: The key to look up in the dictionary. Can be an integer age
            or a string age group.
        :return: The value from the dictionary corresponding to the given key.
        :raises KeyError: If the key is not an integer or string, or if it is an
            integer but not a positive number, a KeyError is raised.
        """
        if isinstance(key, int):
            if key <= 1:
                age_group = "Neonate"
            elif key <= 7:
                age_group = "Pediatric"
            elif key > 7:
                age_group = "Adult"
            return super().__getitem__(age_group)
        if isinstance(key, str):
            # Handle age group input.
            return super().__getitem__(key)
        raise KeyError("Invalid input. Please provide an age or age group.")


reference_range = AgeGroupDict(
    {
        "Adult": {
            "WBC": (3.6e3, 10.6e3),
            "RBC": {"Male": (4.20e6, 6.00e6), "Female": (3.80e6, 5.20e6)},
            "HGB": {"Male": (135, 180), "Female": (120, 150)},
            "HCT": {"Male": (0.40, 0.54), "Female": (0.35, 0.49)},
            "HB": (13.3 - 16.7),
            "MCV": (80, 100),
            "MCH": (26, 34),
            "MCHC": (32.0, 36.0),
            "RDW": (0.115, 0.145),
            "PLT": (150e3, 450e3),
            "Neutrophils": (1.7e3, 7.5e3),
            "Lymphocytes": (1.0e3, 3.2e3),
            "Monocytes": (0.1e3, 1.3e3),
            "Eosinophils": (0.0e3, 0.3e3),
            "Basophils": (0.0e3, 0.2e3),
        },
        "Pediatric": {
            "WBC": (5.0e3, 17.0e3),
            "RBC": (4.00e6, 5.20e6),
            "HGB": (102, 152),
            "HCT": (0.36, 0.46),
            "HB": "TBD",
            "MCV": (78, 94),
            "MCH": (23, 31),
            "MCHC": (320, 360),
            "RDW": (0.115, 0.145),
            "PLT": (150e3, 450e3),
            "Neutrophils": (1.5e3, 11.0e3),
            "Lymphocytes": (1.5e3, 11.1e3),
            "Monocytes": (0.1e3, 1.9e3),
            "Eosinophils": (0.0e3, 0.7e3),
            "Basophils": (0.0e3, 0.3e3),
        },
        "Neonate": {
            "WBC": (9.0e3, 37.0e3),
            "RBC": (4.10e6, 6.10e6),
            "HGB": (165, 215),
            "HCT": (0.48, 0.68),
            "HB": "TBD",
            "MCV": (95, 125),
            "MCH": (30, 42),
            "MCHC": (300, 340),
            "RDW": "TBD",
            "PLT": (150e3, 450e3),
            "Neutrophils": (3.7e3, 30.0e3),
            "Lymphocytes": (1.6e3, 14.1e3),
            "Monocytes": (0.1e3, 4.4e3),
            "Eosinophils": (0.0e3, 1.5e3),
            "Basophils": (0.0e3, 0.7e3),
        },
    }
)
