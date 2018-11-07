import logging

import os
import pprint

import eyed3

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

# logging.warning("Logging.warning functional!")
# logging.info("Logging.info functional!")
logging.getLogger('eyed3').setLevel(logging.INFO)


## TODO: Move this to pydub.silence
def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


class Mp3Metadata(object):
    """
    Models the metadata in an mp3 file.
    """

    def __init__(self, title=None, artist=None, album=None, album_artist=None):
        self.title = title
        self.artist = artist
        self.album = album
        self.album_artist = album_artist

    def __repr__(self):
        return "Title: %s, Artist: %s, Album: %s, Album artist: %s" % (self.title, self.artist, self.album, self.album_artist)

    @classmethod
    def from_file(cls, file_path):
        self = Mp3Metadata()
        self.get_from_file(file_path)
        return self

    def get_from_file(self, file_path):
        """

        """
        audiofile = eyed3.load(file_path)
        if audiofile.tag is not None:
            self.artist = audiofile.tag.artist
            self.title = audiofile.tag.title
            self.album = audiofile.tag.album
            self.album_artist = audiofile.tag.album_artist

    def set_in_file(self, file_path):
        """

        """
        audiofile = eyed3.load(file_path)
        if audiofile.tag is None:
            audiofile.initTag()
        local_tag_update_needed = (audiofile.tag.artist != self.artist) or (audiofile.tag.title != self.title) or (
                audiofile.tag.album != self.album) or (audiofile.tag.album_artist != self.album_artist)

        if local_tag_update_needed:
            logging.info("***Updating %s locally." % file_path)
            logging.info("***Info: %s" % self)
            audiofile.initTag()
            audiofile.tag.artist = self.artist
            audiofile.tag.title = self.title
            audiofile.tag.album = self.album
            audiofile.tag.album_artist = self.album_artist
            audiofile.tag.save()


class Mp3File(object):
    """
    Represents an mp3 file, together with its metadata and associated normalized-sound file.
    """

    def __init__(self, file_path, mp3_metadata=None, load_tags_from_file=False, normalized_file_path=None):
        self.file_path = file_path
        self.directory = os.path.dirname(file_path)
        self.basename = os.path.basename(file_path)
        self.metadata = mp3_metadata if mp3_metadata is not None else Mp3Metadata()
        if load_tags_from_file:
            self.metadata.get_from_file(self.file_path)

        # Linter complains if instance variables are defined outside __init__, so defining here despite calling set_normalized_file():
        self.normalized_file_path = None
        self.normalized_file = None
        self.set_normalized_file(normalized_file_path=normalized_file_path)

    def __repr__(self):
        return "Mp3File(%s)" % self.file_path

    def save_metadata(self):
        """
        Saves metadata in the corresponding file on disk.
        """
        self.metadata.set_in_file(file_path=self.file_path)

    def is_file_normalized(self):
        """ Does the file_path indicate that this file is normalized?

        :return: 
        """
        return self.normalized_file_path == self.file_path

    def set_normalized_file(self, normalized_file_path=None):
        """ Set details about the normalized file corresponding to this base file.

        :return: 
        """
        if normalized_file_path is None:
            self.normalized_file_path = os.path.join(os.path.dirname(self.directory), "normalized_mp3", self.basename)
        else:
            self.normalized_file_path = normalized_file_path
        if self.is_file_normalized():
            self.normalized_file = self
        else:
            if os.path.isfile(self.normalized_file_path) and os.access(self.normalized_file_path, os.R_OK):
                self.normalized_file = Mp3File(self.normalized_file_path, mp3_metadata=self.metadata, normalized_file_path=self.normalized_file_path)
            else:
                self.normalized_file = None

    def is_normalized_file_outdated(self):
        """ Is the normalized file corresponding to this file outdated?

        :return: 
        """
        return not self.is_file_normalized() and (
                (not os.path.isfile(self.normalized_file_path)) or os.path.getmtime(self.file_path) >= os.path.getmtime(
            self.normalized_file_path))

    def check_loudness(self):
        """ Get some loudness metric.

        :return: 
        """
        from pydub import AudioSegment
        sound = AudioSegment.from_mp3(self.file_path)
        return sound.dBFS

    def save_normalized(self, overwrite=False):
        """ Save the sound-normalized version of this file. 

        Currently the normalzied file produced will be mono-channel, around -16dbFS loud, have the same metadata as the original file.
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

        # Remove leading and ending silence beyond 1s and .5s respectively
        start_trim = max(detect_leading_silence(normalized_sound) - 1000, 0)
        end_trim = max(detect_leading_silence(normalized_sound.reverse()) - 500, 0)
        
        duration = len(normalized_sound)
        normalized_sound = normalized_sound[start_trim:duration-end_trim]
        
        logging.info(normalized_sound.dBFS)
        os.makedirs(os.path.dirname(self.normalized_file_path), exist_ok=True)
        self.metadata.get_from_file(self.file_path)
        normalized_sound.export(self.normalized_file_path, format="mp3", tags={
            "artist": self.metadata.artist, "album_artist": self.metadata.album_artist, "title": self.metadata.title,
            "album": self.metadata.album
        })
        self.set_normalized_file()

    def rename_to_title(self):
        new_basename = filename_from_title(self.metadata.title)
        new_filepath = os.path.join(self.directory, new_basename)
        logging.info("renaming %s to %s", self.file_path, new_filepath)
        os.rename(self.file_path, new_filepath)
        self.basename = new_basename
        self.file_path = new_filepath

def get_normalized_files(mp3_files, skip_missing=True):
    normalized_files_unfiltered = [mp3_file.normalized_file for mp3_file in mp3_files]
    if skip_missing:
        normalized_files_present_only = [mp3_file for mp3_file in normalized_files_unfiltered if mp3_file is not None]
        skipped_files = [mp3_file for mp3_file in normalized_files_unfiltered if mp3_file not in normalized_files_present_only]
        logging.warning("Skipping: %s", pprint.pformat(skipped_files))
        return normalized_files_present_only
    else:
        return normalized_files_unfiltered


def filename_from_title(title):
    title_fixed = title.strip().replace(" ", "_").replace(".mp3", "")
    return title_fixed + ".mp3"
    