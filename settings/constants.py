# - plural items should be an iterable, single items should be a non-iterable
# * this may be temporary, as it might be best to store some of these names in the db as it grows
from dataclasses import dataclass
from typing import Union

# *** COMWRAPPER DELAY, TIMEOUT VALUES ***
COM_DELAY = 0.10
COM_TIMEOUT = 30

# *** CODING CONSTANTS ***
SPACE_ATTR_NAME = 'space_'



# *** CONSTANT CLASSES ***
@dataclass
class POCCallout(object):
    block_name: str
    ref_attr: str


MECH_SCHEMATIC_TPOCS = (
    POCCallout('FM_POCM', 'FM'),
    POCCallout('M_TPOC', 'TPOC')
)

# *** AUTOCAD CONSTANTS ***

TITLE_BLOCK_NAME_SSOE = 'i2436SHT'

REV_STRIP_NAME_SSOE = 'i2436RD'

TITLE_BLOCK_REQUIRED_ATTR = 'DWG#'

OWNED_DWG_BLOCK_NAME = 'SSOE_LOGO'

IFR_BLOCK_NAME = 'issue for reference'

NFC_BLOCK_NAME = 'NotForConstruction'
