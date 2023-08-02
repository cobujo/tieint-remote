# there may not be much to put in here, depending on differences between local (dev) and production
from pathlib import Path
import os


def get_project_root():
    return Path(__file__).parent.parent


class Common:
    DB_DIR = os.path.join(get_project_root(), 'sql')


class Local(Common):
    DB_ENGINE_ECHO = False


class Production(Common):
    DB_ENGINE_ECHO = False
