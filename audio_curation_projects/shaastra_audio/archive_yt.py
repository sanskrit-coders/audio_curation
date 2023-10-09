
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

def shrii_vaishnava():
  # archive_utility.update_item(item_id="duShyanth-shrIdhar-talks", dir_path=os.path.join(YT_BASE, "duShyanth-shrIdhar-talks"))
  # archive_utility.update_item(item_id="gspk_stotra-pArAyaNa-kainkaryam", dir_path=os.path.join(YT_BASE, "gspk_stotra-pArAyaNa-kainkaryam"))

  # youtube.get_all(url="https://www.youtube.com/@ramanujadaya8750/videos", dest_dir=os.path.join(YT_BASE, "rAmAnuja-dayA"), postprocessor_args={"metadata": {"albumartist": "rAmAnuja-dayA"}})
  # archive_utility.update_item(item_id="rAmAnuja-dayA-audio", dir_path=os.path.join(YT_BASE, "rAmAnuja-dayA"))
  # archive_utility.update_item(item_id="tattva-muktA-kalApaH_ALvAr", dir_path=os.path.join(YT_BASE, "tattva-muktA-kalApaH_ALvAr"), metadata={"title": "tattva-muktA-kalApaH - ALvAr", "description": "तत्त्व-मुक्ता-कलापः - आळ्वार्-पाठः\n\n" + DESCRIPTION_BASE})

  # youtube.get_all(url="https://www.youtube.com/@parankushacharinstituteofvedic/videos", dest_dir=os.path.join(YT_BASE, "PISV"), postprocessor_args={"metadata": {"albumartist": "pisvTalks"}})
  # archive_utility.update_item(item_id="pisvTalks", dir_path=os.path.join(YT_BASE, "PISV"), metadata={"title": "PISV Talks", "description": "पराङ्कुशाचार्य-वैदिक-शोध-संस्था-धारा-भाषणानि\n\n" + DESCRIPTION_BASE})


  # youtube.get_all(url="https://www.youtube.com/@desikadaily/videos", dest_dir=os.path.join(YT_BASE, "deshika-daily"), postprocessor_args={"metadata": {"albumartist": "deshika-daily"}})
  archive_utility.update_item(item_id="deshika-daily", dir_path=os.path.join(YT_BASE, "deshika-daily"), metadata={"title": "deshika-daily talks", "description": "देशिक-दैनिक-धारा-भाषणानि\n\n" + DESCRIPTION_BASE})
  pass


def dhaarmika_lectures():
  pass
  # archive_utility.update_item(item_id="GIPA_gokhale-institute-talks", dir_path=os.path.join(YT_BASE, "GIPA"))
  # archive_utility.update_item(item_id="pparikh-talks", dir_path=os.path.join(YT_BASE, "prashAnt-pArikh"), metadata={"title": "P Parikh interviews", "description": "Source: Prashant Parikh's YT channel\n\n" + DESCRIPTION_BASE})
  # yt-dlp --continue --no-overwrites --extract-audio --audio-format mp3 -o "ST_%(upload_date)s_%(title).50s.%(ext)s" https://www.youtube.com/channel/UC3nhAUpe7aBm1rFCBgoWWcA/videos --playlist-reverse --restrict-filenames   --add-metadata --postprocessor-args "-metadata artist=SrijanTalks" --download-archive ./ytdl-archive.txt --dateafter 
  # youtube.get_all(url="https://www.youtube.com/channel/UC3nhAUpe7aBm1rFCBgoWWcA/videos", dest_dir=os.path.join(YT_BASE, "srijan"), postprocessor_args={"metadata": {"albumartist": "SrijanTalks"}})


def misc():
  pass
  # archive_utility.update_item(item_id="vyAsarAja-maTha-lectures", dir_path=os.path.join(YT_BASE, "vyAsarAjamaTha"))
  # archive_utility.update_item(item_id="viShNu-purANa-taylor", dir_path=os.path.join(YT_BASE, "../viShNu-purANa-taylor"))


if __name__ == "__main__":
  shrii_vaishnava()
  # dhaarmika_lectures()
  pass
