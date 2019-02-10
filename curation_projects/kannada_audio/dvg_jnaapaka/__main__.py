from audio_curation import google_music
from curation_projects.kannada_audio import dvg_jnaapaka

gmusic_client = None
gmusic_client = google_music.GMusicClient(oauth_file_path="/home/vvasuki/sysconf/kunchikA/google/sanskritnlp/oauth_access_token_gmusic.json", username="vishvas.vasuki@gmail.com")

# dvg_jnaapaka.upload_volume(title = "ಜ್ಞಾಪಕಚಿತ್ರಶಾಲೆ ಹಲವಾರು-ಸಾರ್ವಜನಿಕರು jnApaka-chitra-shAle halavAru-sArvajanikaru", repo_paths=["/home/vvasuki/kannada-audio/dvg-jnApaka/" + "dvg-jnapaka-chitra-shaale-halavaru-sArvajanikaru"], gmusic_client=gmusic_client, dry_run=False)
# dvg_jnaapaka.upload_volume(title = "ಜ್ಞಾಪಕಚಿತ್ರಶಾಲೆ ಹೃದಯಸಮ್ಪನ್ನರು dvg-jnapaka-chitra-shaale-hRdaya-sampannaru", repo_paths=["/home/vvasuki/kannada-audio/dvg-jnApaka/" + "dvg-jnapaka-chitra-shaale-hRdaya-sampannaru"], gmusic_client=gmusic_client, dry_run=False)
# dvg_jnaapaka.upload_volume(title = "ಜ್ಞಾಪಕಚಿತ್ರಶಾಲೆ ಕಲೋಪಾಸಕರು dvg-jnapaka-chitra-shaale-kalopAsakaru", repo_paths=["/home/vvasuki/kannada-audio/dvg-jnApaka/" + "dvg-jnapaka-chitra-shaale-kalopAsakaru"], gmusic_client=gmusic_client, dry_run=False)
# dvg_jnaapaka.upload_volume(title = "ಜ್ಞಾಪಕಚಿತ್ರಶಾಲೆ ಮೈಸೂರಿನ ದಿವಾನರು dvg-jnapaka-chitra-shaale-maisUrina-dIvAnaru", repo_paths=["/home/vvasuki/kannada-audio/dvg-jnApaka/" + "dvg-jnapaka-chitra-shaale-maisUrina-dIvAnaru"], gmusic_client=gmusic_client, dry_run=False)
# dvg_jnaapaka.upload_volume(title = "ಜ್ಞಾಪಕಚಿತ್ರಶಾಲೆ ಸಾಹಿತಿ-ಸಜ್ಜನ-ಸಾರ್ವಜನಿಕರು dvg-jnapaka-chitra-shaale-sAhiti-sajjana-sArvajanikaru", repo_paths=["/home/vvasuki/kannada-audio/dvg-jnApaka/" + "dvg-jnapaka-chitra-shaale-sAhiti-sajjana-sArvajanikaru"], gmusic_client=gmusic_client, dry_run=False)
dvg_jnaapaka.upload_volume(title = "ಜ್ಞಾಪಕಚಿತ್ರಶಾಲೆ ಸಾಹಿತ್ಯೋಪಾಸಕರು dvg-jnapaka-chitra-shaale-sAhityopAsakaru", repo_paths=["/home/vvasuki/kannada-audio/dvg-jnApaka/" + "dvg-jnapaka-chitra-shaale-sAhityopAsakaru"], gmusic_client=gmusic_client, dry_run=False)
dvg_jnaapaka.upload_volume(title = "ಜ್ಞಾಪಕಚಿತ್ರಶಾಲೆ ಸಂಕೀರ್ಣ ಸ್ಮೃತಿ ಸಮ್ಪುಟ dvg-jnapaka-chitra-shaale-sankIrNa-smRti-sampuTa", repo_paths=["/home/vvasuki/kannada-audio/dvg-jnApaka/" + "dvg-jnapaka-chitra-shaale-sankIrNa-smRti-sampuTa"], gmusic_client=gmusic_client, dry_run=False)
dvg_jnaapaka.upload_volume(title = "ಜ್ಞಾಪಕಚಿತ್ರಶಾಲೆ ವೈದಿಕ-ಧರ್ಮ-ಸಮ್ಪ್ರದಾಯಸ್ಥರು dvg-jnapaka-chitra-shaale-vaidika-dharma-sampradAyastharu", repo_paths=["/home/vvasuki/kannada-audio/dvg-jnApaka/" + "dvg-jnapaka-chitra-shaale-vaidika-dharma-sampradAyastharu"], gmusic_client=gmusic_client, dry_run=False)
dvg_jnaapaka.upload_volume(title = "ಜ್ಞಾಪಕಚಿತ್ರಶಾಲೆ ಬ್ರಹ್ಮಪುರಿಯ ಭಿಕ್ಷುಕ dvg-gaNesh-brahmapuriya-bhixuka", repo_paths=["/home/vvasuki/kannada-audio/dvg-jnApaka/" + "brahmapuriya-bhixuka"], gmusic_client=gmusic_client, dry_run=False, description = "ರಾ ಗಣೇಶ R Ganesh")
