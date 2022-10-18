
import logging
import os
import pprint

from audio_curation import audio_repo
from curation_utils import archive_utility
from audio_utils import mp3_utility


YT_BASE = "/mnt/vmedia/audio/curation/archive/yt-curation"



if __name__ == "__main__":
  archive_utility.update_item(item_id="GIPA_gokhale-institute-talks", dir_path=os.path.join(YT_BASE, "GIPA"))
  # archive_utility.update_item(item_id="duShyanth-shrIdhar-talks", dir_path=os.path.join(YT_BASE, "duShyanth-shrIdhar-talks"))
  # archive_utility.update_item(item_id="gspk_stotra-pArAyaNa-kainkaryam", dir_path=os.path.join(YT_BASE, "gspk_stotra-pArAyaNa-kainkaryam"))
  # archive_utility.update_item(item_id="rAmAnuja-dayA-audio", dir_path=os.path.join(YT_BASE, "rAmAnuja-dayA"))
  pass
