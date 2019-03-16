from git import Repo, remote
import datetime


def subir_version():
    rw_dir = ''
    repo = Repo(rw_dir)
    repo.git.add(update=True)
    repo.git.commit('-m', 'Nueva recopilación {}'.format(datetime.datetime.now()), author='mamingo@uc.cl')
    #repo.git.commit('-m', 'Nueva recopilación {}'.format(datetime.datetime.now()), author='leonsanz@gmail.com')
    origin = repo.remote(name='origin')
    origin.push()

def crearRepoGit():
    # rorepo is a Repo instance pointing to the git-python repository.
    # For all you know, the first argument to Repo is a path to the repository
    # you want to work with
    repo = Repo(self.rorepo.working_tree_dir)
    assert not repo.bare