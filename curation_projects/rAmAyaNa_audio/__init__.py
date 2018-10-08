"""
`Ramayana audio project`_.

.. _Ramayana audio project: https://sanskrit.github.io/projects/audio/ramayana-audio/
"""

import glob
import logging
import os

# noinspection PyPep8
from audio_curation import audio_repo

# Remove all handlers associated with the root logger object.

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

LOCAL_REPO_BASE_PATH = "/home/vvasuki/rAmAyaNa-audio/"
repo_paths = sorted(glob.glob(os.path.join(LOCAL_REPO_BASE_PATH, "Kanda*")))

class RamayanaRepo(audio_repo.AudioRepo):
    pass


item_description = """
यद्ध्वनिमुद्रणं रामायणस्य तस्येदानीं नकोपि प्रतिकृत्यधिकार 
आरक्ष्यते देहलीस्थसंस्थजनैरिति पाठकयोरन्यतरो हरिसीतारामो ब्रूते । तस्य 
प्रसारेण लोकप्रयोजनं स्यादिति बुद्ध्याङ्गीक्रीयते तैः । विवरणाय 
हरिसीतारामः प्रष्टव्योत्र।

अन्तर्जालप्रकटनसन्दर्भे Credit निमित्तं पाठकयोर्नामनि वक्तव्य इति ।
१. "वेदभाष्यरत्नम्" - ब्रह्मश्री सलक्षणघनपाठी V.श्रीरामः
२. "स्वाध्यायरत्नम्" - ब्रह्मश्री सलक्षणघनपाठी हरिसीताराममूर्तिः

गृहसङ्केतः - Sri Shankara gurukula veda pathashala, Veda Bhavan, Road no.1, Chandragiri colony, Neredmet, Hyderabad - 500056
"""

repo = RamayanaRepo(git_repo_paths=repo_paths, archive_id="Ramayana-recitation-Sriram-harisItArAmamUrti-Ghanapaati-v2", git_remote_origin_basepath="git@github.com:ramayana-audio")
# exit(1)

repo.update_archive_item(mp3_files_in=repo.get_unnormalized_files(), mirror_repo_structure=True, dry_run=False)