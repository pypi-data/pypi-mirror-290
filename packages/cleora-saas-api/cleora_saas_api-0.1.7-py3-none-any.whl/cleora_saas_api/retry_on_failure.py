import time


def retry_on_failure(fun, arg, repeat_number=7, delay=2):
    try:
        return fun(*arg)
    except Exception as e:
        if repeat_number == 1:
            raise e
        time.sleep(delay)
        return retry_on_failure(fun, arg, repeat_number=repeat_number - 1, delay=delay)