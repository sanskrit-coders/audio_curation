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

# URL style:
# https://aurobindo.ru/workings/matherials/rigveda/01/01-177.mp3
# wget and urllib.request is blocked.


class RgVedaRepo(audio_repo.AudioRepo):
    pass


def update_rgveda_sriranga():
    metadata = {
        "title" : "Rig-veda shakala saMhitA",
        "description" : """
    ऋग्वेदः। शकल-संहिता।
    Reciters: Sri Shyama Sundara Sharma, Sri Satya Krishna Bhatta
    via aurobindo.ru, by Sriranga Technologies Pvt. Ltd. (2012)
    Tech details- see  https://sanskrit.github.io/projects/audio/veda-audio/index.html
    """
    }

    archive_id="rgveda-auro-sriranga"
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id)
    repo = RgVedaRepo(git_repo_paths=[os.path.join("/home/vvasuki/veda-audio/", "rgveda-shriranga")], archive_audio_item=archive_audio_item, git_remote_origin_basepath="git@github.com:veda-audio")
    # repo.update_git(collapse_history=False, first_push=True)
    # exit(1)
    # repo.archive_item.update_metadata(metadata=metadata)
    # repo.archive_item.delete_unaccounted_for_files(all_files=repo.get_unnormalized_files())
    repo.update_archive_item(mp3_files_in=repo.get_unnormalized_files(), overwrite_all=False)



def update_rgveda_auro():
    metadata = {
        "title" : "Rig-veda shakala saMhitA",
        "description" : """
    ऋग्वेदः। शकल-संहिता।
    
    via aurobindo.ru
    Tech details- see  https://sanskrit.github.io/projects/audio/veda-audio/index.html
    """
    }

    archive_id="Rg-veda-shakala-auro1"
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id)
    repo = RgVedaRepo(git_repo_paths=[os.path.join("/home/vvasuki/veda-audio/", "rgveda-auro")], archive_audio_item=archive_audio_item, git_remote_origin_basepath="git@github.com:veda-audio")
    # repo.update_git(collapse_history=False, first_push=True)
    # exit(1)
    # repo.archive_item.update_metadata(metadata=metadata)
    # repo.archive_item.delete_unaccounted_for_files(all_files=repo.get_unnormalized_files())
    repo.update_archive_item(mp3_files_in=repo.get_unnormalized_files(), overwrite_all=False)


if __name__ == "__main__":
    update_rgveda_auro()