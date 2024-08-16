from collections import UserDict
from typing import Any

import rtoml


class Config(UserDict):
    def __init__(self, config_file: str) -> None:
        try:
            with open(config_file, "r", encoding="utf8") as f:
                self.config = rtoml.load(f)
        except IOError as e:
            print(e)

        super().__init__(self)

    def __getitem__(self, key: Any) -> Any:
        return self.config[key]
