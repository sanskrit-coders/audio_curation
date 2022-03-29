"""
`kAvya audio project`_ : Raghuvamsha

.. _kAvya audio project: https://sanskrit.github.io/groups/dyuganga/projects/audio/kaavya-audio/
"""
import logging
import pprint

from audio_curation import audio_repo, archive_utility, yt_music

repo_paths = ["/home/vvasuki/Music/git-curation/kAvya-audio/rAmacharitamAnasa-AIR"]



class Ramcharitmanas(audio_repo.BaseAudioRepo):

    metadata = {
        "title": "rAma-charita-mAnasa राम-चरित-मानस",
        "description": """
        रामचरितमानस। 
        Ramcharitmanas version of Ramayan complete by All India Radio.
        Derived from https://archive.org/details/EPI63 to fix file ordering; and with replacement recordings for missing and duplicated files.
        
        Contributions welcome: https://sanskrit.github.io/groups/dyuganga/projects/audio/kAvya-audio/
        """
    }
    archive_id="rAmcharitmAnas-AIR"
    pass


def update(dry_run):
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=Ramcharitmanas.archive_id, metadata=Ramcharitmanas.metadata)
    repo = Ramcharitmanas(repo_paths=repo_paths, archive_audio_item=archive_audio_item)
    logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))
    # archive_audio_item.update_metadata(metadata=Ramcharitmanas.metadata)



if __name__ == "__main__":
    
    # 
    update(dry_run=False)
    pass
