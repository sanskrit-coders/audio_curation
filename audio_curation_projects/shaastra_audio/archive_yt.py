
import logging
import os
import pprint

from audio_curation import audio_repo, archive_utility
from audio_utils import mp3_utility


YT_BASE = "/mnt/vmedia/audio/curation/archive/yt-curation"



if __name__ == "__main__":
  archive_utility.update_item(item_id="GIPA_gokhale-institute-talks", dir_path=os.path.join(YT_BASE, "GIPA"))
  pass
