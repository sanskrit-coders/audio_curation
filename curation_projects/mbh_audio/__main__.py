import glob
import logging

import pprint

from audio_curation import archive_utility, audio_repo
from curation_projects import mbh_audio

# Remove all handlers associated with the root logger object.

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)

dry_run = False
repo = mbh_audio.MbhRepoBase(repo_paths=mbh_audio.repo_paths, git_remote_origin_basepath="git@github.com:mahabharata-audio-2018")
logging.info(pprint.pformat(repo.reprocess(dry_run=dry_run)))

archive_id="mahAbhArata-mUla-paThanam-GP"
archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id)
# [archive_audio_item.update_mp3_metadata(mp3_file=file) for file in glob.glob("/home/vvasuki/mahabharata-audio-2018/parva01-101-233/normalized_mp3/001-137p0*.mp3")]
# exit()
normalized_files_repo = audio_repo.NormalizedRepo(base_repo=repo, archive_audio_item=archive_audio_item)
logging.info(pprint.pformat(normalized_files_repo.reprocess(dry_run=dry_run)))

archive_id="mahAbhArata-mUla-paThanam-GP-150p-speed"
archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id)
archive_audio_item.update_metadata(metadata=mbh_audio.SpeedFileRepo.metadata)
speed_files_repo = mbh_audio.SpeedFileRepo(base_repo=normalized_files_repo, archive_audio_item=archive_audio_item)
logging.info(pprint.pformat(speed_files_repo.reprocess(dry_run=dry_run)))

