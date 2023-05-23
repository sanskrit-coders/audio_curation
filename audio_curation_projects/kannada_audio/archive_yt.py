
import logging
import os
import pprint

from audio_curation import audio_repo
from curation_utils import archive_utility
from audio_utils import mp3_utility



YT_BASE = "/run/media/vvasuki/vData/audio/curation/archive/"
DESCRIPTION_BASE = """
श्रवणसौकर्याय-रक्ष्यमाणम् अत्र।  
भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/
"""

def shorts():
  # archive_utility.update_item(item_id="kannada-short-lectures", dir_path=os.path.join(YT_BASE, "kannada-short-lectures"), metadata={"title": "Kannada Short lectures", "description": "ಕನ್ನಡದಲ್ಲಿ ಲಘು-ಲೇಖಗಳು ಲಘು-ಭಾಷಣಗಳು\n\n" + DESCRIPTION_BASE})
  archive_utility.update_item(item_id="kannada_short_stories_tts", dir_path=os.path.join(YT_BASE, "kannada_short_stories_tts"), metadata={"title": "Kannada Short Stories", "description": "ಕನ್ನಡದಲ್ಲಿ ಲಘು-ಕಥೆಗಳು\n\n" + DESCRIPTION_BASE})


if __name__ == "__main__":
  shorts()
  pass
