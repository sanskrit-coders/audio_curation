"""
`Veda audio project`_.

.. _Veda audio project: https://sanskrit.github.io/projects/audio/veda-audio/

Audio items:
https://archive.org/details/jaiminIya-sAma-gAna-paravastu-tradition-santhA
https://archive.org/details/jaiminIya-sAma-gAna-paravastu-tradition

 
"""

## TODO:
# jaiminIya-sAma-gAna-paravastu-tradition-compilation-rAmAnuja 1974 - up to date on google play, upload to archive.
# jaiminIya-sAma-gAna-paravastu-tradition-compilation-rAmAnuja 1974
# jaiminIya-sAma-gAna-paravastu-tradition-compilation-gopAla - up to date on google play (barring possible additions from pavan), upload to archive.
# jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2015 - upload in both places.
# jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2018 - upload in both places.
# jaiminIya-sAma-gAna-paravastu-tradition-gopAla-2014 - fix names in google play, upload to archive.
# jaiminIya-sAma-gAna-paravastu-tradition-anuvachanam-gopAla-pavan - fix names, upload to both places.

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


class Gopal2015Repo(audio_repo.AudioRepo):
    pass





if __name__ == "__main__":
    pass