
from generalimport import generalimport
generalimport("pandas")

from generalfile.path import Path
from generalfile.configfile import ConfigFile
from generalfile.errors import CaseSensitivityError, InvalidCharacterError

Path.get_lock_dir().create_folder()
