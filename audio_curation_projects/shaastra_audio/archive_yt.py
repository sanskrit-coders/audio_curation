
import logging
import os
import pprint

from audio_curation import audio_repo
from curation_utils import archive_utility
from audio_utils import mp3_utility



YT_BASE = "/run/media/vvasuki/vData/audio/curation/archive/yt-curation"


def shrii_vaishnava():
  archive_utility.update_item(item_id="duShyanth-shrIdhar-talks", dir_path=os.path.join(YT_BASE, "duShyanth-shrIdhar-talks"))
  archive_utility.update_item(item_id="gspk_stotra-pArAyaNa-kainkaryam", dir_path=os.path.join(YT_BASE, "gspk_stotra-pArAyaNa-kainkaryam"))
  archive_utility.update_item(item_id="rAmAnuja-dayA-audio", dir_path=os.path.join(YT_BASE, "rAmAnuja-dayA"))


if __name__ == "__main__":
  # archive_utility.update_item(item_id="GIPA_gokhale-institute-talks", dir_path=os.path.join(YT_BASE, "GIPA"))
  archive_utility.update_item(item_id="vyAsarAja-maTha-lectures", dir_path=os.path.join(YT_BASE, "vyAsarAjamaTha"))
  # archive_utility.update_item(item_id="viShNu-purANa-taylor", dir_path=os.path.join(YT_BASE, "../viShNu-purANa-taylor"))
  # shrii_vaishnava()
  pass
