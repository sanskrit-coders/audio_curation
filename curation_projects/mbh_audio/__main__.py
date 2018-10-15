from audio_curation import archive_utility
from curation_projects import mbh_audio

archive_id="mahAbhArata-mUla-paThanam-GP"
archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id)
repo = mbh_audio.MbhRepo(git_repo_paths=mbh_audio.repo_paths, archive_audio_item=archive_audio_item)
# repo.reprocess_files(mp3_files=repo.get_particular_normalized_files(["001-009.mp3", "001-027.mp3", "001-028.mp3", "001-043.mp3", ]))
repo.reprocess_files(mp3_files=repo.get_unnormalized_files())
# repo.update_archive_item(mp3_files_in=repo.get_normalized_files(), overwrite_all=False)
# repo.archive_item.update_metadata(metadata=metadata)
# repo.update_git(collapse_history=False)
# repo.archive_item.archive_item.modify_metadata(metadata=metadata)