import json


class Settings:

    def __init__(self, filename):
        """
        :param filename: str, file name for configuration file
        """
        with open(filename, 'r') as f:
            ret = json.load(f)
        f.close()
        if ret is None:
            raise Exception("Cannot load configuration file.")
        self.token = Settings._get_item(ret, "pushbullet token")
        self.hours = Settings._get_item(ret, "notification hours")
        sites = Settings._get_item(ret, "monitored sites")
        for site in sites:
            Settings._check_site_attribute(site, "url")
            Settings._check_site_attribute(site, "title xpath")
            Settings._check_site_attribute(site, "href xpath")
        self.n = sites.__len__()
        self.url_list = [site["url"] for site in sites]
        self.title_xpath_list = [site["title xpath"] for site in sites]
        self.href_xpath_list = [site["href xpath"] for site in sites]
        self.temp_file_name = ["temp_file_{}.json".format(i) for i in range(1, self.n + 1)]

    @staticmethod
    def _get_item(dic, key):
        """
        :param dic: dict, lookup dictionary
        :param key: str, key string
        :return: type not fixed, the value
        """
        if not dic.__contains__(key):
            raise Exception("Error reading configuration file, cannot find {}".format(key))
        ret = dic[key]
        if ret is None:
            raise Exception("Error reading configuration file, cannot find {}".format(key))
        if type(ret) is list:
            if ret.__len__() is 0:
                raise Exception("Error reading configuration file, find empty list:{}".format(key))
        return ret

    @staticmethod
    def _check_site_attribute(site, attribute_name):
        """
        :param site: dict, site object
        :param attribute_name: str
        :return:
        """
        if not site.__contains__(attribute_name):
            raise Exception("Error reading configuration file, cannot find {} for site.".format(attribute_name))
        if site[attribute_name] is None:
            raise Exception("Error reading configuration file, empty field for {}.".format(attribute_name))

