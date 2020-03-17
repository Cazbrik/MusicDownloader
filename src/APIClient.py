import requests
import logging
import json
import re
import youtube_dl

from src.Music import Artist, Album, Track

class DeezerClient(object):

    DEEZER_API = "https://api.deezer.com/"
    
    def __init__(self):
        self.logger = logging.getLogger("DeezerClient")

    # 'private' methods #

    def __request(self, url: str) -> dict:
        self.logger.warning("http get at: " + url)
        res = requests.get(url)
        if res.status_code != 200: raise Exception("Http request respond with code: " + str(res.status_code))
        self.logger.warning(str(res.status_code))
        return res.json()
    
    def __search(self, path: str, name: str) -> dict:
        url = self.DEEZER_API + "search/" + path + "?q=" + name
        self.logger.warning("search for: " + name + " in: " + path)
        data = self.__request(url)
        if len(data.keys()) == 0: raise Exception("Can not find corresponding result for :" + path + " and " + name)
        return data["data"][0]

    #  search methods #

    def findArtist(self, name: str) -> Artist:
        data = self.__search("artist", name)
        return Artist(data["id"], data["name"], data["picture"], None)

    def findAlbum(self, name: str) -> (Artist, int):
        data = self.__search("album", name)
        return Artist(data["artist"]["id"], data["artist"]["name"], data["artist"]["picture"], None), data["id"]

    def findTrack(self, name: str) -> (Artist, int, Track):
        data = self.__search("track", name)
        return Artist(data["artist"]["id"], data["artist"]["name"], data["artist"]["picture"], None), data["album"]["id"], Track(data["id"], data["title_short"])
    
    # More specifique research #

    def allAlbumFromArtist(self, artistId: int) -> list:
        url = self.DEEZER_API + "artist/" + str(artistId) + "/albums"
        data = self.__request(url)
        return [album["id"] for album in data["data"]]
    
    def allAlbumInformations(self, albumId: int) -> Album:
        url = self.DEEZER_API + "album/" + str(albumId)
        data = self.__request(url)
        album = Album(data["id"], data["title"], data["cover"], [genre["name"] for genre in data["genres"]["data"]], data["release_date"], None)
        album.tracks = [Track(track["id"], track["title_short"]) for track in data["tracks"]["data"]]
        return album

class YoutubeClient(object):

    YOUTUBE_SEARCH = "https://www.youtube.com/results?search_query="
    YOUTUBE_VIDEO = "https://www.youtube.com/watch?"
    YOUTUBE_REGEX = re.compile(r'/watch\?([^\"]+)', re.I | re.M | re.U)
    
    def __init__(self):
        self.logger = logging.getLogger("YoutubeClient")

    def search(self, name: str) -> str:
        self.logger.warning("Search on youtube for: " + name)
        res = requests.get(self.YOUTUBE_SEARCH + name).content.decode('utf-8')
        vids = self.YOUTUBE_REGEX.findall(res)
        self.logger.warning(str(len(vids)) + " video(s) found for: " + name)
        if not vids: raise Exception("No video found corresponding to: " + name)
        else: return vids[0]

    def download(self, url: str, outPath: str) -> None:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outPath + '.%(ext)s',
            'ignoreerrors': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        self.logger.warning("Download video: " + self.YOUTUBE_VIDEO + url)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl: ydl.download([self.YOUTUBE_VIDEO + url])