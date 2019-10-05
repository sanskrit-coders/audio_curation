"""
`kAvya audio project`_.

.. _kAvya audio project: https://sanskrit.github.io/projects/audio/kaavya-audio/
"""

import glob
import logging
import os

from audio_curation import audio_repo
from audio_utils import mp3_utility

repo_paths = ["/home/vvasuki/kAvya-audio/meghadUta"]

metadata = {
    "title": "mahA-darshana-devuDu-narasimha-shAstrI",
    "description": """
      मेघदूतम् कालिदास-कृतम्।  
     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/projects/audio/kaavya-audio/index.html
    """
}


def set_mp3_metadata(mp3_file):
    part_id = mp3_file.basename
    # parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=mp3_file.file_path)
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        title=part_id,
        album = "मेघदूतम् meghadUtam",
        album_artist = "कालिदासः kAlidAsaH"
    )


class MeghadutaRepoBase(audio_repo.BaseAudioRepo):
    pass
repo = MeghadutaRepoBase(repo_paths=repo_paths, archive_id="meghadUta-dhvaniH", git_remote_origin_basepath="git@github.com:kAvya-audio")
# repo.update_git(collapse_history=False, first_push=True)
# exit(1)
# repo.archive_item.update_metadata(metadata=metadata)
# repo.archive_item.archive_item.modify_metadata(metadata=metadata)
