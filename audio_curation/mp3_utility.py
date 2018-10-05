import logging

import os
import eyed3

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(filename)s:%(lineno)d %(message)s"
)

logging.warning("Logging.warning functional!")
logging.info("Logging.info functional!")
logging.getLogger('eyed3').setLevel(logging.INFO)


def get_parva_adhyaaya_id(file_path):
    """

    :param file_path: 
    :return: 
    """
    basename = os.path.basename(file_path)
    parva_adhyaaya_part_id = os.path.splitext(basename)[0]
    return parva_adhyaaya_part_id[0:7]


class Mp3Metadata(object):
    def __init__(self, title=None, artist=None, album=None, album_artist=None):
        pass


class Mp3File(object):
    """

    """
    def __init__(self, file_path, load_tags_from_file=False, artist=None):
        self.file_path = file_path
        self.directory = os.path.dirname(file_path)
        self.basename = os.path.basename(file_path)
        self.parva_adhyaaya_part_id = os.path.splitext(self.basename)[0]
        self.parva_adhyaaya_id = get_parva_adhyaaya_id(file_path=file_path)
        self.parva_id = self.basename.split("-")[0]
        self.title = self.parva_adhyaaya_part_id
        if load_tags_from_file:
            self.set_tags_from_file()
        if (not hasattr(self, "artist")) and (artist is not None):
            self.artist = artist
        self.album = "महाभारतम् mahAbhAratam - parva %s" % self.parva_id
        self.album_artist = "वेदव्यासः vedavyAsa"

        # Linter complains if instance variables are defined outside __init__, so defining here despite calling set_normalized_file():
        self.normalized_file_path = None
        self.normalized_file = None
        self.set_normalized_file()

    def __str__(self):
        return "Mp3File(%s)" % self.file_path

    def set_tags_from_file(self):
        """

        """
        audiofile = eyed3.load(self.file_path)
        if audiofile.tag is not None:
            self.artist = audiofile.tag.artist

    def is_file_normalized(self):
        """

        :return: 
        """
        return self.normalized_file_path == self.file_path

    def set_normalized_file(self, normalized_file_path=None):
        """

        :return: 
        """
        if normalized_file_path is None:
            self.normalized_file_path = os.path.join(os.path.dirname(self.directory), "normalized_mp3", self.basename)
        if self.is_file_normalized():
            return
        if os.path.isfile(self.normalized_file_path) and os.access(self.normalized_file_path, os.R_OK):
            self.normalized_file = Mp3File(self.normalized_file_path, artist=self.artist)
        else:
            self.normalized_file = None

    def is_normalized_file_outdated(self):
        """

        :return: 
        """
        return not self.is_file_normalized() and (
                (not os.path.isfile(self.normalized_file_path)) or os.path.getmtime(self.file_path) >= os.path.getmtime(
            self.normalized_file_path))

    def update_metadata(self):
        """

        """
        audiofile = eyed3.load(self.file_path)
        if audiofile.tag is None:
            audiofile.initTag()
        local_tag_update_needed = (audiofile.tag.artist != self.artist) or (audiofile.tag.title != self.title) or (
                audiofile.tag.album != self.album) or (audiofile.tag.album_artist != self.album_artist)

        if local_tag_update_needed:
            logging.info("***Updating %s locally." % self.basename)
            audiofile.tag.artist = self.artist
            audiofile.tag.title = self.title
            audiofile.tag.album = self.album
            audiofile.tag.album_artist = self.album_artist
            audiofile.tag.save()

    def check_loudness(self):
        """

        :return: 
        """
        from pydub import AudioSegment
        sound = AudioSegment.from_mp3(self.file_path)
        return sound.dBFS

    def save_normalized(self, normalized_mp3_path=None, overwrite=False):
        """

        :param overwrite: 
        :return: 
        """
        if (not overwrite) and (os.path.isfile(self.normalized_file_path)):
            logging.warning("Not overwriting %s" % self.normalized_file_path)
            return
        from pydub import AudioSegment
        sound = AudioSegment.from_mp3(self.file_path)
        logging.info(sound.dBFS)
        # Convert to mono.
        normalized_sound = sound.set_channels(1)
        # Set loudness to the standard level:  -16LUFS or roughly -16dbFS
        # Eventually we would want to use LUFS. One would need to switch libraries or await resolution of https://github.com/jiaaro/pydub/issues/321 .
        normalized_sound = normalized_sound.apply_gain(-16 - sound.dBFS)
        logging.info(normalized_sound.dBFS)
        os.makedirs(os.path.dirname(normalized_mp3_path), exist_ok=True)
        self.set_tags_from_file()
        normalized_sound.export(normalized_mp3_path, format="mp3", tags={
            "artist": self.artist, "album_artist": self.album_artist, "title": self.title, "album": self.album
        })
        self.set_normalized_file()
