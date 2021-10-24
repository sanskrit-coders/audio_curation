"""
`kAvya audio project`_ : meghadUtam

.. _kAvya audio project: https://sanskrit.github.io/groups/dyuganga/projects/audio/kaavya-audio/
"""

import logging
import pprint

from audio_curation import audio_repo, archive_utility
from audio_utils import mp3_utility

repo_paths = ["/home/vvasuki/kAvya-audio/meghadUtam"]


def set_mp3_metadata(mp3_file):
    part_id = mp3_file.basename[:-4]
    # parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=mp3_file.file_path)
    mp3_file.metadata = mp3_utility.Mp3Metadata(
        title=part_id,
        album="मेघदूतम् meghadUta",
        artist="कालिदासः kAlidAsa and vedabhoomi.org",
        album_artist="कालिदासः kAlidAsa and vedabhoomi.org"
    )


class RepoBase(audio_repo.BaseAudioRepo):
    def update_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        for mp3_file in mp3_files:
            set_mp3_metadata(mp3_file)
            mp3_file.save_metadata()


class NormalizedFilesRepo(audio_repo.NormalizedRepo):

    metadata = {
        "title": "meghadUtam मेघदूतम्",
        "description": """
          रघुवंशम् कालिदास-कृतम्।  
    
    The core portion of https://archive.org/details/MeghadootamByVedabhoomi.org .
    
    Original description:
Written in the 4th century by India's greatest Sanskrit poet Mahakavi Kalidasa, Megha Sandesha (The Cloud Messenger) is considered to be one of the greatest Mahakavyas set to the 'mandakranta' meter known for its lyrical sweetness.
Megha Sandesha tells the tale of a young demigod, banished to earth, who sends a message (sandesha) to his beloved wife in the heavens through a passing rain cloud (megha).
As the Megha travels across India to deliver his message, Kalidasa's poetry describes the glorious beauty of his country.
         भवद्योगदानं‌ काङ्क्ष्यते - https://sanskrit.github.io/groups/dyuganga/projects/audio/kaavya-audio/index.html
        """
    }
    archive_id="meghadUta-mUlam-vedabhoomi.org"



def update_kAvya(dry_run):
    repo = RepoBase(repo_paths=repo_paths)
    logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))

    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=NormalizedFilesRepo.archive_id)
    # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
    normalized_files_repo = NormalizedFilesRepo(base_repo=repo, archive_audio_item=archive_audio_item)
    logging.info(pprint.pformat(normalized_files_repo.reprocess(dry_run=dry_run)))



if __name__ == "__main__":
    
    
    update_kAvya(gmusic_client=dry_run=False)
    pass
