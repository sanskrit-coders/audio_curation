from audio_curation import archive_utility
from curation_projects import rAmAyaNa_audio
archive_id="Ramayana-recitation-Sriram-harisItArAmamUrti-Ghanapaati-v2"
archive_audio_item = archive_utility.ArchiveAudioItem(archive_id=archive_id)
repo = rAmAyaNa_audio.RamayanaRepoBase(repo_paths=rAmAyaNa_audio.repo_paths, archive_audio_item=archive_audio_item, git_remote_origin_basepath="git@github.com:ramayana-audio")
# repo.update_git(collapse_history=False, first_push=True)
# exit(1)
# repo.archive_item.update_metadata(metadata=metadata)
# repo.update_archive_item(mp3_files_in=repo.get_unnormalized_files(), mirror_repo_structure=True, dry_run=False)