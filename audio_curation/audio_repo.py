import glob
import itertools
import logging
import os

import git

from audio_curation import mp3_utility

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s"
)


def check_loudness(mp3_files):
    """
    Get some stats about loudness levels among a bunch of mp3 files.

    :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
    """
    loudnesses = list(map(lambda mp3_file: mp3_file.check_loudness(), mp3_files))
    local_mp3_file_basenames = list(map(lambda x: x.basename, mp3_files))
    import pandas
    basenames_to_loudnesses = pandas.DataFrame({"basename": local_mp3_file_basenames, "loudness": loudnesses})
    basenames_to_loudnesses.set_index("basename")
    logging.info(basenames_to_loudnesses)
    logging.info("min %d", basenames_to_loudnesses["loudness"].min())
    logging.info("mean %d", basenames_to_loudnesses["loudness"].mean())
    logging.info("max %d", basenames_to_loudnesses["loudness"].max())
    logging.info("deviation %f", basenames_to_loudnesses["loudness"].std())


def _get_repo(repo_path, git_remote_origin_basepath=None):
    try:
        return git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        assert git_remote_origin_basepath is not None, "Pass valid git repos, or specify git_remote_origin_basepath so that we may initialize repos for you."
        repo = git.Repo.init(repo_path)
        remote_origin_path = "%s/%s" % (git_remote_origin_basepath, os.path.basename(repo_path))
        remote_origin_path = remote_origin_path.replace("//", "/")
        repo.create_remote("origin", remote_origin_path)
        return repo


def title_based_normalized_file_namer(fpath):
    metadata = mp3_utility.Mp3Metadata.from_file(fpath)
    if metadata.title is None:
        return basename_based_normalized_file_namer(fpath)
    else:
        new_basename = mp3_utility.filename_from_title(metadata.title)
        return os.path.join(os.path.dirname(os.path.dirname(fpath)), "normalized_mp3", new_basename)

def basename_based_normalized_file_namer(fpath):
    return os.path.join(os.path.dirname(os.path.dirname(fpath)), "normalized_mp3", os.path.basename(fpath))


class DerivativeRepo(object):
    """A repo whose files are derived from another DerivativeRepo or AudioRepo"""
    def __init__(self, base_repo, derivative_namer, repo_paths=None, archive_audio_item=None,
                 gmusic_client=None):
        self.base_repo = base_repo
        if repo_paths is None:
            self.repo_paths = []
        self.archive_audio_item = archive_audio_item
        self.gmusic_client = gmusic_client
        self.derivative_namer = derivative_namer

    def get_files(self):
        return [self.derivative_namer(file) for file in self.base_repo.get_files() if os.path.exists(file)]

    def get_derived_files(self):
        """ Get all non-outdated derivative files from this repo. 
    
        :return: List of :py:class:mp3_utility.Mp3File objects
        """
        derived_files = [self.derivative_namer(file.file_path) for file in self.base_repo.get_files() if
                            not self.is_derivative_file_outdated(file.file_path)]
        if len(derived_files) == 0:
            logging.warning("derivative_files is empty! Out of date? Regenerate them.")
        return derived_files

    def get_underived_files(self):
        return [file for file in self.base_repo.get_files() if self.is_derivative_file_outdated(file)]

    def reprocess(self, dry_run=False):
        files_to_upload = self.update_derivatives(dry_run=dry_run)
        self.delete_obsolete_derivatives(dry_run=dry_run)
        if self.archive_audio_item is not None:
            self.archive_audio_item.update_archive_item(file_paths=files_to_upload, overwrite_all=True, dry_run=dry_run)
            self.archive_audio_item.delete_unaccounted_for_files(all_files=self.get_files(), dry_run=dry_run)
        # In case of dry_run, the derivative mp3 files are not generated, but gmusic_client needs them.
        if self.gmusic_client is not None and len(files_to_upload) > 0 and not dry_run:
            mp3_files = [mp3_utility.Mp3File(file_path=file, load_tags_from_file=True) for file in files_to_upload]
            logging.info(self.gmusic_client.get_album_tracks(mp3_files[0].metadata.album))
            self.gmusic_client.upload(mp3_files=mp3_files, overwrite=True, dry_run=dry_run)
            all_mp3_files = [mp3_utility.Mp3File(file_path=file, load_tags_from_file=True) for file in self.get_files()]
            self.gmusic_client.delete_unaccounted_for_files(all_files=all_mp3_files, dry_run=dry_run)
        return files_to_upload

    def update_derivatives(self, dry_run=False):
        if dry_run:
            return [self.derivative_namer(file) for file in self.get_underived_files()]
        else:
            underived_files = self.get_underived_files()
            return [self.update_derivative(file) for file in underived_files]

    def delete_obsolete_derivatives(self, dry_run=False):
        derivatives_retainable = self.get_files()
        repo_contents = [item for sublist in [sorted(glob.glob(os.path.join(repo_path, "*"))) for repo_path in self.repo_paths] for item in sublist]
        for file_path in repo_contents:
            if file_path not in derivatives_retainable:
                logging.info("Removing obsolete file: %s", file_path)
                if not dry_run:
                    os.remove(file_path)

    def update_derivative(self, base_file):
        pass

    def is_derivative_file_outdated(self, base_file_path):
        """ Is the normalized file corresponding to this file outdated?
    
        :return: 
        """
        derivative_path = self.derivative_namer(base_file_path)
        return (not os.path.isfile(derivative_path)) or os.path.getmtime(base_file_path) >= os.path.getmtime(derivative_path)


class NormalizedRepo(DerivativeRepo):
    def __init__(self, base_repo, derivative_namer=basename_based_normalized_file_namer, archive_audio_item=None,
                 gmusic_client=None, normalization_speed_multiplier=1):
        self.normalization_speed_multiplier = normalization_speed_multiplier
        super(NormalizedRepo, self).__init__(base_repo=base_repo, derivative_namer=derivative_namer, archive_audio_item=archive_audio_item, gmusic_client=gmusic_client)
        
    def update_derivative(self, base_file):
        mp3_utility.Mp3File(file_path=base_file, load_tags_from_file=True).save_normalized(overwrite=True, speed_multiplier=self.normalization_speed_multiplier, normalized_file_path=self.derivative_namer(base_file))
        return self.derivative_namer(base_file)


class AudioRepo(object):
    """ An Audio file repository.
    The local repository, by default, is assumed to be a collection of git repository working directories (self.git_repo_paths) with two subfolders:

        - mp3: Containing mp3-s for every "episode" in the repository. 
        - normalized_mp3: Automatically generated from mp3/*.mp3.
    
    Remote staging/ storage can happen via git remotes and an archive item with a given id.
    
    Current recommendations regarding git repos:

        - be mindful of Github repo size limits (1GB as of 2018)
        - setup .gitignore in the repo so as to ignore contents of normalized_mp3
        - periodically collapse git history (using update_git()) so as to avoid wasted space. 
    """
    def __init__(self, git_repo_paths, 
                 archive_audio_item=None, 
                 git_remote_origin_basepath=None,
                 gmusic_client=None):
        self.git_repo_paths = git_repo_paths
        self.git_repos = [_get_repo(repo_path, git_remote_origin_basepath=git_remote_origin_basepath) for repo_path in git_repo_paths]

        self.base_mp3_file_paths = [item for sublist in
                                    [sorted(glob.glob(os.path.join(repo_path, "mp3", "*.mp3"))) for repo_path in
                                     git_repo_paths] for item in sublist]
        logging.info("Got %d files" % (len(self.base_mp3_file_paths)))
        self.archive_item = archive_audio_item
        self.gmusic_client = gmusic_client

    def get_files(self):
        return self.base_mp3_file_paths

    def update_metadata(self, mp3_files):
        """ Update mp3 metadata of a bunch of files. Meant to be overridden.

        :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
        """
        pass

    def rename_to_titles(self, mp3_files):
        for mp3_file in mp3_files:
            mp3_file.rename_to_title()

    def reprocess_files(self, mp3_files, update_git=True, dry_run=False):
        """ When you add a new file to the repository, use this method to update the metadata, the local normalized file colleciton, archive and git locations.
    
        
        :returns The list of :py:class:mp3_utility.Mp3File objects which were ultimately processed (could be same as mp3_files, or could be their normalized counterparts).
        """
        logging.info("reprocessing %d files", len(mp3_files))
        self.update_metadata(mp3_files=mp3_files)
        if update_git:
            self.update_git()
        files_to_upload = mp3_files
        if self.archive_item is not None:
            self.archive_item.update_archive_audio_item(mp3_files_in=files_to_upload, overwrite_all=True, dry_run=dry_run)
        if self.gmusic_client is not None and len(files_to_upload) > 0:
            logging.debug(self.gmusic_client.get_album_tracks(files_to_upload[0].metadata.album))
            self.gmusic_client.upload(mp3_files=files_to_upload, overwrite=True, dry_run=dry_run)
        return files_to_upload

    def delete_unaccounted_for_files(self, dry_run=False):
        if self.archive_item is not None:
            self.archive_item.delete_unaccounted_for_files(all_files=self.get_files(), dry_run=dry_run)
        if self.gmusic_client is not None:
            mp3_files = [mp3_utility.Mp3File(file_path=file, load_tags_from_file=True) for file in self.get_files()]            
            self.gmusic_client.delete_unaccounted_for_files(all_files=mp3_files, dry_run=dry_run)

    def update_git(self, collapse_history=False, first_push=False):
        """ Update git repos associated with this item.

        :param collapse_history: Boolean. Git history involving mp3 files takes up too much space - more than what providers like GitHub offer for free. This option makes this method put up the latest files without any history.
        :param first_push: Boolean. Do  git push --set-upstream origin master in such cases.
        """

        def add_changed(repo_x):
            """Add all untracked or changed items in a repo.

            :param repo_x: Some git repo object.
            """
            changed_files = [ item.a_path for item in repo_x.index.diff(None) ]
            if len(changed_files) > 0:
                assert (False not in set(map(lambda file: file.endswith(".mp3") or file.endswith("md") or os.path.basename(file) in [".gitignore"], changed_files)))
                for fpath in changed_files:
                    if os.path.exists(os.path.join(repo_x.working_tree_dir, fpath)):
                        repo_x.index.add([fpath])
                    else:
                        repo_x.index.remove([fpath],working_tree = True)
                repo_x.index.commit(message="Changed %d files\n\n%s" % (len(changed_files), changed_files))
            return len(changed_files)

        # In case of collapse_history, we are:
        # following tip from https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github
        for git_repo in self.git_repos:
            commits_behind = git_repo.iter_commits('master..origin/master')
            changed_files = [ item.a_path for item in git_repo.index.diff(None) ]
            logging.info("Got %d changed files for %s: %s", len(changed_files), git_repo.git_dir, changed_files)
            if collapse_history or len(changed_files) > 0 or len(list(commits_behind)) > 0:
                if collapse_history:
                    logging.info(git_repo.git.checkout("--orphan", "branch_for_collapsing"))
                add_changed(git_repo)
                if collapse_history:
                    if "master" in [h.name for h in git_repo.branches()]:
                        logging.info(git_repo.git.branch("-D", "master"))
                    logging.info(git_repo.git.branch("-m", "master"))
                    logging.info(git_repo.git.push("-f", "origin", "master"))
                else:
                    logging.info(git_repo.git.push("-u", "origin", "master"))
                    # The below would only work if the remote branch is set.
                    # git_repo.remote("origin").push() 
