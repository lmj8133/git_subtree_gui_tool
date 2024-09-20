from Model.git_model import GitModel

class MainViewModel:
    APP_VERSION = "2.0.0"

    def __init__(self):
        self.model = GitModel()

    def check_git_initialized(self):
        return self.model.is_git_initialized()

    def add_subtree(self, repo_url, subtree_url, ref):
        self.model.git_subtree_add(repo_url, subtree_url, ref)

    def pull_subtree(self, subtree_url, ref):
        self.model.git_subtree_pull(subtree_url, ref)

