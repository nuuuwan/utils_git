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
        cmd = ' '.join(cmd_lines)
        log.debug(cmd)
        os.system('cd ' + self.dir_repo)
        os.system(cmd)

    # Initialization
    def clone(self, dir_repo, branch_name):
        assert dir_repo is not None
        assert branch_name is not None

        self.dir_repo = dir_repo
        self.branch_name = branch_name

        if os.path.exists(dir_repo):
            shutil.rmtree(dir_repo)
            log.debug(f'Removed {dir_repo}')
        os.makedirs(dir_repo)
        log.debug(f'Created {dir_repo}')

        self.run(
            'git clone',
            f'-b {self.branch_name}',
            '--single-branch ',
            self.git_repo_url,
            self.dir_repo,
        )

    # Working on Code
    def status(self):
        return self.run('git status')

    def diff(self):
        return self.run('git diff', '--compact-summary')

    # Staging Changes
    def add(self):
        return self.run('git add', '.')

    # Committing Changes
    def commit(self, message):
        return self.run('git commit', f'-m "{message}"')

    # Synchronization
    def pull(self):
        return self.run('git pull origin', self.branch_name)

    def push(self):
        return self.run('git push origin', self.branch_name)

    # Branching
    def checkout(self, branch_name):
        self.branch_name = branch_name
        return self.run('git checkout', self.branch_name)
