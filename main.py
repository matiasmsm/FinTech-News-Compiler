from load_global import load_todo
from control_versiones_automatico_gitpython import subir_version
from crontab import CronTab
from datetime import datetime

entry = CronTab('40 * * * *')
entry.next()

if __name__ == '__main__':
    load_todo()
    subir_version()
