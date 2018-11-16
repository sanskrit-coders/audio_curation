"""
`Veda audio project`_.

.. _Veda audio project: https://sanskrit.github.io/projects/audio/veda-audio/

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
from audio_curation import audio_repo, archive_utility, mp3_utility, google_music

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)


class Gopal2018Repo(audio_repo.AudioRepo):

    def update_metadata(self, mp3_files):
        """ Update mp3 metadata of a bunch of files. Meant to be overridden.

        :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
        """
        for mp3_file in mp3_files:
            mp3_file.metadata = mp3_utility.Mp3Metadata(
                title=mp3_file.title_from_filename(),
                album="jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2018 जैमिनीय-परवस्तु-साम-गानम् २०१८",
                album_artist="paravastu-gopAla परवस्तु-गोपालः",
                artist="paravastu-gopAla परवस्तु-गोपालः"
            )
            mp3_file.save_metadata()


def update_gopal_2018(gmusic_client, dry_run=False):
    metadata = {
        "title" : "jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2018",
        "description" : """
    सामवेदः। जैमिनीय-शाखा।
    
    jaiminIya-sAma-gAna TN-AP-paravastu-tradition, as presented by shrI gopAla around 2018.
    
    Generations ago from ALwarthirunagari.
    
    Details: https://sanskritdocuments.org/sites/pssramanujaswamy/#audios
    Tech details- see  https://sanskrit.github.io/projects/audio/veda-audio/index.html
    """
    }
    archive_id="jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2018"
    archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id)
    archive_audio_item.update_metadata(metadata=metadata)
    repo = Gopal2018Repo(git_repo_paths=[os.path.join("/home/vvasuki/veda-audio/jaiminIya-sAma-paravastu", "jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2018")], archive_audio_item=archive_audio_item, git_remote_origin_basepath="git@github.com:veda-audio", gmusic_client=gmusic_client)
    repo.reprocess_files(mp3_files=repo.get_unnormalized_files(), update_git=False, dry_run=dry_run, normalize_files=False)
    repo.delete_unaccounted_for_files(all_files=repo.get_unnormalized_files(), dry_run=dry_run)
    # gmusic_client.upload(mp3_files=repo.get_unnormalized_files(), dry_run=True)


if __name__ == "__main__":
    gmusic_client = google_music.GMusicClient(oauth_file_path="/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/oauth_access_token_gmusic.json", username="vishvas.vasuki@gmail.com")
    # gmusic_client = None
    update_gopal_2018(gmusic_client=gmusic_client, dry_run=False)
    pass