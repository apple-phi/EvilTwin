import pathlib
import collections
import toml

SAVEFILE = pathlib.Path(__file__).parent / "save.toml"
SAVEFILE.touch()


class _UserData(collections.UserDict):
    def __init__(self):
        self.data = toml.load(SAVEFILE)

    def save(self):
        assert all(
            isinstance(key, str) for key in self.data
        ), "all TOML keys must be strings."
        with SAVEFILE.open("w") as f:
            toml.dump(self.data, f)

    def unlocked(self, level: int) -> bool:
        return str(level - 1) in self or level == 0

    def unlock(self, level: int):
        self[str(level)] = 0

    def stars_in(self, level: int, default=None):
        return self.get(str(level), default)


user_data = _UserData()
