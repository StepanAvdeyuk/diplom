from django_apscheduler.jobstores import DjangoJobStore, register_events
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from parsing.tasks import update_vacancies

logger = logging.getLogger(__name__)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        update_vacancies,
        trigger=IntervalTrigger(hours=10),
        id="update_vacancies",
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=3600,
        jobstore="default"
    )

    register_events(scheduler)
    scheduler.start()
    logger.info("Scheduler started...")