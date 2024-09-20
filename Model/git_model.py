import os
import subprocess
import sys

class GitModel:
    def __init__(self):
        pass

    def is_git_initialized(self):
        """Check if the .git directory exists in the current directory."""
        return os.path.isdir(".git")

    def execute_git_commands(self, commands):
        """Execute a list of git commands."""
        for cmd in commands:
            subprocess.run(cmd, check=True)

    def git_subtree_add(self, repo_url, subtree_url, ref):
        """Add a git subtree."""
        git_executable = self._get_git_executable()

        commands = [
            [git_executable, 'config', '--global', 'core.autocrlf', 'false'],
            [git_executable, 'init'],
            [git_executable, 'remote', 'add', 'origin', repo_url],
            [git_executable, 'add', '--all'],
            [git_executable, 'commit', '-m', ':tada: Initial Commit'],
            [git_executable, 'subtree', 'add', '--prefix', 'subtree', subtree_url, ref]
        ]
        self.execute_git_commands(commands)

    def git_subtree_pull(self, subtree_url, ref):
        """Pull changes from a git subtree."""
        git_executable = self._get_git_executable()

        commands = [
            [git_executable, 'subtree', 'pull', '--prefix', 'subtree', subtree_url, ref]
        ]
        self.execute_git_commands(commands)

    def _get_git_executable(self):
        """Get the path to the git executable."""
        git_executable = os.path.join(sys._MEIPASS, 'PortableGit', 'bin', 'git.exe')
        if not os.path.exists(git_executable):
            raise FileNotFoundError(f"Git executable not found at: {git_executable}")
        return git_executable

