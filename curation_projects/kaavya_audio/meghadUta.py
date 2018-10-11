"""
`kAvya audio project`_.

.. _kAvya audio project: https://sanskrit.github.io/projects/audio/kaavya-audio/
"""

import glob
import logging
import os

from audio_curation import audio_repo

repo_paths = ["/home/vvasuki/kAvya-audio/meghadUta"]

metadata = {
    "title": "mahA-darshana-devuDu-narasimha-shAstrI",
    "description": """
      मेघदूतम् कालिदास-कृतम्।  
     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/projects/audio/kaavya-audio/index.html
    """
}


class RaghuvamshaRepo(audio_repo.AudioRepo):
    pass
repo = RaghuvamshaRepo(git_repo_paths=repo_paths, archive_id="meghadUta-dhvaniH", git_remote_origin_basepath="git@github.com:kAvya-audio")
# repo.update_git(collapse_history=False, first_push=True)
# exit(1)
# repo.archive_item.update_metadata(metadata=metadata)
# repo.archive_item.archive_item.modify_metadata(metadata=metadata)
