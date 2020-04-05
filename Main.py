#!/usr/bin/python3

import argparse
import logging
import sys

from src.Helper import Searcher, Downloader

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=False)
    parser.add_argument("-a", "--artist", nargs='+', type=str, help="name of the artist", action="store")
    parser.add_argument("-c", "--collection", nargs='+', type=str, help="name of the album", action="store")
    parser.add_argument("-t", "--track", nargs='+', type=str, help="name of the track", action="store")
    parser.add_argument("-d", "--download", help="download the track(s) found", action="store_true", default=False)

    args = vars(parser.parse_args())
    logging.basicConfig(stream=sys.stdout, format="[Info] %(message)s", level=logging.WARN if args["verbose"] else logging.FATAL)
    
    if not any(args.values()):
        parser.print_help()
        exit(0)
    
    client = Searcher()
    dl = Downloader()

    logger = logging.getLogger("MusicDownloader")

    if args["artist"]:
        for art in args["artist"]:
            try:
                artist = Searcher().artistInfo(art)
                if args["download"]: dl.artistDl(artist, "music")
                else: print(artist)
            except Exception as e:
                logger.fatal(str(e))

    if args["collection"]:
        for col in args["collection"]:
            try:
                artist = Searcher().albumInfo(col)
                if args["download"]: dl.artistDl(artist, "music")
                else: print(artist)
            except Exception as e:
                logger.fatal(str(e))
    
    if args["track"]:
        for tra in args["track"]:
            try:
                artist = Searcher().trackInfo(tra)
                if args["download"]: dl.artistDl(artist, "music")
                else: print(artist)
            except Exception as e:
                logger.fatal(str(e))