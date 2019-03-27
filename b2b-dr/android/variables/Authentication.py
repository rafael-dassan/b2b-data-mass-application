# coding: utf-8
class Helper(object):

    def __init__(self):
        pass

    def test(self, arg):
        return self._helper_method(arg)

    def _helper_method(self, arg):
        return arg.upper()

    @classmethod
    def my_method(self, arg):
        return arg.upper()


class Helper2(object):

    def __init__(self):
        pass

    def test(self, arg):
        return self._helper_method(arg)

    def _helper_method(self, arg):
        return arg.upper()

    @classmethod
    def my_method(self, arg):
        return arg.upper()
