"""
`Veda audio project`_.

.. _Veda audio project: https://sanskrit.github.io/projects/audio/veda-audio/

Audio items:
https://archive.org/details/jaiminIya-sAma-gAna-paravastu-tradition-santhA
https://archive.org/details/jaiminIya-sAma-gAna-paravastu-tradition
jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2015

"""
import logging
import os

# noinspection PyPep8
import pprint

from audio_curation import audio_repo, archive_utility, google_music

from audio_utils import mp3_utility

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)


class GopalPavanaRepoBase(audio_repo.BaseAudioRepo):

    def update_metadata(self, mp3_files):
        """ Update mp3 metadata of a bunch of files. Meant to be overridden.

        :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
        """
        for mp3_file in mp3_files:
            mp3_file.metadata = mp3_utility.Mp3Metadata(
                title=mp3_file.title_from_filename(),
                album="jaiminIya-sAma-gAna-paravastu-tradition-anuvachanam-gopAla-pavana जैमिनीय-परवस्तु-साम अनुवचनम् गोपाल-पवनाभ्याम् २०१५",
                album_artist="paravastu-gopAla परवस्तु-गोपालः",
                artist="paravastu-gopAla परवस्तु-गोपालः, paravastu-pavana परवस्तु-पवनः"
            )
            mp3_file.save_metadata()




class NormalizedFilesRepo(audio_repo.NormalizedRepo):
    metadata = {
        "title" : "jaiminIya-sAma-gAna-paravastu-tradition-anuvachanam-gopAla-pavana",
        "description" : """
    सामवेदः। जैमिनीय-शाखा।
    
    jaiminIya-sAma-gAna TN-AP-paravastu-tradition, as taught by shrI gopAla to shrI pavana around 2015.
    
    Generations ago from ALwarthirunagari.
    
    Details: https://sanskritdocuments.org/sites/pssramanujaswamy/#audios
    Tech details- see  https://sanskrit.github.io/projects/audio/veda-audio/index.html
    """
    }
    archive_id="jaiminIya-sAma-gAna-paravastu-tradition-anuvachanam-gopAla-pavana-2015"


class SpeedFileRepo(audio_repo.SpeedFileRepo):
    metadata = {
        "title" : "jaiminIya-sAma-gAna-paravastu-tradition-anuvachanam-gopAla-pavana",
        "description" : """
    सामवेदः। जैमिनीय-शाखा।
    
    jaiminIya-sAma-gAna TN-AP-paravastu-tradition, as taught by shrI gopAla to shrI pavana around 2015. (Speed 1.5x)
    
    Generations ago from ALwarthirunagari.
    
    Details: https://sanskritdocuments.org/sites/pssramanujaswamy/#audios
    Tech details- see  https://sanskrit.github.io/projects/audio/veda-audio/index.html
    """
    }

    archive_id = NormalizedFilesRepo.archive_id + "-150p-speed"

    def update_metadata(self, mp3_files):
        """ Update mp3 metadata of a bunch of files. Meant to be overridden.

        :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
        """
        for mp3_file in mp3_files:
            mp3_file.metadata = mp3_utility.Mp3Metadata(
title=mp3_file.title_from_filename(),
                album="paravastu-jaiminIya-sAma-anuvachanam-gopAla-pavana 1.5x speed जैमिनीय-परवस्तु-साम अनुवचनम् गोपाल-पवनाभ्याम् २०१५",
                album_artist="paravastu-gopAla परवस्तु-गोपालः",
                artist="paravastu-gopAla परवस्तु-गोपालः, paravastu-pavana परवस्तु-पवनः"
            )
            mp3_file.save_metadata()


def update_gopal_pavana(gmusic_client, dry_run=False):
    repo = GopalPavanaRepoBase(repo_paths=[os.path.join("/home/vvasuki/veda-audio/jaiminIya-sAma-paravastu", "jaiminIya-sAma-gAna-paravastu-tradition-anuvachanam-gopAla-pavana")])
    logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))

    archive_audio_item = None
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=NormalizedFilesRepo.archive_id)
    # archive_audio_item.update_metadata(metadata=NormalizedFilesRepo.metadata)
    normalized_files_repo = audio_repo.NormalizedRepo(base_repo=repo, archive_audio_item=archive_audio_item, gmusic_client=gmusic_client)
    logging.info(pprint.pformat(normalized_files_repo.reprocess(dry_run=dry_run)))

    archive_audio_item = None
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=SpeedFileRepo.archive_id)
    # archive_audio_item.update_metadata(metadata=SpeedFilesRepo.metadata)
    speed_files_repo = SpeedFileRepo(base_repo=normalized_files_repo, archive_audio_item=archive_audio_item, gmusic_client=gmusic_client)
    logging.info(pprint.pformat(speed_files_repo.reprocess(dry_run=dry_run)))


if __name__ == "__main__":
    gmusic_client = None
    gmusic_client = google_music.GMusicClient(oauth_file_path="/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/oauth_access_token_gmusic.json", username="vishvas.vasuki@gmail.com")
    update_gopal_pavana(gmusic_client=gmusic_client, dry_run=False)
    pass