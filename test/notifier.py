from src.notifier import PushBulletNotifier


def _test_pushbullet_nofitier(token):
    my_bullet = PushBulletNotifier(token)
    # test english
    my_bullet.push_link("test title", "test body", "www.google.com")
    # time simplified chinese
    my_bullet.push_link("新消息", "内容", "www.google.com")


def start_test():
    # enter pushbullet token here
    pushbullet_token = "o.rzkPR5DVJjD9T3BWXpHIxHTXv2qXV1vc"
    _test_pushbullet_nofitier(pushbullet_token)
