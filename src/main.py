from logger.logger import logger
from scheduler.tasks import SmartHomeMonitor

if __name__ == "__main__":
    logger.info("Starting the scheduler")
    monitor = SmartHomeMonitor()
    monitor.schedule_tasks()
