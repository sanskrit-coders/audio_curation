"""
`Veda audio project`_.

.. _Veda audio project: https://sanskrit.github.io/projects/audio/veda-audio/
"""

import glob
import logging
import os

# noinspection PyPep8
from audio_curation import audio_repo, google_music, archive_utility

# Remove all handlers associated with the root logger object.

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

LOCAL_REPO_BASE_PATH = os.path.join("/home/vvasuki/veda-audio/", "rgveda-shriranga")

# URL style:
# https://aurobindo.ru/workings/matherials/rigveda/01/01-177_2.mp3
# wget and urllib.request is blocked.


class RgVedaSrirangaRepo(audio_repo.AudioRepo):
    pass

metadata = {
    "title" : "Rig-veda shakala saMhitA",
    "description" : """
    ऋग्वेदः। शकल-संहिता।
    Reciters: Sri Shyama Sundara Sharma, Sri Satya Krishna Bhatta
    via aurobindo.ru, by Sriranga Technologies Pvt. Ltd. (2012)
    Tech details- see  https://sanskrit.github.io/projects/audio/veda-audio/index.html
    """
}

if __name__ == "__main__":
    archive_id="rgveda-auro-sriranga"
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id)
    repo = RgVedaSrirangaRepo(git_repo_paths=[LOCAL_REPO_BASE_PATH], archive_audio_item=archive_audio_item, git_remote_origin_basepath="git@github.com:veda-audio")
    # repo.update_git(collapse_history=False, first_push=True)
    # exit(1)
    repo.archive_item.update_metadata(metadata=metadata)
    repo.update_archive_item(mp3_files_in=repo.get_unnormalized_files(), overwrite_all=False, dry_run=True)