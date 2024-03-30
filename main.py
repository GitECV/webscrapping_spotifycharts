import sched
import time
from services.charts_service import ChartsService

scheduler = sched.scheduler(time.time, time.sleep)


def schedule_scrapper():
    scheduler.enter(900, 1, schedule_scrapper)
    ChartsService.spotify_scrap()


if __name__ == '__main__':
    schedule_scrapper()
    # scheduler.run()
