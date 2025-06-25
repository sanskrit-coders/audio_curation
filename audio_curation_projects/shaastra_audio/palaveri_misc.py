import os

from audio_utils import mp3_utility

from audio_curation import archive_utility as archive_utility_audio
from audio_curation import audio_repo

BASE_DIR = "/media/vvasuki/vData/audio/curation/archive/shAstra-audio/palaveri-laxmI-narasiMhaH/"
GENERIC_DESCRIPTION = """
पलवेरि-लक्ष्मीनारायणार्य बोधनानि।  
**अधिकारिभिर् एव तद्-अनुज्ञया श्राव्यम्, नेतरैर्** इति प्रवक्तुर् निर्बन्धः।  
श्रवणसौकर्याय रक्ष्यमाणम् अत्र।  
भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/shaastra-audio/index.html
"""


class RepoBase(audio_repo.NonGitArchiveRepo):
  def __init__(self, album_id, dir_path, archive_id, desc):
    super().__init__(repo_paths=[dir_path])
    self.album_id = album_id
    archive_audio_item = archive_utility_audio.ArchiveAudioItem(archive_id=archive_id, metadata={"description":desc}, repo_base=dir_path)
    self.archive_audio_item = archive_audio_item

  def update_metadata(self, mp3_files):
    """ Update mp3 metadata of a bunch of files. Meant to be overridden.

    :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
    """
    for mp3_file in mp3_files:
      mp3_file.metadata = mp3_utility.Mp3Metadata(
        title=mp3_file.title_from_filename(),
        album=self.album_id,
        artist="palaveri-laxmI-narasiMhaH पलवेरि-लक्ष्मी-नरसिंहः",
      )
      mp3_file.save_metadata()


def bhagavad_vishayam():
  repo = RepoBase(archive_id="laxmI-narasiMhaH_BV", dir_path=os.path.join(BASE_DIR, "bhagavad-viShayam"), album_id="bhagavad-viShayam भगवद्-विषयः", desc=f"{GENERIC_DESCRIPTION}\n\nभगवद्-विषयम्।")
  repo.update_derivatives(dry_run=False)
  # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
  repo.archive_audio_item.update_from_dir(file_patterns=["*.mp3"], overwrite_all=False)


def rts():
  repo = RepoBase(archive_id="laxmI-narasiMhaH_RTS", dir_path=os.path.join(BASE_DIR, "rahasya-traya-sAraH"), album_id="rahasya-traya-sAraH रहस्य-त्रय-सारः", desc=f"{GENERIC_DESCRIPTION}\n\nरहस्य-त्रय-सारः।")
  repo.update_derivatives(dry_run=False)
  # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
  repo.archive_audio_item.update_from_dir(file_patterns=["*.mp3"], overwrite_all=False)


def tirukkural():
  repo = RepoBase(archive_id="laxmI-narasiMhaH_tirukkuraL", dir_path=os.path.join(BASE_DIR, "tiruk-kuraL"), album_id="tiruk-kuraL तिरुक्-कुरळ्", desc=f"{GENERIC_DESCRIPTION}\n\nतिरुक्-कुरळ्।")
  repo.update_derivatives(dry_run=False)
  # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
  repo.archive_audio_item.update_from_dir(file_patterns=["*.mp3"], overwrite_all=False)


def bs():
  repo = RepoBase(archive_id="laxmI-narasiMhaH_BS", dir_path=os.path.join(BASE_DIR, "brahma-sUtram"), album_id="brahma-sUtrANi ब्रह्म-सूत्राणि", desc=f"{GENERIC_DESCRIPTION}\n\nब्रह्म-सूत्राणि।")
  repo.update_derivatives(dry_run=False)
  # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
  repo.archive_audio_item.update_from_dir(file_patterns=["*.mp3"], overwrite_all=False)



def misc():
  repo = RepoBase(archive_id="laxmI-narasiMha-bodhanAni", dir_path=os.path.join(BASE_DIR, "misc"), album_id="misc प्रकीर्ण-बोधनानि", desc=f"{GENERIC_DESCRIPTION}\n\nप्रकीर्ण-बोधनानि।")
  repo.update_derivatives(dry_run=False)
  # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
  repo.archive_audio_item.update_from_dir(file_patterns=["*.mp3"], overwrite_all=False)



if __name__ == '__main__':
  # bhagavad_vishayam()
  rts()
  # tirukkural()
  # bs()
  misc()
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_BS", dir_path=os.path.join(BASE_DIR, "brahma-sUtram"), metadata={"description":GENERIC_DESCRIPTION})
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_AhAra-niyamaH", dir_path=os.path.join(BASE_DIR, "AhAra-niyamaH"), metadata={"description":GENERIC_DESCRIPTION})
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_rAmAyaNam_2023", dir_path=os.path.join(BASE_DIR, "rAmAyaNam_2023"), metadata={"description":GENERIC_DESCRIPTION})

  pass