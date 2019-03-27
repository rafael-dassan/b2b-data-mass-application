from Authentication import Helper, Helper2


def my_keyword(arg):
    return _helper_method(arg)


def _helper_method(arg):
    return arg.upper()


def another(arg):
    helper = Helper()
    return helper.test(arg)


def another_keyword(arg):
    return Helper2.my_method(arg)
