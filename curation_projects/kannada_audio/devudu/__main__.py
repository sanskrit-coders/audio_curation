from audio_curation import google_music
from curation_projects.kannada_audio import devudu

gmusic_client = None
gmusic_client = google_music.GMusicClient(oauth_file_path="/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/oauth_access_token_gmusic.json", username="vishvas.vasuki@gmail.com")

devudu.upload_volume(title = "ಮಹಾ-ದರ್ಶನ mahA-darshana", archive_id="mahA-darshana-devuDu-narasimha-shAstrI", repo_paths=["/home/vvasuki/kannada-audio/devuDu/" + "mahA-darshana-devuDu-narasimha-shAstrI"], gmusic_client=gmusic_client, dry_run=False)
devudu.upload_volume(title = "ಮಹಾ-ಕ್ಷತ್ರಿಯ mahA-kShatriya", archive_id="mahA-kShatriya-devuDu-narasimha-shAstrI", repo_paths=["/home/vvasuki/kannada-audio/devuDu/" + "mahA-kShatriya-devuDu-narasimha-shAstrI"], gmusic_client=gmusic_client, dry_run=False)
devudu.upload_volume(title = "ಮಹಾ-ಬ್ರಾಹ್ಮಣ mahA-brAhmaNa", archive_id="MahaBrahmana-by-DevuduAudio", repo_paths=["/home/vvasuki/kannada-audio/devuDu/" + "mahA-brAhmaNa-by-devuDu"], gmusic_client=gmusic_client, dry_run=False)

