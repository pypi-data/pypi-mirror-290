from enum import Enum, IntEnum
from pathlib import Path
from typing import Final, TypedDict, Optional

BRAND_NAME: Final[str] = "SynDB"

TEST_USERNAME: Final[str] = "caniko@syndb.xyz"
TEST_PASSWORD: Final[str] = "systar"

APP_DATA_DIR: Final[Path] = Path.home() / ".syndb"
APP_CACHE_DIR: Final[Path] = APP_DATA_DIR / "cache"
APP_GUI_CACHE_DIR: Final[Path] = APP_DATA_DIR / "gui"


class LocationConsent(IntEnum):
    NONE = 0
    CONTINENT_OK = 1
    CITY_OK = 2


class LocationInfo(TypedDict):
    continent: Optional[str]
    country: Optional[str]
    city: Optional[str]
