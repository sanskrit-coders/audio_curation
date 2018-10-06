import logging

import pprint

import pandas

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from indic_transliteration import xsanscript

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)
logging.getLogger('gspread').setLevel(logging.INFO)
logging.getLogger('oauth2client').setLevel(logging.INFO)


def get_sheet(spreadhsheet_id, worksheet_name, google_key):
    """

    :param spreadhsheet_id: 
    :param worksheet_name: 
    :param google_key: 
    :return: 
    """
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_key, scopes)

    client = gspread.authorize(creds)
    logging.debug(pprint.pformat(client.list_spreadsheet_files()))
    sheet_book = client.open_by_key(spreadhsheet_id)
    logging.debug(sheet_book.worksheets())
    return sheet_book.worksheet(worksheet_name)

class EpisodeData(object):
    """
    Represents episode data stored in a Google spreadsheet.
    """
    def __init__(self, spreadhsheet_id, worksheet_name, google_key,
                 episode_id_column, recorder_column):
        """
    
        :return: 
        """
        # noinspection PyPep8Naming
        self.data_sheet = get_sheet(spreadhsheet_id=spreadhsheet_id, worksheet_name=worksheet_name, google_key=google_key)
        self.episode_id_column = episode_id_column
        self.recorder_column = recorder_column
        self.episode_df = None
        self.set_episode_df()

    def _set_episode_df(self):
        """
        
        :return: 
        """
        episode_sheet_values = self.data_sheet.get_all_values()
        episode_df = pandas.DataFrame(episode_sheet_values[1:], columns=episode_sheet_values.pop(0))
        episode_df = episode_df.set_index(self.episode_id_column)
        self.episode_df = episode_df

    def get_recorder(self, episode_id):
        """
        Read the name of the person who recorded this episode.
    
        :param episode_id: 
        :return: 
        """
        artist_devanaagarii = self.episode_df.loc[episode_id, self.recorder_column]
        return "%s %s" % (
        xsanscript.transliterate(artist_devanaagarii, xsanscript.DEVANAGARI, xsanscript.OPTITRANS), artist_devanaagarii)
