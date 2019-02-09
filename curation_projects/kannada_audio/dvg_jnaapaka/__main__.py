from audio_curation import google_music
from curation_projects.kannada_audio import dvg_jnaapaka

gmusic_client = None
gmusic_client = google_music.GMusicClient(oauth_file_path="/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/oauth_access_token_gmusic.json", username="vishvas.vasuki@gmail.com")

dvg_jnaapaka.upload_volume(title = "ಜ್ಞಾಪಕಚಿತ್ರಶಾಲೆ ಹಲವಾರು-ಸಾರ್ವಜನಿಕರು jnApaka-chitra-shAle halavAru-sArvajanikaru", repo_paths=["/home/vvasuki/kannada-audio/dvg-jnApaka/" + "dvg-jnapaka-chitra-shaale-halavaru-sArvajanikaru"], gmusic_client=gmusic_client, dry_run=False)