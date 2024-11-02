import time
import datetime

from chirp.common.printing import cprint


def fake_command(fn):
    """
    Decorator that can be used to easily replace a real command function with
    its mock equivalent. Useful during manual testing.

    """
    mock_func = globals()[fn.__name__]
    return mock_func


def new_artists():
    for i in range(1, 31):
        cprint('Artist #%d' % i)
        time.sleep(0.2)
        yield

    cprint('Found 30 new artists!', type='success')


def update_artist_whitelist():
    for i in range(1, 31):
        cprint('Artist #%d' % i)
        time.sleep(0.2)
        if i == 11:
            raise Exception('Oh no random unexpected error!')
        yield

    cprint('Added 30 new artists!', type='success')


def import_music():
    cprint('Finished!', type='success')
    yield


def push_artist_whitelist():
    cprint('Simulated pushing artist whitelist to git', type='success')
    yield


def check_music():
    for i in range(1, 13):
        kwargs = {}
        if i % 5 == 0:
            kwargs.update(type='error')
        cprint('Track #%d' % i, **kwargs)
        time.sleep(0.2)
        yield

    cprint('Encountered some errors', type='failure')


generate_traktor = new_artists


def upload(date):
    yield
    cprint('Date: {}'.format(date))
    dt = datetime.datetime.strptime(date, '%m/%d/%Y')

    cprint('Pushing artists metadata...')

    cprint('Uploading track changes made since: {:%m/%d/%Y %H:%M}'.format(dt))
    timestamp = time.mktime(dt.timetuple())
    cprint('Using timestamp: {}'.format(timestamp))

    cprint('Pushing track metadata...')

    cprint('Done!', type='success')
