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

    :param mp3_files: 
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
    """

    :param mp3_files: 
    """
    for mp3_file in mp3_files:
        mp3_file.save_normalized(overwrite=True)


class AudioRepo(object):
    def __init__(self, git_repo_paths, archive_id):
        self.git_repo_paths = git_repo_paths
        self.git_repos = [git.Repo(repo_path) for repo_path in git_repo_paths]
        self.base_mp3_file_paths = [item for sublist in [sorted(glob.glob(os.path.join(repo_path, "mp3", "*.mp3"))) for repo_path in git_repo_paths] for item in sublist]
        logging.info("Got %d files" % (len(self.base_mp3_file_paths)))
        self.base_mp3_files = list(
            map(lambda fpath: mp3_utility.Mp3File(file_path=fpath, load_tags_from_file=True), self.base_mp3_file_paths))
        self.archive_item = archive_utility.ArchiveAudioItem(archive_id=archive_id)


    def get_normalized_files(self):
        """
    
        :return: 
        """
        normalized_files = [file.normalized_file for file in self.base_mp3_files if not file.is_normalized_file_outdated()]
        if len(normalized_files) == 0:
            logging.warning("normalized_files is empty! Out of date? Regenerate them.")
        return normalized_files
    
    
    def get_unnormalized_files(self):
        """
    
        :return: 
        """
        return [file for file in self.base_mp3_files if file.is_normalized_file_outdated()]
    
    
    def get_particular_normalized_files(self, basename_list):
        return [file.normalized_file for file in self.base_mp3_files if file.basename in basename_list]
    
    
    def update_archive_metadata(self, mp3_files):
        """
    
        :param mp3_files: 
        """
        for mp3_file in mp3_files:
            self.archive_item.update_metadata(mp3_file=mp3_file)


    def update_metadata(self, mp3_files):
        pass


    def update_archive_item(self, mp3_files_in, overwrite_all=False, start_at=None):
        """
    
        :param mp3_files_in: 
        :param overwrite_all: 
        :param start_at: 
        """
        mp3_files = mp3_files_in[:]
        if start_at is not None:
            mp3_files = list(itertools.dropwhile(lambda file: file.basename != start_at, mp3_files))
        self.archive_item.update_archive_item(mp3_files=mp3_files, overwrite_all=overwrite_all)


    def reprocess_files(self, mp3_files):
        """
    
        """
        self.update_metadata(mp3_files=mp3_files)
        self.update_git()
        update_normalized_mp3s(mp3_files=mp3_files)
        self.update_archive_item(mp3_files_in=mp3_files, overwrite_all=True, start_at=None)


    def update_git(self, collapse_history=False):
        def add_untracked(git_repo):
            untracked_files = git_repo.untracked_files.copy()
            assert(False not in set(map(lambda file: file.endswith(".mp3"), untracked_files)))
            git_repo.index.add(untracked_files)
            git_repo.index.commit(message="Added %d mp3-s" % len(untracked_files))

        # In case of collapse_history:
        # Following tip from https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github
        for git_repo in self.git_repos:
            if collapse_history:
                logging.info(git_repo.git.checkout("--orphan", "branch_for_collapsing"))
            add_untracked(git_repo)
            if collapse_history:
                logging.info(git_repo.git.branch("-D", "master"))
                logging.info(git_repo.git.branch("-m", "master"))
                logging.info(git_repo.git.push("-f", "origin", "master"))
            else:
                git_repo.remote("origin").push()
            # git_repo.commit()