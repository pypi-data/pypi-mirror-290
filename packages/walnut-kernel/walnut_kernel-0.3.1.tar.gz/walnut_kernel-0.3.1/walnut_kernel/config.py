import os
from pathlib import Path as P

WALNUT_JAR = None
WALNUT_HOME = None


def setup_path():
    global WALNUT_HOME, WALNUT_JAR
    if "WALNUT_HOME" in os.environ:
        WALNUT_HOME = P(os.environ["WALNUT_HOME"])
    else:
        WALNUT_HOME = P(os.environ["HOME"])
    if not WALNUT_HOME.is_dir() or not (WALNUT_HOME / "Result").is_dir():
        raise RuntimeError(
            "Please define WALNUT_HOME and make it point to a writable directory containing Walnut runtime files"
        )
    if "WALNUT_JAR" in os.environ:
        WALNUT_JAR = P(os.environ["WALNUT_JAR"])
    else:
        WALNUT_JAR = WALNUT_HOME / "walnut.jar"
    if not WALNUT_JAR.is_file():
        raise RuntimeError(
            "Please define WALNUT_JAR and make it point to a Walnut main jar"
        )
