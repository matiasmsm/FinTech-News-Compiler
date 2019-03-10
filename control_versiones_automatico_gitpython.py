from git import Repo,remote
import datetime


def subir_version():
    rw_dir = '/Users/matiasmingo/Desktop/Banco Central/A:PEGA/Tareas/Recopilación y filtración noticias/Code'
    repo = Repo(rw_dir)
    repo.git.add(update=True)
    repo.git.commit('-m', 'Nueva recopilación {}'.format(datetime.datetime.now()), author='mamingo@uc.cl')
    origin = repo.remote(name='origin')
    origin.push()