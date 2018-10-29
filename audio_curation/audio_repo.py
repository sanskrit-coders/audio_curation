import glob

import git
import itertools
import logging
import os

from audio_curation import mp3_utility, archive_utility

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


def update_normalized_mp3s(mp3_files):
    """Regenerate normalized files corresponding to some mp3_files

    :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
    """
    for mp3_file in mp3_files:
        mp3_file.save_normalized(overwrite=True)


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
    def __init__(self, git_repo_paths, archive_audio_item=None, git_remote_origin_basepath=None, normalized_file_namer = basename_based_normalized_file_namer):
        self.git_repo_paths = git_repo_paths
        self.git_repos = [_get_repo(repo_path, git_remote_origin_basepath=git_remote_origin_basepath) for repo_path in git_repo_paths]

        self.base_mp3_file_paths = [item for sublist in
                                    [sorted(glob.glob(os.path.join(repo_path, "mp3", "*.mp3"))) for repo_path in
                                     git_repo_paths] for item in sublist]
        logging.info("Got %d files" % (len(self.base_mp3_file_paths)))
        self.base_mp3_files = list(
            map(lambda fpath: mp3_utility.Mp3File(file_path=fpath, load_tags_from_file=True, normalized_file_path=normalized_file_namer(fpath)), self.base_mp3_file_paths))
        self.archive_item = archive_audio_item

    def get_normalized_files(self):
        """ Get all non-outdated normalized-sound files from this repo. 
    
        :return: List of :py:class:mp3_utility.Mp3File objects
        """
        normalized_files = [file.normalized_file for file in self.base_mp3_files if
                            not file.is_normalized_file_outdated()]
        if len(normalized_files) == 0:
            logging.warning("normalized_files is empty! Out of date? Regenerate them.")
        return normalized_files

    def get_unnormalized_files(self):
        """ Get all 
    
        :return: List of :py:class:mp3_utility.Mp3File objects 
        """
        return [file for file in self.base_mp3_files if file.is_normalized_file_outdated()]

    def delete_obsolete_normalized_files(self):
        normalized_files = self.get_normalized_files()
        normalized_file_paths_retainable = [file.file_path for file in normalized_files]
        normalized_mp3_file_paths = [item for sublist in
                                    [sorted(glob.glob(os.path.join(repo_path, "normalized_mp3", "*.mp3"))) for repo_path in self.git_repo_paths] for item in sublist]
        for file_path in normalized_mp3_file_paths:
            if file_path not in normalized_file_paths_retainable:
                logging.info("Removing obsolete file: %s", file_path)
                os.remove(file_path)

    def get_particular_normalized_files(self, basename_list):
        """ Get normalized-sound files corresponding to basename_list.

        :param basename_list: A list of file names.
        :return: List of :py:class:mp3_utility.Mp3File objects
        """
        return [file.normalized_file for file in self.base_mp3_files if file.basename in basename_list]

    def update_archive_metadata(self, mp3_files):
        """ Update archive metadata based on mp3 file metadata.
    
        :param mp3_files: List of :py:class:mp3_utility.Mp3File objects 
        """
        for mp3_file in mp3_files:
            self.archive_item.update_mp3_metadata(mp3_file=mp3_file)

    def update_metadata(self, mp3_files):
        """ Update mp3 metadata of a bunch of files. Meant to be overridden.

        :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
        """
        pass

    def update_archive_item(self, mp3_files_in, overwrite_all=False, start_at=None, mirror_repo_structure=False,
                            dry_run=False):
        """ Upload a bunch of files to archive.
    
        :param mp3_files_in: List of :py:class:mp3_utility.Mp3File objects
        :param overwrite_all: Boolean 
        :param start_at: String representing the basename of the file to start the uploading with.
        :param mirror_repo_structure: In archive item, place each file in a folder mirroring its local location.
        :param dry_run: Boolean
        """
        mp3_files = mp3_files_in[:]
        if start_at is not None:
            mp3_files = list(itertools.dropwhile(lambda file: file.basename != start_at, mp3_files))
        self.archive_item.update_archive_audio_item(files_in=mp3_files, overwrite_all=overwrite_all, dry_run=dry_run)

    def rename_to_titles(self, mp3_files):
        for mp3_file in mp3_files:
            mp3_file.rename_to_title()

    def reprocess_files(self, mp3_files, update_git=True):
        """ When you add a new file to the repository, use this method to update the metadata, the local normalized file colleciton, archive and git locations.
    
        """
        logging.info("reprocessing %d files", len(mp3_files))
        self.update_metadata(mp3_files=mp3_files)
        if update_git:
            self.update_git()
        self.delete_obsolete_normalized_files()
        update_normalized_mp3s(mp3_files=mp3_files)
        self.update_archive_item(mp3_files_in=mp3_utility.get_normalized_files(mp3_files=mp3_files, skip_missing=True), overwrite_all=True, start_at=None)

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
                    if "master" in [h.name for h in git_repo.branches]:
                        logging.info(git_repo.git.branch("-D", "master"))
                    logging.info(git_repo.git.branch("-m", "master"))
                    logging.info(git_repo.git.push("-f", "origin", "master"))
                else:
                    logging.info(git_repo.git.push("-u", "origin", "master"))
                    # The below would only work if the remote branch is set.
                    # git_repo.remote("origin").push() 
