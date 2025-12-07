
import logging
import os
import pprint

import regex

from audio_curation import audio_repo
from audio_curation import archive_utility as audio_archive_utility
from curation_utils import archive_utility
from audio_utils import mp3_utility
from audio_curation.scraping import youtube

ARCHIVE_BASE = "/media/vvasuki/vData/audio/curation/archive"
YT_BASE = "/media/vvasuki/vData/audio/curation/archive/yt-curation"
DESCRIPTION_BASE = """
श्रवणसौकर्याय-रक्ष्यमाणम् अत्र।  
भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/
"""

def shrii_vaishnava(actions=["download", "upload"], channel_pattern=".*"):

  # https://www.youtube.com/@DesikanAdiyar
  if regex.match(channel_pattern, "@DesikanAdiyar"):
    if "download" in actions:
      youtube.get_all(url="https://www.youtube.com/@DesikanAdiyar/videos", dest_dir=os.path.join(YT_BASE, "DesikanAdiyar"), postprocessor_args={"metadata": {"albumartist": "देशिक-दासाः"}})
    if "upload" in actions:
      archive_utility.update_item(item_id="DesikanAdiyar_YT", dir_path=os.path.join(YT_BASE, "DesikanAdiyar"), metadata={"title": "DesikanAdiyar talks", "description": "DesikanAdiyar-भाषणानि\n\n" + DESCRIPTION_BASE})

  if regex.match(channel_pattern, "@APNSWAMI"):
    if "download" in actions:
      youtube.get_all(url="https://www.youtube.com/@APNSWAMI/videos", dest_dir=os.path.join(YT_BASE, "APN"), postprocessor_args={"metadata": {"albumartist": "अनन्त-पद्माचार्यः"}})
    if "upload" in actions:
      archive_utility.update_item(item_id="APN_YT", dir_path=os.path.join(YT_BASE, "APN"), metadata={"title": "APN talks", "description": "अनन्त-पद्मनाभाचार्य-भाषणानि\n\n" + DESCRIPTION_BASE})

  if regex.match(channel_pattern, "@parankushacharinstituteofvedic"):
    if "download" in actions:
      youtube.get_all(url="https://www.youtube.com/@parankushacharinstituteofvedic/videos", dest_dir=os.path.join(YT_BASE, "PISV"), postprocessor_args={"metadata": {"albumartist": "pisvTalks"}})
    if "upload" in actions:
      archive_utility.update_item(item_id="pisvTalks", dir_path=os.path.join(YT_BASE, "PISV"), metadata={"title": "PISV Talks", "description": "पराङ्कुशाचार्य-वैदिक-शोध-संस्था-धारा-भाषणानि\n\n" + DESCRIPTION_BASE})


  if regex.match(channel_pattern, "@desikadaily"):
    if "download" in actions:
      youtube.get_all(url="https://www.youtube.com/@desikadaily/videos", dest_dir=os.path.join(YT_BASE, "deshika-daily"), postprocessor_args={"metadata": {"albumartist": "deshika-daily"}})
    if "upload" in actions:
      archive_utility.update_item(item_id="deshika-daily", dir_path=os.path.join(YT_BASE, "deshika-daily"), metadata={"title": "deshika-daily talks", "description": "देशिक-दैनिक-धारा-भाषणानि\n\n" + DESCRIPTION_BASE})

  if regex.match(channel_pattern, "@SriNrusimhaPriya"):
    if "download" in actions:
      youtube.get_all(url="https://www.youtube.com/@SriNrusimhaPriya/videos", dest_dir=os.path.join(YT_BASE, "nRsiMha-priya"), postprocessor_args={"metadata": {"albumartist": "nRsiMha-priya"}})
    if "upload" in actions:
      archive_utility.update_item(item_id="nRsiMha-priya", dir_path=os.path.join(YT_BASE, "nRsiMha-priya"), metadata={"title": "nRsiMha-priya talks", "description": "नृसिंह-प्रिय-धारा-भाषणानि\n\n" + DESCRIPTION_BASE})

  if regex.match(channel_pattern, "@Ramayanaforus"):
    if "download" in actions:
      pass
      # youtube.get_all(url="https://www.youtube.com/@Ramayanaforus/videos", dest_dir=os.path.join(YT_BASE, "duShyanth-shrIdhar-talks"), postprocessor_args={"metadata": {"albumartist": "dushyanth shrIdhar"}})
    if "upload" in actions:
      archive_utility.update_item(item_id="duShyanth-shrIdhar-talks", dir_path=os.path.join(YT_BASE, "duShyanth-shrIdhar-talks"))


  if regex.match(channel_pattern, "@gspk"):
    if "download" in actions:
      youtube.get_all(url="https://www.youtube.com/@gspk/videos", dest_dir=os.path.join(YT_BASE, "gspk_stotra-pArAyaNa-kainkaryam"), postprocessor_args={"metadata": {"albumartist": "GSPK"}})
    if "upload" in actions:
      archive_utility.update_item(item_id="gspk_stotra-pArAyaNa-kainkaryam", dir_path=os.path.join(YT_BASE, "gspk_stotra-pArAyaNa-kainkaryam"))

  if regex.match(channel_pattern, "@ramanujadaya8750"):
    if "download" in actions:
      youtube.get_all(url="https://www.youtube.com/@ramanujadaya8750/videos", dest_dir=os.path.join(YT_BASE, "rAmAnuja-dayA"), postprocessor_args={"metadata": {"albumartist": "rAmAnuja-dayA"}})
    if "upload" in actions:
      archive_utility.update_item(item_id="rAmAnuja-dayA-audio", dir_path=os.path.join(YT_BASE, "rAmAnuja-dayA"))


  # archive_utility.update_item(item_id="tattva-muktA-kalApaH_ALvAr", dir_path=os.path.join(YT_BASE, "tattva-muktA-kalApaH_ALvAr"), metadata={"title": "tattva-muktA-kalApaH - ALvAr", "description": "तत्त्व-मुक्ता-कलापः - आळ्वार्-पाठः\n\n" + DESCRIPTION_BASE})

  if regex.match(channel_pattern, "@nArAyaNAchArya"):
    if "download" in actions:
      youtube.get_all(url="https://www.youtube.com/playlist?list=PLFLowj4VMohUI_zCFA0ZadHDEARgm8J7B", dest_dir=os.path.join(YT_BASE, "nArAyaNAchArya/mbh"), postprocessor_args={"metadata": {"albumartist": "KS nArAyaNAchArya"}})
    if "upload" in actions:
      archive_utility.update_item(item_id="nArAyaNAchArya_mbh", dir_path=os.path.join(YT_BASE, "nArAyaNAchArya/mbh"), metadata={"title": "nArAyaNAchArya MBh talks", "description": "नारायणाचार्य-भाषणानि\n\n" + DESCRIPTION_BASE})

  if regex.match(channel_pattern, "@acharyapaduka"):
    if "download" in actions:
      youtube.get_all(url="https://www.youtube.com/@acharyapaduka/videos", dest_dir=os.path.join(YT_BASE, "acharyapaduka"), postprocessor_args={"metadata": {"albumartist": "AchArya-pAdukA"}})
    if "upload" in actions:
      archive_utility.update_item(item_id="AchAryapAdukA_YT", dir_path=os.path.join(YT_BASE, "acharyapaduka"), metadata={"title": "acharyapaduka talks", "description": "आचार्य-पादुका-धारा-भाषणानि\n\n" + DESCRIPTION_BASE})

  if regex.match(channel_pattern, "@Bhakthamrutham"):
    if "download" in actions:
      youtube.get_all(url="https://www.youtube.com/@Bhakthamrutham/videos", dest_dir=os.path.join(YT_BASE, "bhaktAmRtam"), postprocessor_args={"metadata": {"albumartist": "bhaktAmRta-shrInidhiH"}})
    if "upload" in actions:
      archive_utility.update_item(item_id="bhaktAmRtam_YT", dir_path=os.path.join(YT_BASE, "bhaktAmRtam"), metadata={"title": "bhaktAmRtam talks", "description": "भक्तामृत-धारा-भाषणानि\n\n" + DESCRIPTION_BASE})
  pass


  pass

def naaTTeri(dry_run=False):
  archive_id = "natteri-guru-paramparA_tamiL"
  base_dir = os.path.join(ARCHIVE_BASE, "nATTeri")
  item = audio_archive_utility.ArchiveAudioItem(archive_id=archive_id, repo_base=base_dir)
  # archive_audio_item.update_metadata(metadata=metadata)
  # item.download_original_files(destination_dir=base_dir)
  item.update_from_dir(dry_run=dry_run)
  # item.delete_unaccounted_for_files(all_files_or_dir=base_dir, dry_run=dry_run)
  # item.delete_matching(pattern=".*.mp3.*", dry_run=dry_run)


def dhaarmika_lectureicts():
  pass
  # archive_utility.update_item(item_id="GIPA_gokhale-institute-talks", dir_path=os.path.join(YT_BASE, "GIPA"))
  # archive_utility.update_item(item_id="pparikh-talks", dir_path=os.path.join(YT_BASE, "prashAnt-pArikh"), metadata={"title": "P Parikh interviews", "description": "Source: Prashant Parikh's YT channel\n\n" + DESCRIPTION_BASE})
  # yt-dlp --continue --no-overwrites --extract-audio --audio-format mp3 -o "ST_%(upload_date)s_%(title).50s.%(ext)s" https://www.youtube.com/channel/UC3nhAUpe7aBm1rFCBgoWWcA/videos --playlist-reverse --restrict-filenames   --add-metadata --postprocessor-args "-metadata artist=SrijanTalks" --download-archive ./ytdl-archive.txt --dateafter 
  # youtube.get_all(url="https://www.youtube.com/channel/UC3nhAUpe7aBm1rFCBgoWWcA/videos", dest_dir=os.path.join(YT_BASE, "srijan"), postprocessor_args={"metadata": {"albumartist": "SrijanTalks"}})


def misc():
  pass
  # archive_utility.update_item(item_id="paNDita-parichayaH", dir_path=os.path.join(YT_BASE, "../paNDita-parichayaH"))
  archive_utility.update_item(item_id="MA-lakShmI-tAtAchAryaH", dir_path=os.path.join(YT_BASE, "../paNDita-parichayaH/laxmI-tAtAryaH"))
  # archive_utility.update_item(item_id="vyAsarAja-maTha-lectures", dir_path=os.path.join(YT_BASE, "vyAsarAjamaTha"))
  # archive_utility.update_item(item_id="viShNu-purANa-taylor", dir_path=os.path.join(YT_BASE, "../viShNu-purANa-taylor"))


if __name__ == "__main__":
  shrii_vaishnava()
  # shrii_vaishnava(actions=["upload"])
  # naaTTeri(dry_run=False)
  # dhaarmika_lectures()
  # misc()
  pass
