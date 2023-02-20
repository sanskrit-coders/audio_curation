
import logging
import os
import pprint

from audio_curation import audio_repo
from curation_utils import archive_utility
from audio_utils import mp3_utility



YT_BASE = "/run/media/vvasuki/vData/audio/curation/archive/yt-curation"
DESCRIPTION_BASE = """
श्रवणसौकर्याय-रक्ष्यमाणम् अत्र।  
भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/
"""

def shrii_vaishnava():
  # archive_utility.update_item(item_id="duShyanth-shrIdhar-talks", dir_path=os.path.join(YT_BASE, "duShyanth-shrIdhar-talks"))
  # archive_utility.update_item(item_id="gspk_stotra-pArAyaNa-kainkaryam", dir_path=os.path.join(YT_BASE, "gspk_stotra-pArAyaNa-kainkaryam"))
  # archive_utility.update_item(item_id="rAmAnuja-dayA-audio", dir_path=os.path.join(YT_BASE, "rAmAnuja-dayA"))
  archive_utility.update_item(item_id="tattva-muktA-kalApaH_ALvAr", dir_path=os.path.join(YT_BASE, "tattva-muktA-kalApaH_ALvAr"), metadata={"title": "tattva-muktA-kalApaH - ALvAr", "description": "तत्त्व-मुक्ता-कलापः - आळ्वार्-पाठः\n\n" + DESCRIPTION_BASE})


if __name__ == "__main__":
  # archive_utility.update_item(item_id="GIPA_gokhale-institute-talks", dir_path=os.path.join(YT_BASE, "GIPA"))
  # archive_utility.update_item(item_id="vyAsarAja-maTha-lectures", dir_path=os.path.join(YT_BASE, "vyAsarAjamaTha"))
  archive_utility.update_item(item_id="pparikh-talks", dir_path=os.path.join(YT_BASE, "prashAnt-pArikh"), metadata={"title": "P Parikh interviews", "description": "Source: Prashant Parikh's YT channel\n\n" + DESCRIPTION_BASE})
  # archive_utility.update_item(item_id="viShNu-purANa-taylor", dir_path=os.path.join(YT_BASE, "../viShNu-purANa-taylor"))
  # shrii_vaishnava()
  pass
