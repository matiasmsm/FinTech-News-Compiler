from load_global import load_todo
from apscheduler.schedulers.blocking import BlockingScheduler
import pinboardOT
import os


sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=5)
def timed_job():
    load_todo()
sched.start()
#pinboardOT.obtener_posts()