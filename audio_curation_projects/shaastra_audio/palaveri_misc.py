
import logging
import os
import pprint

from audio_curation import audio_repo
from audio_curation import archive_utility as archive_utility_audio
from curation_utils import archive_utility
from audio_utils import mp3_utility


BASE_DIR = "/media/vvasuki/vData/audio/curation/git/shAstra-audio/palaveri-laxmI-narasiMhaH/"
GENERIC_DESCRIPTION = """
पलवेरि-लक्ष्मीनारायणार्य बोधनानि।  
**अधिकारिभिर् एव तद्-अनुज्ञया श्राव्यम्, नेतरैर्** इति प्रवक्तुर् निर्बन्धः।  
श्रवणसौकर्याय-रक्ष्यमाणम् अत्र।  
भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/shaastra-audio/index.html
"""


class RepoBase(audio_repo.NonGitArchiveRepo):
  def __init__(self, album_id, dir_path, archive_id):
    super().__init__(repo_paths=[dir_path])
    self.album_id = album_id
    archive_audio_item = archive_utility_audio.ArchiveAudioItem(archive_id=archive_id, metadata={"description":GENERIC_DESCRIPTION}, repo_base=dir_path)
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
  repo = RepoBase(archive_id="laxmI-narasiMhaH_BV", dir_path = os.path.join(BASE_DIR, "bhagavad-viShayam"), album_id="bhagavad-viShayam भगवद्-विषयः")
  repo.update_derivatives(dry_run=False)
  # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
  repo.archive_audio_item.update_from_dir(file_patterns=["*.mp3"], overwrite_all=True)



if __name__ == '__main__':
  bhagavad_vishayam()
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_RTS", dir_path=os.path.join(BASE_DIR, "rahasya-traya-sAraH"), metadata={"description":GENERIC_DESCRIPTION})
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_BS", dir_path=os.path.join(BASE_DIR, "brahma-sUtram"), metadata={"description":GENERIC_DESCRIPTION})
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_AhAra-niyamaH", dir_path=os.path.join(BASE_DIR, "AhAra-niyamaH"), metadata={"description":GENERIC_DESCRIPTION})
  # archive_utility.update_item(item_id="laxmI-narasiMhaH_rAmAyaNam_2023", dir_path=os.path.join(BASE_DIR, "rAmAyaNam_2023"), metadata={"description":GENERIC_DESCRIPTION})

  pass