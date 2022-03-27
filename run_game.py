import io, contextlib

from pkg_resources import DistributionNotFound

try:
    with contextlib.redirect_stdout(io.StringIO()):
        import toml, pygame, numpy
except ImportError as e:
    raise ModuleNotFoundError(
        "Required modules for the game not found. Please run `pip install -r requirements.txt`."
    ) from e

try:
    import EvilTwin.__main__
except ImportError as e:
    raise DistributionNotFound(
        "You must have your current working directory set to the directory containing the README.md"
    ) from e
