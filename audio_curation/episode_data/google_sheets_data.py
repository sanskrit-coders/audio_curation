import logging

from indic_transliteration import xsanscript

from curation_utils.google import sheets

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)


class EpisodeData(sheets.IndexSheet):
    """
    Represents episode data stored in a Google spreadsheet.
    """
    def __init__(self, spreadhsheet_id, worksheet_name, google_key,
                 episode_id_column, recorder_column=None, title_column=None, script=xsanscript.DEVANAGARI):
        super(EpisodeData, self).__init__(spreadhsheet_id=spreadhsheet_id, worksheet_name=worksheet_name, google_key=google_key, id_column=episode_id_column)
        self.recorder_column = recorder_column
        self.title_column = title_column
        self.script = script

    def get_recorder(self, episode_id):
        """
        Read the name of the person who recorded this episode.
    
        :param episode_id: 
        :return: 
        """
        if self.script == xsanscript.DEVANAGARI:
            artist_devanaagarii = self._df.loc[episode_id, self.recorder_column]
            return "%s %s" % (
            xsanscript.transliterate(artist_devanaagarii, xsanscript.DEVANAGARI, xsanscript.OPTITRANS), artist_devanaagarii)
        else:
            return self._df.loc[episode_id, self.recorder_column]

    def get_title(self, episode_id):
        """
        Read the title of this episode.
    
        :param episode_id: 
        :return: 
        """
        if self._df.index.name == self.title_column:
            title_base = episode_id
        else:
            title_base = self._df.loc[episode_id, self.title_column]
        if self.script == xsanscript.DEVANAGARI:
            title_devanaagarii = title_base
            return "%s %s" % (
                xsanscript.transliterate(title_devanaagarii, xsanscript.DEVANAGARI, xsanscript.OPTITRANS), title_devanaagarii)
        else:
            return title_base
