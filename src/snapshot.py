class Snapshot:

    def __init__(self, call_id):
        """
        :param call_id: int, caller id
        """
        self.call_id = call_id
        self.data = []

    def push_data(self, data):
        """
        :param data: dict[str title, str url]
        :return:
        """
        self.data.append(data)

    def contains_key(self, title):
        """
        :param title: str
        :return: boolean
        """
        for d in self.data:
            if d.__contains__(title):
                return True
        return False

    def compare_with(self, old):
        """
        :param old: Snapshot
        :return: dict{str title, str url}, new items
        """
        new = self
        if new.data.__len__() is not old.data.__len__():
            raise Exception("Warning: inconsistent # of pages in snapshot comparison.")
        if new.call_id <= old.caller_id:
            raise Exception("Warning: comparing to a newer snapshot.")
        ret = {}
        for i in range(new.data.__len__()):
            for new_key in new.data:
                if not old.data.__contains__(new_key):
                    ret[new_key] = new.data[new_key]
        return ret

