from load_global import load_todo
from apscheduler.schedulers.blocking import BlockingScheduler
import pinboardOT

if __name__ == '__main__':
    """scheduler = BlockingScheduler()
    scheduler.add_job(load_todo)
    scheduler.add_job(load_todo, 'interval', minutes=30)
    scheduler.start()
    """
    load_todo()
    #pinboardOT.obtener_posts()