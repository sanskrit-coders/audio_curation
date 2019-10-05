"""
`kAvya audio project`_ : durgA-saptashatI

.. _kAvya audio project: https://sanskrit.github.io/projects/audio/kaavya-audio/
"""

import logging
import os
import pprint

from audio_curation import audio_repo, archive_utility, google_music
from audio_utils import mp3_utility


class RepoBase(audio_repo.BaseAudioRepo):

    def update_metadata(self, mp3_files):
        """ Update mp3 metadata of a bunch of files. Meant to be overridden.

        :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
        """
        for mp3_file in mp3_files:
            mp3_file.metadata = mp3_utility.Mp3Metadata(
                title=mp3_file.title_from_filename(),
                album="durgA-saptashatI दुर्गासप्तशती",
                artist="MH brAhmaNas ब्राह्मणाः"
            )
            mp3_file.save_metadata()


class NormalizedFilesRepo(audio_repo.NormalizedRepo):
    metadata = {
        "title" : "durgA-saptashatI दुर्गासप्तशती चण्डी-पाठः",
        "description" : """
          दुर्गासप्तशती मार्कण्डेयपुराणात्। durgAsaptashatI from mArkaNDeyapurANa.  
          Chanted by brAhmaNas from MH, likely. Obtained via puja.net.
          Aka ChaNDI-pAThaH.
          भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/projects/audio/kaavya-audio/index.html
    """
    }
    archive_id="durgA-saptashatI"


def update_repo(gmusic_client, dry_run=False):
    repo = RepoBase(repo_paths=[os.path.join("/home/vvasuki/kAvya-audio/durgA-saptashatI")])
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=NormalizedFilesRepo.archive_id)
    archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
    normalized_files_repo = audio_repo.NormalizedRepo(base_repo=repo, archive_audio_item=archive_audio_item, gmusic_client=gmusic_client)
    logging.info(pprint.pformat(normalized_files_repo.reprocess(dry_run=dry_run)))


if __name__ == "__main__":
    gmusic_client = None
    gmusic_client = google_music.GMusicClient(oauth_file_path="/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/oauth_access_token_gmusic.json", username="vishvas.vasuki@gmail.com")
    update_repo(gmusic_client=gmusic_client, dry_run=False)
    pass
