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
    """
    
    :param repo_path: 
    :param git_remote_origin_basepath: Example: "git@github.com:kannada-audio" 
    :return: 
    """
    try:
        return git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        if git_remote_origin_basepath is not None:
            repo = git.Repo.init(repo_path)
            remote_origin_path = "%s/%s" % (git_remote_origin_basepath, os.path.basename(repo_path))
            remote_origin_path = remote_origin_path.replace("//", "/")
            repo.create_remote("origin", remote_origin_path)
            return repo
        else:
            raise


def title_based_file_namer(fpath, dir_name):
    metadata = mp3_utility.Mp3Metadata.from_file(fpath)
    if metadata.title is None:
        return basename_based_file_namer(fpath, dir_name=dir_name)
    else:
        new_basename = mp3_utility.filename_from_title(metadata.title)
        return os.path.join(os.path.dirname(os.path.dirname(fpath)), dir_name, new_basename)

def basename_based_file_namer(fpath, dir_name):
    return os.path.join(os.path.dirname(os.path.dirname(fpath)), dir_name, os.path.basename(fpath))


class DerivativeRepo(object):
    """A repo whose files are derived from another DerivativeRepo or AudioRepo"""
    def __init__(self, base_repo, derivative_namer, dir_name, repo_paths=None, archive_audio_item=None, gmusic_client=None):
        self.base_repo = base_repo
        self.dir_name = dir_name
        if repo_paths is None:
            repo_paths = [os.path.join(repo_path, self.dir_name) for repo_path in base_repo.repo_paths]
        self.repo_paths = repo_paths
        self.archive_audio_item = archive_audio_item
        self.gmusic_client = gmusic_client
        self.derivative_namer = derivative_namer

    def get_files(self):
        return [self.derivative_namer(file, dir_name=self.dir_name) for file in self.base_repo.get_files() if os.path.exists(file)]

    def get_derived_files(self):
        """ Get all non-outdated derivative files from this repo. 
    
        :return: List of :py:class:mp3_utility.Mp3File objects
        """
        derived_files = [self.derivative_namer(file.file_path, dir_name=self.dir_name) for file in self.base_repo.get_files() if
                            not self.is_derivative_file_outdated(file.file_path)]
        if len(derived_files) == 0:
            logging.warning("derivative_files is empty! Out of date? Regenerate them.")
        return derived_files

    def get_underived_files(self):
        return [file for file in self.base_repo.get_files() if self.is_derivative_file_outdated(file)]

    def reprocess(self, dry_run=False):
        files_to_upload = self.update_derivatives(dry_run=dry_run)
        self.delete_obsolete_derivatives(dry_run=dry_run)
        self.sync_upload_locations(files=files_to_upload, dry_run=dry_run, overwrite=True)
        # Some files, processed earlier, may not have been uploaded earlier. Hence: 
        self.sync_upload_locations(files=self.get_files(), dry_run=dry_run, overwrite=False)
        return files_to_upload

    def sync_upload_locations(self, files, overwrite=False, dry_run=False):
        self.delete_obsolete_uploaded_files(dry_run=dry_run)

        if self.archive_audio_item is not None:
            self.archive_audio_item.update_archive_item(file_paths=files, overwrite_all=overwrite, dry_run=dry_run)

        # In case of dry_run, the derivative mp3 files are not generated, but gmusic_client needs them.
        if self.gmusic_client is not None and len(files) > 0 and not dry_run:
            mp3_files = [mp3_utility.Mp3File(file_path=file, load_tags_from_file=True) for file in files]
            logging.info(self.gmusic_client.get_album_tracks(mp3_files[0].metadata.album))
            self.gmusic_client.upload(mp3_files=mp3_files, overwrite=overwrite, dry_run=dry_run)


    def update_derivatives(self, dry_run=False):
        if dry_run:
            return [self.derivative_namer(file, dir_name=self.dir_name) for file in self.get_underived_files()]
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

    def delete_obsolete_uploaded_files(self, dry_run=False):
        if self.archive_audio_item is not None:
            self.archive_audio_item.delete_unaccounted_for_files(all_files=self.get_files(), dry_run=dry_run)

        if self.gmusic_client is not None and not dry_run:
            all_mp3_files = [mp3_utility.Mp3File(file_path=file, load_tags_from_file=True) for file in self.get_files()]
            self.gmusic_client.delete_unaccounted_for_files(all_files=all_mp3_files, dry_run=dry_run)


    def update_derivative(self, base_file):
        pass

    def is_derivative_file_outdated(self, base_file_path):
        """ Is the normalized file corresponding to this file outdated?
    
        :return: 
        """
        derivative_path = self.derivative_namer(base_file_path, dir_name=self.dir_name)
        return (not os.path.isfile(derivative_path)) or os.path.getmtime(base_file_path) >= os.path.getmtime(derivative_path)

    def update_metadata(self, mp3_files):
        """ Update mp3 metadata of a bunch of files. Meant to be overridden.

        :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
        """
        pass


class NormalizedRepo(DerivativeRepo):
    def __init__(self, base_repo, derivative_namer=basename_based_file_namer, archive_audio_item=None, gmusic_client=None, normalization_speed_multiplier=1, repo_paths=None):
        super(NormalizedRepo, self).__init__(base_repo=base_repo, derivative_namer=derivative_namer, dir_name="normalized_mp3", archive_audio_item=archive_audio_item, gmusic_client=gmusic_client, repo_paths=repo_paths)
        self.normalization_speed_multiplier = normalization_speed_multiplier
        
    def update_derivative(self, base_file):
        base_mp3 = mp3_utility.Mp3File(file_path=base_file, load_tags_from_file=True)
        # In case of renamed files, observed that the metadata might not get updated (To check). Hence doing the below for good measure.
        self.base_repo.update_derivative(base_file=base_file)
        base_mp3.save_normalized(overwrite=True, speed_multiplier=self.normalization_speed_multiplier, normalized_file_path=self.derivative_namer(base_file, dir_name=self.dir_name))
        return self.derivative_namer(base_file, dir_name=self.dir_name)


class SpeedFileRepo(DerivativeRepo):
    def __init__(self, base_repo, derivative_namer=basename_based_file_namer, archive_audio_item=None,
                 gmusic_client=None, speed_multiplier=1.5, repo_paths=None):
        super(SpeedFileRepo, self).__init__(base_repo=base_repo, derivative_namer=derivative_namer, dir_name="speed_mp3", archive_audio_item=archive_audio_item, gmusic_client=gmusic_client, repo_paths=repo_paths)
        self.speed_multiplier = speed_multiplier

    def update_derivative(self, base_file):
        mp3_utility.Mp3File(file_path=base_file, load_tags_from_file=True).speedup(speed_multiplier=self.speed_multiplier, out_file=self.derivative_namer(base_file, dir_name=self.dir_name))
        self.update_metadata([mp3_utility.Mp3File(file_path=self.derivative_namer(base_file, dir_name=self.dir_name), load_tags_from_file=True)])
        return self.derivative_namer(base_file, dir_name=self.dir_name)

    def update_metadata(self, mp3_files):
        """ Update mp3 metadata of a bunch of files. Meant to be overridden.

        :param mp3_files: List of :py:class:mp3_utility.Mp3File objects
        """
        for mp3_file in mp3_files:
            mp3_file.metadata.album = mp3_file.metadata.album + " 1.5x speed"
            mp3_file.save_metadata()


class BaseAudioRepo(DerivativeRepo):
    """ An Audio file repository.
    The local repository, by default, is assumed to be a collection of git repository working directories (self.repo_paths) with two subfolders:

        - mp3: Containing mp3-s for every "episode" in the repository. 
        - normalized_mp3: Automatically generated from mp3/*.mp3.
    
    Remote staging/ storage can happen via git remotes and an archive item with a given id.
    
    Current recommendations regarding git repos:

        - be mindful of Github repo size limits (1GB as of 2018)
        - setup .gitignore in the repo so as to ignore contents of normalized_mp3
        - periodically collapse git history (using update_git()) so as to avoid wasted space. 
    """
    def __init__(self, repo_paths,
                 archive_audio_item=None,
                 git_remote_origin_basepath=None,
                 gmusic_client=None, dir_name="mp3"):
        super(BaseAudioRepo, self).__init__(base_repo=None, derivative_namer=lambda x, _: x, repo_paths=repo_paths, dir_name=dir_name, archive_audio_item=archive_audio_item, gmusic_client=gmusic_client)
        self.git_repos = [_get_repo(repo_path, git_remote_origin_basepath=git_remote_origin_basepath) for repo_path in repo_paths]

        self.base_mp3_file_paths = [item for sublist in
                                    [sorted(glob.glob(os.path.join(repo_path, self.dir_name, "*.mp3"))) for repo_path in
                                     repo_paths] for item in sublist]
        logging.info("Got %d files" % (len(self.base_mp3_file_paths)))

    def get_files(self):
        return self.base_mp3_file_paths

    def get_derived_files(self):
        return self.get_files()

    def get_underived_files(self):
        """Gets files not updated in git. Not sure how it handles renaming."""
        changed_files= []
        for git_repo in self.git_repos:
            changed_files.extend([ os.path.join(git_repo.working_tree_dir, item.a_path) for item in git_repo.index.diff(None) if os.path.exists(os.path.join(git_repo.working_tree_dir, item.a_path))])
        return changed_files

    def update_derivative(self, base_file):
        """The derivative, in case of a base repo, is usually the file itself."""
        if base_file.endswith("mp3"):
            self.update_metadata([mp3_utility.Mp3File(file_path=base_file, load_tags_from_file=True)])
        return base_file

    def delete_obsolete_derivatives(self, dry_run=False):
        pass

    def reprocess(self, dry_run=False):
        """ When you add a new file to the repository, use this method to update the metadata, the local normalized file colleciton, archive and git locations.

        :returns The list of :py:class:mp3_utility.Mp3File objects which were ultimately processed (could be same as mp3_files, or could be their normalized counterparts).
        """
        self.update_derivatives(dry_run=dry_run)
        self.update_git(dry_run=dry_run)
        return super(BaseAudioRepo, self).reprocess(dry_run=dry_run)

    def update_git(self, collapse_history=False, dry_run=False):
        """ Update git repos associated with this item.

        :param collapse_history: Boolean. Git history involving mp3 files takes up too much space - more than what providers like GitHub offer for free. This option makes this method put up the latest files without any history.
        :param dry_run: Boolean.
        """
        def get_changed_files(repo_x):
            changed_files = [ item.a_path for item in repo_x.index.diff(None) ]
            changed_files.extend(list(filter(lambda path: os.path.basename(os.path.dirname(path)) == "mp3", repo_x.untracked_files)))
            return changed_files

        def add_changed(repo_x, dry_run=False):
            """Add all untracked or changed items in a repo.

            :param repo_x: Some git repo object.
            """
            changed_files = get_changed_files(repo_x=repo_x)
            if len(changed_files) > 0:
                assert (False not in set(map(lambda file: file.endswith(".mp3") or file.endswith("md") or os.path.basename(file) in [".gitignore"], changed_files)))
                for fpath in changed_files:
                    if os.path.exists(os.path.join(repo_x.working_tree_dir, fpath)):
                        logging.info("Adding %s", fpath)
                        if not dry_run:
                            repo_x.index.add([fpath])
                    else:
                        logging.info("Removing %s", fpath)
                        if not dry_run:
                            repo_x.index.remove([fpath],working_tree = True)
                repo_x.index.commit(message="Changed %d files\n\n%s" % (len(changed_files), changed_files))
            return changed_files

        # In case of collapse_history, we are:
        # following tip from https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github
        for git_repo in self.git_repos:
            changed_files = get_changed_files(repo_x=git_repo)
            logging.info("Got %d changed files for %s: %s", len(changed_files), git_repo.git_dir, changed_files)
            if collapse_history or len(changed_files) > 0:
                if (not dry_run) and collapse_history:
                    logging.info(git_repo.git.checkout("--orphan", "branch_for_collapsing"))
                add_changed(git_repo, dry_run=dry_run)
                if not dry_run:
                    if collapse_history:
                        if "master" in [h.name for h in git_repo.branches()]:
                            logging.info(git_repo.git.branch("-D", "master"))
                        logging.info(git_repo.git.branch("-m", "master"))
            
            logging.debug("git_repo.remotes %s", git_repo.remotes)
            if (not dry_run) and len(git_repo.remotes) > 0:
                if collapse_history:
                    logging.info(git_repo.git.push("-f", "origin", "master"))
                else:
                    # We don't do the below so as to be able to deal with uninitialized repositories.
                    # commits_behind = list(git_repo.iter_commits('origin/master..master'))
                    # if len(commits_behind) > 0:
                    logging.info(git_repo.git.push("-u", "origin", "master"))
                    # The below would only work if the remote branch is set.
                    # git_repo.remote("origin").push()
