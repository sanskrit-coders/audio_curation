

import logging
import os
import pprint

from audio_curation import audio_repo, archive_utility
from audio_utils import mp3_utility


class RepoBase(audio_repo.BaseAudioRepo):

  def update_metadata(self, mp3_files):
    """ Update mp3 metadata of a bunch of files. Meant to be overridden.

    :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
    """
    for mp3_file in mp3_files:
      mp3_file.metadata = mp3_utility.Mp3Metadata(
        title=mp3_file.title_from_filename(),
        album="sthaaneshvara-bhaaShaNaani स्थानेश्वर-भाषणानि",
        artist="sthAneshvaraH स्थानेश्वरः",
      )
      mp3_file.save_metadata()


class NormalizedFilesRepo(audio_repo.NormalizedRepo):
  metadata = {
    "title" : "sthaaneshvara-bhaaShaNaani स्थानेश्वर-भाषणानि",
    "description" : """
          Miscellaneous talks by sthAneshvar timalsIna.  
          श्रवणसौकर्याय-रक्ष्यमाणम् अत्र।  
          भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/shaastra-audio/index.html
    """
  }
  archive_id="sthAneshvara-talks"


def update_repo(dry_run=False):
  repo = RepoBase(repo_paths=["/media/vvasuki/vData/audio/curation/git/shAstra-audio/sthAneshvara-talks/"])
  archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=NormalizedFilesRepo.archive_id)
  # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
  logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))
  normalized_files_repo = audio_repo.NormalizedRepo(base_repo=repo, archive_audio_item=archive_audio_item)
  logging.info(pprint.pformat(normalized_files_repo.reprocess(dry_run=dry_run)))


if __name__ == "__main__":
  update_repo(dry_run=False)
  pass
