import src.notifier as nt


def test_pushbullet_nofitier():
    my_bullet = nt.PushBulletNotifier("o.rzkPR5DVJjD9T3BWXpHIxHTXv2qXV1vc")
    my_bullet.push_link("新消息", "内容", "www.google.com")


test_pushbullet_nofitier()
