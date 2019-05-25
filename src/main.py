from src.scraper import craw_all, spiderList
from src.snapshot import Snapshot
from src.timer import Timer
from src.notifier import PushBulletNotifier


last_snapshot = None
push_notifier = None


def unit_callback(call_id):
    # crawl data
    ret = craw_all()

    # put crawled data into snapshot
    n = spiderList.__len__()
    snapshot = Snapshot(call_id)
    for i in range(n):
        data = ret.__next__()
        snapshot.push_data(data)

    # if first run
    global last_snapshot
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


def main():
    global push_notifier
    push_notifier = PushBulletNotifier("o.rzkPR5DVJjD9T3BWXpHIxHTXv2qXV1vc")
    notification_hours = [14, 19, 23]
    timer = Timer(notification_hours, unit_callback)
    timer.start_counter()


main()

