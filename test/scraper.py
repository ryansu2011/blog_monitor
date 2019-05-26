import src.scraper as scraper
from src.settings import Settings


def start_test():
    # read config file
    settings = Settings("../config/test_config.json")

    # tell scraper about the settings
    scraper.settings_ref = settings

    # scrape
    ret = scraper.craw_all()
    for obj in ret:
        print(obj)
