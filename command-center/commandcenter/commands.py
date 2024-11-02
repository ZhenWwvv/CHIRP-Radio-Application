import sys
import subprocess
import os.path as op
import time
import datetime

from chirp.common.printing import cprint

from mock_commands import fake_command


def new_artists():
    from chirp.library.do_dump_new_artists_in_dropbox import main_generator
    for _ in main_generator(rewrite=False):
        yield


def update_artist_whitelist():
    from chirp.library import artists
    from chirp.library.do_dump_new_artists_in_dropbox import main_generator
    cwd = op.dirname(artists._WHITELIST_FILE)

    # Make sure the comitted version of the whitelist is checked out.
    # This allows operators to fix mistakes by editing mp3 tags
    # and continuously re-running this task.
    cmd = ['git', 'checkout', artists._WHITELIST_FILE]
    exec_and_print(cmd, cwd)

    # This will reload the artist whitelist file
    # in python memory.
    artists._init()

    for _ in main_generator(rewrite=True):
        yield

    # Show changes to the artist whitelist file
    cprint('Changes made to artist whitelist:')
    cmd = ['git', 'diff', artists._WHITELIST_FILE]
    exec_and_print(cmd, cwd)

    # Once again, this reloads the artist whitelist file
    # in python memory.
    artists._init()


def push_artist_whitelist():
    from chirp.library import artists
    cwd = op.dirname(artists._WHITELIST_FILE)

    # Commit and push.
    cmd = ['git', 'commit', artists._WHITELIST_FILE, '-m', 'Adding new artists']
    exec_and_print(cmd, cwd)
    cmd = ['git', 'push']
    exec_and_print(cmd, cwd)
    cprint('Changes to artist whitelist pushed to git', type='success')

    yield   # to make this function a generator function


def check_music():
    from chirp.library.do_periodic_import import import_albums
    for _ in import_albums(dry_run=True):
        yield


def import_music():
    from chirp.library.do_periodic_import import import_albums
    for _ in import_albums(dry_run=False):
        yield
    cprint('Finished!', type='success')


def generate_traktor():
    from chirp.library.do_generate_collection_nml import main_generator
    for _ in main_generator():
        yield


def upload(date):
    from chirp.library.do_push_artists_to_chirpradio import main_generator
    for _ in main_generator():
        yield

    from chirp.library.do_push_to_chirpradio import main_generator

    # Parse the date string we got from the client.
    dt = datetime.datetime.strptime(date, '%m/%d/%Y')
    cprint('Uploading track changes made since: {:%m/%d/%Y %H:%M}'.format(dt))
    timestamp = time.mktime(dt.timetuple())
    for _ in main_generator(start_timestamp=timestamp):
        yield

    cprint('Finished!', type='success')


def exec_and_print(cmd, cwd):
    cprint(' '.join(cmd), type='highlight')
    output = subprocess.check_output(cmd, cwd=cwd)
    cprint(output)
