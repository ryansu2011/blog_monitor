import sys
import os
import pathlib
import inspect

# must be direct call
if __name__ != '__main__':
    print(__name__, '__main__', (__name__ is not '__main__'))
    raise Exception("Run this config directly. Do not import.")

# go to root directory, add root to path
main_path_str = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
main_path = pathlib.Path(main_path_str)
for i in range(10):
    if main_path.name != "blog_monitor":
        main_path = main_path.parent
if main_path.name != "blog_monitor":
    raise Exception("Error locating the root directory of 'blog_monitor' project.")
root_path_str = main_path.__str__()
os.chdir(root_path_str)
sys.path.insert(0, root_path_str)
print("Info: added root directory to path. ({})\n".format(root_path_str))

# make and go into temp folder
if not os.path.exists('./temp') or not os.path.isdir('./temp'):
    os.mkdir('./temp')
os.chdir('./temp')
print("Info: current working folder is ({})\n".format(os.getcwd()))


import src.scraper as scraper
from src.snapshot import Snapshot
from src.timer import Timer
from src.notifier import PushBulletNotifier
from src.settings import Settings


last_snapshot = None
push_notifier = None
settings = None


def unit_callback(call_id):
    """
    :param call_id: int caller id from the timer, increment 1 for every time of callback
    :return:
    """
    global settings, last_snapshot

    # crawl data
    ret = scraper.craw_all()

    # put crawled data into snapshot
    snapshot = Snapshot(call_id)
    for data in ret:
        snapshot.push_data(data)

    # if first run
    if last_snapshot is None:
        last_snapshot = snapshot
        return

    # compare new snapshot with old snapshot
    new_articles = snapshot.compare_with(last_snapshot)
    if new_articles.__len__() is 0:
        return
    last_snapshot = snapshot

    # send push notifications
    global push_notifier
    if push_notifier is None:
        raise Exception("Cannot find push notifier.")
    for title in new_articles:
        url = new_articles[title]
        push_notifier.push_link(title, '', url)


def main(config_file_name):
    """
    :param config_file_name: str, name of the configuration json file
    :return:
    """
    global push_notifier, settings

    # read config file
    settings = Settings(config_file_name)

    # tell scraper about the settings
    scraper.settings_ref = settings

    # create notifier
    push_notifier = PushBulletNotifier(settings.token)

    # start timer
    timer = Timer(settings.hours, unit_callback)
    timer.start_counter()


# get tested component
if sys.argv.__len__() <= 1:
    raise Exception("Error. Need to add configuration file name as argument.")
config_file = sys.argv[1]
main(config_file)

