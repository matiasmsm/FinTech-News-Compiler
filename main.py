from load_global import load_todo
from apscheduler.schedulers.blocking import BlockingScheduler
import pinboardOT
import os

if __name__ == '__main__':
	load_todo()
	