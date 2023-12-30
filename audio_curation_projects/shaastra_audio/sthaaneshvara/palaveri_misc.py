
import logging
import os
import pprint

from audio_curation import audio_repo
from curation_utils import archive_utility
from audio_utils import mp3_utility


BASE_DIR = "/run/media/vvasuki/vData/audio/curation/git/shAstra-audio/palaveri-laxmI-narasiMhaH/"
GENERIC_DESCRIPTION = """
पलवेरि-लक्ष्मीनारायणार्य बोधनानि।  
**अधिकारिभिर् एव तद्-अनुज्ञया श्राव्यम्, नेतरैर्** इति प्रवक्तुर् निर्बन्धः।  
श्रवणसौकर्याय-रक्ष्यमाणम् अत्र।  
भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/shaastra-audio/index.html
"""


if __name__ == '__main__':
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_RTS", dir_path=os.path.join(BASE_DIR, "rahasya-traya-sAraH"), metadata={"description":GENERIC_DESCRIPTION})
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_BS", dir_path=os.path.join(BASE_DIR, "brahma-sUtram"), metadata={"description":GENERIC_DESCRIPTION})
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_BV", dir_path=os.path.join(BASE_DIR, "bhagavad-viShayam"), metadata={"description":GENERIC_DESCRIPTION})
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_AhAra-niyamaH", dir_path=os.path.join(BASE_DIR, "AhAra-niyamaH"), metadata={"description":GENERIC_DESCRIPTION})
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_rAmAyaNam_2023", dir_path=os.path.join(BASE_DIR, "rAmAyaNam_2023"), metadata={"description":GENERIC_DESCRIPTION})

  pass