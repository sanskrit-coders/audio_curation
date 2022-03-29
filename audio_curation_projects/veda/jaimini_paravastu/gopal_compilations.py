"""
`Veda audio project`_.

.. _Veda audio project: https://sanskrit.github.io/groups/dyuganga/projects/audio/veda-audio/

Audio items:
https://archive.org/details/jaiminIya-sAma-gAna-paravastu-tradition-santhA
https://archive.org/details/jaiminIya-sAma-gAna-paravastu-tradition
jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2015

"""

## TODO:
# jaiminIya-sAma-gAna-paravastu-tradition-compilation-rAmAnuja 1974 - up to date on google play, upload to archive.
# jaiminIya-sAma-gAna-paravastu-tradition-compilation-rAmAnuja 1974
# jaiminIya-sAma-gAna-paravastu-tradition-compilation-gopAla - up to date on google play (barring possible additions from pavan), upload to archive.
# jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2015 - upload in both places.
# jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2018 - upload in both places.
# jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2014 - fix names in google play, upload to archive.
# jaiminIya-sAma-gAna-paravastu-tradition-anuvachanam-gopAla-pavan - fix names, upload to both places.

import logging
import os

# noinspection PyPep8
from audio_curation import audio_repo, archive_utility

from audio_utils import mp3_utility

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)


class GopalcompilationRepoBase(audio_repo.BaseAudioRepo):

    def update_metadata(self, mp3_files):
        """ Update mp3 metadata of a bunch of files. Meant to be overridden.

        :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
        """
        for mp3_file in mp3_files:
            mp3_file.metadata = mp3_utility.Mp3Metadata(
                title=mp3_file.title_from_filename(),
                album="jaiminIya-sAma-gAna-paravastu-tradition-gopAla-compilation जैमिनीय-परवस्तु-साम-गानम् सङ्ग्रहाः",
                album_artist="paravastu-gopAla परवस्तु-गोपालः",
                artist="paravastu-gopAla परवस्तु-गोपालः"
            )
            mp3_file.save_metadata()


def update_gopal_compilation(dry_run=False):
    metadata = {
        "title" : "jaiminIya-sAma-gAna-paravastu-tradition-gopAla-compilation",
        "description" : """
    सामवेदः। जैमिनीय-शाखा।
    
    jaiminIya-sAma-gAna TN-AP-paravastu-tradition, as presented by shrI gopAla around 2014-2017.
    
    Generations ago from ALwarthirunagari.
    
    Details: https://sanskritdocuments.org/sites/pssramanujaswamy/#audios
    Tech details- see  https://sanskrit.github.io/groups/dyuganga/projects/audio/veda-audio/index.html
    """
    }
    archive_id="jaiminIya-sAma-gAna-paravastu-tradition-gopAla-compilation"
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id)
    archive_audio_item.update_metadata(metadata=metadata)
    repo = GopalcompilationRepoBase(repo_paths=[os.path.join("/home/vvasuki/veda-audio/jaiminIya-sAma-paravastu", "jaiminIya-sAma-gAna-paravastu-tradition-gopAla-compilation")], archive_audio_item=archive_audio_item, git_remote_origin_basepath="git@github.com:veda-audio")
    repo.reprocess_files(mp3_files=repo.get_unnormalized_files(), update_git=False, dry_run=dry_run, normalize_files=False)
    repo.delete_unaccounted_for_files(all_files=repo.get_unnormalized_files(), dry_run=dry_run)
    # gmusic_client.upload(mp3_files=repo.get_unnormalized_files(), dry_run=True)


if __name__ == "__main__":
    
    # 
    update_gopal_compilation(dry_run=False)
    pass