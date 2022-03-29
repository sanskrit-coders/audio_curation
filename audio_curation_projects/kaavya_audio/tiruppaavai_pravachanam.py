"""
`kAvya audio project`_ : meghadUtam

.. _kAvya audio project: https://sanskrit.github.io/groups/dyuganga/projects/audio/kaavya-audio/
"""

import logging
import pprint

from audio_curation import audio_repo, archive_utility

repo_paths = ["/home/vvasuki/Music/git-curation/kAvya-audio/tiruppAvai-saMskRta-Pravachanam_shrIrAma-jagannAthaH"]


class RepoBase(audio_repo.BaseAudioRepo):
  def update_metadata(self, mp3_files):
    pass


class NormalizedFilesRepo(audio_repo.NormalizedRepo):
  metadata = {
    "title": "tiruppAvai of ANDAL - sanskrit discourse by sreeram jagannathan तिरुप्पावै",
    "description": """
         tiruppAvai (also spelled thiruppAvai) of ANDAL
         sanskrit discourse by sreeram jagannathan
         tiruppAvai-saMskRta-Pravachanam - shrIrAma-jagannAthaH
         तिरुप्पावै-संस्कृत-प्रवचनम् -  जगन्नाथ-श्रीरामः
         
         भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/kaavya-audio/
        """
  }
  archive_id = "tiruppAvai-saMskRta-Pravachanam_shrIrAma-jagannAthaH"


def update_kAvya(dry_run):
  repo = RepoBase(repo_paths=repo_paths)
  logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))

  archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=NormalizedFilesRepo.archive_id)
  # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
  normalized_files_repo = NormalizedFilesRepo(base_repo=repo, archive_audio_item=archive_audio_item)
  logging.info(pprint.pformat(normalized_files_repo.reprocess(dry_run=dry_run)))


if __name__ == "__main__":
  update_kAvya(dry_run=False)
  pass
