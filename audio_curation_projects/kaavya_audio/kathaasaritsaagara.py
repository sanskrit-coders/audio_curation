"""
`kAvya audio project`_.

.. _kAvya audio project: https://sanskrit.github.io/groups/dyuganga/projects/audio/kaavya-audio/
"""

import glob
import logging
import os
import pprint

from audio_curation import audio_repo, archive_utility
from audio_utils import mp3_utility
from audio_curation.episode_data import google_sheets_data

LOCAL_REPO_BASE_PATH = "/home/vvasuki/Music/git-curation/kAvya-audio/kathAsaritsAgara"
repo_paths = [LOCAL_REPO_BASE_PATH]
episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1K8cuRtvTLQKntE7r9Kn5gOqg_ciGlwYWao4RX9Wx-TQ", worksheet_name="कार्यावलिः", google_key = '/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', episode_id_column="सञ्चिकाशीर्षिका", recorder_column="पठिता")


def get_taranga_id(file_path):
    """

    :param file_path: 
    :return: 
    """
    basename = os.path.basename(file_path)
    return basename[0:9]


def set_mp3_metadata(mp3_file):
    taranga_part_id = os.path.splitext(mp3_file.basename)[0]
    # parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=mp3_file.file_path)
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        title=taranga_part_id,
        album = "कथासरित्सागरः kathAsaritsAgara",
        album_artist = "गुणाढ्यः guNADhya"
    )


class KathasaritsagaraRepoBase(audio_repo.BaseAudioRepo):
    metadata = {
        "title": "कथासरित्सागरः kathAsaritsAgara",
        "description": """
     कथासरित्सागरः। 
     guNADhya.  गुणाढ्य-कृत-कथासरित्-सागरः


     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/kAvya-audio/
    """
    }

    def update_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        for mp3_file in mp3_files:
            set_mp3_metadata(mp3_file)
            mp3_file.metadata.artist = episode_data.get_recorder(get_taranga_id(file_path=mp3_file.file_path))
            mp3_file.save_metadata()


class SpeedFileRepo(audio_repo.SpeedFileRepo):
    metadata = {
        "title": "कथासरित्सागरः kathAsaritsAgara १.५गत्या ",
        "description": """
     कथासरित्सागरः।
     guNADhya.  गुणाढ्य-कृत-कथासरित्-सागरः

     भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/kAvya-audio/index.html
    """
    }


dry_run = False
base_repo = KathasaritsagaraRepoBase(repo_paths=repo_paths, git_remote_origin_basepath="git@github.com:kAvya-audio")
logging.info(pprint.pformat(base_repo.reprocess(dry_run=dry_run)))

archive_audio_item = archive_utility.ArchiveAudioItem(archive_id="kathAsaritsAgara-shrAvaNam")
archive_audio_item.update_metadata(metadata=KathasaritsagaraRepoBase.metadata)
normalized_files_repo = audio_repo.NormalizedRepo(base_repo=base_repo, archive_audio_item=archive_audio_item)
logging.info(pprint.pformat(normalized_files_repo.reprocess(dry_run=dry_run)))

archive_id = archive_audio_item.archive_id + "-150p-speed"
archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id)
archive_audio_item.update_metadata(metadata=SpeedFileRepo.metadata)
speed_files_repo = SpeedFileRepo(base_repo=normalized_files_repo, archive_audio_item=archive_audio_item)
logging.info(pprint.pformat(speed_files_repo.reprocess(dry_run=dry_run)))
