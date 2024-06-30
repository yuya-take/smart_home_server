from logger.logger import logger
from scheduler.tasks import schedule_tasks

if __name__ == "__main__":
    logger.info("Starting the scheduler")
    schedule_tasks()
