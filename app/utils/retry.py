import time


def retry(function, retries=3):

    last_error = None

    for _ in range(retries):

        try:

            return function()

        except Exception as error:

            last_error = error

            time.sleep(1)

    raise last_error