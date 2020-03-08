#!/usr/bin/python3

import argparse
import logging
import sys

from src.Helper import Searcher, Downloader

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=False)
    parser.add_argument("-a", "--artist", type=str, help="name of the artist", action="store")
    parser.add_argument("-c", "--collection", type=str, help="name of the album", action="store")
    parser.add_argument("-t", "--track", type=str, help="name of the track", action="store")
    parser.add_argument("-d", "--download", help="download the track(s) found", action="store_true", default=False)

    args = vars(parser.parse_args())
    logging.basicConfig(stream=sys.stdout, format="[DEBUG] %(message)s", level=logging.WARN if args["verbose"] else logging.FATAL)
    
    if not any(args.values()):
        parser.print_help()
        exit(0)
    
    client = Searcher()
    artist = Searcher().infos(args["track"], args["collection"], args["artist"])

    if args["download"]:
        dl = Downloader()
        dl.artistDl(artist, "music")
    else:
        print(artist)