from audio_curation import google_music
from audio_curation.episode_data import google_sheets_data
from curation_projects import kannada_audio

gmusic_client = None
gmusic_client = google_music.GMusicClient(oauth_file_path="/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/oauth_access_token_gmusic.json", username="vishvas.vasuki@gmail.com")

kannada_audio.upload_volume(title ="havyaka hADugaLu ಹವ್ಯಕ ಹಾಡುಗಳು", archive_id="havyaka_hADugaLu", author="ಹವ್ಯಕರು", reader="ಸುಭದ್ರಾ", repo_paths=["/home/vvasuki/kannada-audio/" + "havyaka-hadu-by-subhadra"], gmusic_client=gmusic_client, dry_run=False)

# rangapriya svAmI\
# episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1MvZ9lGzxEpI23O4q938qvwagknF7m3eZZp6SuNxbECk", worksheet_name="habba", google_key = '/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', episode_id_column="current filename", title_column="new title", script="en")
# kannada_audio.upload_volume(title ="ಭಾರತೀಯ-ಹಬ್ಬ-ಆಚರಣೆಗಳು bhAratIya habba AcharaNegaLu", archive_id="bhAratIya-habba-AcharaNegaLu-rangapriya-swamy", reader="ವಾಸುಕಿ-ನಾಗರತ್ನಾ vAsuki-nAgaratnA", author="ರಂಗಪ್ರಿಯ-ಸ್ವಾಮಿ rangapriya-svAmI", episode_data=episode_data, repo_paths=["/home/vvasuki/kannada-audio/" + "bhAratIya-habba-AcharaNegaLu-rangapriya-swamy"], gmusic_client=gmusic_client, dry_run=False)


# gorur
# episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1MvZ9lGzxEpI23O4q938qvwagknF7m3eZZp6SuNxbECk", worksheet_name="rasikaru", google_key = '/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', episode_id_column="current filename", title_column="new title", script="en")
# kannada_audio.upload_volume(title ="ನಮ್ಮೂರ ರಸಿಕರು nammUra rasikaru", archive_id="nammuura-rasikaru", reader="ಕಡಬ-ವಾಸುಕಿ kaDaba-vAsuki", author="ಗೊರೂರು ರಾಮಸ್ವಾಮಿ ಅಯ್ಯಂಗಾರ್ Gorur Ramaswami Iyengar", episode_data=episode_data, repo_paths=["/home/vvasuki/kannada-audio/" + "nammuura-rasikaru"], gmusic_client=gmusic_client, dry_run=False)

# devuDu

# episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1MvZ9lGzxEpI23O4q938qvwagknF7m3eZZp6SuNxbECk", worksheet_name="m-darshana", google_key = '/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', episode_id_column="original_filename", title_column="new title", script="en")
# kannada_audio.upload_volume(title ="ಮಹಾ-ದರ್ಶನ mahA-darshana", archive_id="mahA-darshana-devuDu-narasimha-shAstrI",  reader="ಕಡಬ-ವಾಸುಕಿ kaDaba-vAsuki", author="ದೇವುಡು ನರಸಿಂಹ-ಶಾಸ್ತ್ರೀ devuDu-narasimha-shAstrI", episode_data=episode_data, repo_paths=["/home/vvasuki/kannada-audio/devuDu/" + "mahA-darshana-devuDu-narasimha-shAstrI"], episode_data=episode_data, gmusic_client=gmusic_client, dry_run=False)
# episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1MvZ9lGzxEpI23O4q938qvwagknF7m3eZZp6SuNxbECk", worksheet_name="m-kShatriya", google_key = '/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', episode_id_column="original_filename", title_column="new title", script="en")
# kannada_audio.upload_volume(title ="ಮಹಾ-ಕ್ಷತ್ರಿಯ mahA-kShatriya", archive_id="mahA-kShatriya-devuDu-narasimha-shAstrI",  reader="ಕಡಬ-ವಾಸುಕಿ kaDaba-vAsuki", author="ದೇವುಡು ನರಸಿಂಹ-ಶಾಸ್ತ್ರೀ devuDu-narasimha-shAstrI", episode_data=episode_data, repo_paths=["/home/vvasuki/kannada-audio/devuDu/" + "mahA-kShatriya-devuDu-narasimha-shAstrI"], gmusic_client=gmusic_client, dry_run=False)
# episode_data = google_sheets_data.EpisodeData(spreadhsheet_id="1MvZ9lGzxEpI23O4q938qvwagknF7m3eZZp6SuNxbECk", worksheet_name="m-darshana", google_key = '/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/service_account_key.json', episode_id_column="original_filename", title_column="new title", script="en")
# kannada_audio.upload_volume(title ="ಮಹಾ-ಬ್ರಾಹ್ಮಣ mahA-brAhmaNa", archive_id="MahaBrahmana-by-DevuduAudio",  reader="ಕಡಬ-ವಾಸುಕಿ kaDaba-vAsuki", author="ದೇವುಡು ನರಸಿಂಹ-ಶಾಸ್ತ್ರೀ devuDu-narasimha-shAstrI", episode_data=episode_data, repo_paths=["/home/vvasuki/kannada-audio/devuDu/" + "mahA-brAhmaNa-by-devuDu"], gmusic_client=gmusic_client, dry_run=False)

