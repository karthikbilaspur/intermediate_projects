from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.config.fileConfig('logging.conf')

def job():
    logging.info("Task executed")

sched = BlockingScheduler()
sched.add_job(job, 'interval', minutes=10)
sched.start()