import os
import shutil

from utils_base import Log

log = Log('Git')


class Git:
    def __init__(self, git_repo_url):
        self.git_repo_url = git_repo_url
        self.dir_repo = None
        self.branch_name = None

    def run(self, *cmd_lines):
        assert self.dir_repo is not None
        cmd_lines = ['cd', self.dir_repo, '&&'] + list(cmd_lines)
        cmd = ' '.join(cmd_lines)
        log.debug(cmd)

        os.system(cmd)

    def __init_dir_repo__(self, dir_repo):
        self.dir_repo = dir_repo

        if os.path.exists(dir_repo):
            shutil.rmtree(dir_repo)
            log.debug(f'Removed {dir_repo}')
        os.makedirs(dir_repo)
        log.debug(f'Created {dir_repo}')

    # Initialization
    def clone(self, dir_repo, branch_name):
        # Clone (or copy) a repository from an existing URL.
        assert dir_repo is not None
        assert branch_name is not None

        self.__init_dir_repo__(dir_repo)
        self.branch_name = branch_name

        self.run(
            'git clone',
            f'-b {self.branch_name}',
            '--single-branch ',
            self.git_repo_url,
            self.dir_repo,
        )

    # Working on Code
    def status(self):
        # Check the status of your changes
        return self.run('git status')

    def diff(self):
        # Check the status of your changes
        return self.run('git diff', '--compact-summary')

    # Staging Changes
    def add(self):
        # Add all changes in the current directory to the staging area
        return self.run('git add', '.')

    # Committing Changes
    def commit(self, message):
        # Commit changes that have been added to the staging area with a
        # message describing the changes
        return self.run('git commit', f'-m "{message}"')

    # Synchronization
    def pull(self):
        # Download changes and directly merge into the current branch
        return self.run('git pull origin', self.branch_name)

    def push(self):
        # Download changes and directly merge into the current branch
        return self.run('git push origin', self.branch_name)

    # Branching
    def branch(self, branch_name):
        # Create a new branch
        self.branch_name = branch_name
        return self.run('git branch', self.branch_name)

    def checkout(self, branch_name):
        # Switch to another branch
        self.branch_name = branch_name
        return self.run('git checkout', self.branch_name)
