
import logging
import os
import pprint

from audio_curation import audio_repo
from curation_utils import archive_utility
from audio_utils import mp3_utility


BASE_DIR = "/run/media/vvasuki/vData/audio/curation/git/shAstra-audio/sthAneshvara"
GENERIC_DESCRIPTION = """
Talks by sthAneshvar timalsIna.  
श्रवणसौकर्याय-रक्ष्यमाणम् अत्र।  
भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/shaastra-audio/index.html
"""


if __name__ == '__main__':
  archive_utility.update_item(item_id="sarvAmnAya-intro", dir_path=os.path.join(BASE_DIR, "sarvAmnAya-intro"), metadata={"description":GENERIC_DESCRIPTION})
  pass