import requests
import json


class PushBulletNotifier:
    """Use PushBullet service to send push notifications."""

    _url_me = "https://api.pushbullet.com/v2/users/me"
    _url_device = "https://api.pushbullet.com/v2/devices"
    _url_push = "https://api.pushbullet.com/v2/pushes"

    def __init__(self, token):
        """
        :param token: str, pushbullet token
        """
        self._key = token
        self._email = ''
        self._name = ''
        self._device_id = ''
        self._device_token = ''
        print('Initializing PushBulletNotifier:')
        print('    Auth Token = {}'.format(token))
        self._get_myself()
        self._get_devices()

    def _get_myself(self):
        header = {'Access-Token': self._key}
        ret = requests.get(PushBulletNotifier._url_me, headers=header)
        if ret.status_code is not 200:
            raise Exception('Unexpected HTTP status code {} in _get_myself.'.format(ret.status_code))
        self._email = _get_json_entry(ret.json(), 'email', '_get_myself')
        self._name = _get_json_entry(ret.json(), 'name', '_get_myself')
        print('Getting user profile:')
        print('    email address = {}'.format(self._email))
        print('    user name = {}'.format(self._name))

    def _get_devices(self):
        header = {'Access-Token': self._key}
        ret = requests.get(PushBulletNotifier._url_device, headers=header)
        if ret.status_code is not 200:
            raise Exception('Unexpected HTTP status code {} in _get_devices.'.format(ret.status_code))
        devices = _get_json_entry(ret.json(), 'devices', '_get_devices')
        if devices is None or devices.__len__() is 0:
            raise Exception('Cannot get the device list in _get_devices.')
        print('    List of devices:')
        for i in range(devices.__len__()):
            dv = devices[i]
            print('       Device #{}:'.format(i))
            print('                Active:{}'.format(dv['active']))
            print('                Nickname:{}'.format(dv['nickname']))
            print('                Manufacturer:{}'.format(dv['manufacturer']))
            print('                Model:{}'.format(dv['model']))
        while True:
            inp = input('    Enter the device number for receiving push notifications:')
            try:
                idx = int(inp)
            except ValueError:
                print('    Invalid input, please try again.')
                continue
            if idx < 0 or idx >= devices.__len__():
                print('    Invalid input, please try again.')
                continue
            print('    Selected device #{}:{}'.format(idx, devices[idx]['nickname']))
            break
        self._device_id = devices[idx]['iden']
        self._device_token = devices[idx]['push_token']

    def push_link(self, title, body, url):
        """
        :param title: str, message title
        :param body: str, message body
        :param url: str, message url
        :return:
        """
        header = {
            'Access-Token': self._key,
            'Content-Type': 'application/json'
        }
        data = {
            "device_iden": self._device_id,
            "type": "link",
            "title": title,
            "body": body,
            "url": url
        }
        ret = requests.post(PushBulletNotifier._url_push, headers=header, data=json.dumps(data))
        if ret.status_code is not 200:
            raise Exception('Unexpected HTTP status code {} in push_link.'.format(ret.status_code))


def _get_json_entry(json_object, attribute_name, caller):
    """
    :param json_object: dict[str, xx]
    :param attribute_name: str, attribute name
    :param caller: str, name of the caller function
    :return:
    """
    if json_object.__contains__(attribute_name):
        return json_object[attribute_name]
    raise Exception('Cannot find attribute {} in {}.'.format(attribute_name, caller))
