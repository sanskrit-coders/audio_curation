
import logging
import os
import pprint

from audio_curation import audio_repo, archive_utility
from audio_utils import mp3_utility


YT_BASE = "/mnt/vmedia/audio/curation/archive/yt-curation"



if __name__ == "__main__":
  archive_audio_item = archive_utility.ArchiveAudioItem(archive_id="GIPA_gokhale-institute-talks", repo_base=os.path.join(YT_BASE, "GIPA"))
  archive_audio_item.update_from_dir()
  pass
