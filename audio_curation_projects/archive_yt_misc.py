
import logging
import os
import pprint

from audio_curation import audio_repo
from curation_utils import archive_utility
from audio_utils import mp3_utility
from audio_curation.scraping import youtube


YT_BASE = "/run/media/vvasuki/vData/audio/curation/archive/yt-curation"
DESCRIPTION_BASE = """
श्रवणसौकर्याय-रक्ष्यमाणम् अत्र।  
भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/
"""



def misc():
  pass
  # youtube.get_all(url="https://www.youtube.com/@TheRoyalInstitution/videos", dest_dir=os.path.join(YT_BASE, "royal-inst-yt-talks"), postprocessor_args={"metadata": {"albumartist": "Royal Institutution"}})
  # archive_utility.update_item(item_id="royal-inst-yt-talks", dir_path=os.path.join(YT_BASE, "royal-inst-yt-talks") , metadata={"title": "Royal Institution Public talks", "description": "Royal Institution Public talks - stored here for listening convenience.\n\n" + DESCRIPTION_BASE})


if __name__ == "__main__":
  misc()
  pass
