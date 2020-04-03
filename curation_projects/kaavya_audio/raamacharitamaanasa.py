"""
`kAvya audio project`_ : Raghuvamsha

.. _kAvya audio project: https://sanskrit.github.io/projects/audio/kaavya-audio/
"""

import logging
import pprint

from audio_curation import audio_repo, archive_utility, google_music
from audio_utils import mp3_utility

repo_paths = ["/home/vvasuki/kAvya-audio/rAmacharitamAnasa-AIR"]



class Ramcharitmanas(audio_repo.BaseAudioRepo):

    metadata = {
        "title": "rAma-charita-mAnasa राम-चरित-मानस",
        "description": """
        रामचरितमानस। 
        Ramcharitmanas version of Ramayan complete by All India Radio.
        Derived from https://archive.org/details/EPI63 to fix file ordering.
        """
    }
    archive_id="rAmcharitmAnas-AIR"
    pass


def update(gmusic_client, dry_run):
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=Ramcharitmanas.archive_id, metadata=Ramcharitmanas.metadata)
    repo = Ramcharitmanas(repo_paths=repo_paths, archive_audio_item=archive_audio_item, gmusic_client=gmusic_client)
    logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))
    archive_audio_item.update_metadata(metadata=Ramcharitmanas.metadata)
    
    


if __name__ == "__main__":
    gmusic_client = None
    gmusic_client = google_music.GMusicClient(oauth_file_path="/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/oauth_access_token_gmusic.json", username="vishvas.vasuki@gmail.com")
    update(gmusic_client=gmusic_client, dry_run=False)
    pass
