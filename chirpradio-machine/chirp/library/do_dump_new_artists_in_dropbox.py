#!/usr/bin/env python

import codecs
import sys
from chirp.common.printing import cprint
from chirp.library import artists
from chirp.library import dropbox


def main_generator(rewrite):
    drop = dropbox.Dropbox()
    new_artists = set()
    for au_file in drop.tracks():
        try:
            tpe1 = au_file.mutagen_id3["TPE1"].text[0]
        except:
            cprint(u'** file: %r' % au_file.path)
            raise
        standardized_name = artists.standardize(tpe1)
        if standardized_name:
            if (standardized_name != tpe1):
                inp = input(f"You inputted artist name {tpe1}. Did you mean {standardized_name}?" \
                    f"Type 'no' to use {tpe1}, or type 'yes' to use {standardized_name}.")
                while (True):
                    if (inp == "no"):
                        print(f"Continuing, using artist name {tpe1}")
                        new_artists.add(tpe1)
                        break
                    elif (inp == "yes"):
                        print(f"Continuing, using artist name {standardized_name}")
                        break
                    else:
                        inp = input(f"Could not read input. Type only either 'yes' or 'no'")

        else:
            new_artists.add(tpe1)
        
    to_print = list(new_artists)
    if rewrite:
        to_print.extend(artists.all())
    to_print.sort(key=artists.sort_key)

    output = None
    if rewrite:
        output = codecs.open(artists._WHITELIST_FILE, "w", "utf-8")
    for tpe1 in to_print:
        if output:
            output.write(tpe1)
            output.write("\n")
        else:
            cprint(tpe1)
        yield

    if rewrite:
        cprint('Artist whitelist updated', type='success')
    else:
        cprint('Found %d new artists' % len(to_print), type='success')


def main():
    for _ in main_generator(rewrite="--rewrite" in sys.argv):
        pass


if __name__ == "__main__":
    main()
