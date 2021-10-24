"""
`Veda audio project`_.

.. _Veda audio project: https://sanskrit.github.io/groups/dyuganga/projects/audio/veda-audio/
"""

import glob
import logging
import os

# noinspection PyPep8
import pprint

from audio_curation import audio_repo, archive_utility

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

# URL style:
# https://aurobindo.ru/workings/matherials/rigveda/01/01-177.mp3
# wget and urllib.request is blocked.


class VedaRepoBase(audio_repo.BaseAudioRepo):
    metadata = {
        "title" : "kRShNa-yajur-veda taittirIya saMhitA IGNCA",
        "description" : """
    यजुर्-वेदः। तैत्तिरीय-संहिता।
    Courtsey : IGNCA and Indian taxpayers.
    Tech details- see  https://sanskrit.github.io/groups/dyuganga/projects/audio/veda-audio/index.html
    """
    }

    archive_id="yajurveda-taittirIya-ignca"
    pass


def update_repos(dry_run=False):
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=VedaRepoBase.archive_id, metadata=VedaRepoBase.metadata)
    repo = VedaRepoBase(repo_paths=[os.path.join("/home/vvasuki/Music/git-curation/veda-audio", "taittirIya_ignca")], archive_audio_item=archive_audio_item, git_remote_origin_basepath=None)
    logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))


if __name__ == "__main__":
    
    update_repos(gmusic_client=dry_run=False)