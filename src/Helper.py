import logging
import requests
import shutil
import re
from pathlib import Path
from mutagen.easyid3 import EasyID3

from src.Music import Artist, Album, Track
from src.APIClient import YoutubeClient, DeezerClient

class Searcher(object):

    def __init__(self):
        self.logger = logging.getLogger("Searcher")
        self.client = DeezerClient()

    def trackInfo(self, name: str) -> Artist:
        self.logger.warning("looking for track: '" + name + "' informations")
        artist, albumId, track = self.client.findTrack(name)
        self.logger.warning("info received, artist: " + artist.name + ", album's id: " + str(albumId) + ", track's id: " + str(track.id))
        album = self.client.allAlbumInformations(albumId)
        self.logger.warning("album infos received, name: " + album.name + ", id: " + str(album.id) + ", genres: " + str(album.genres) + ", date: " + album.date)
        album.tracks = [track]
        artist.albums = [album]
        return artist

    def albumInfo(self, name: str) -> Artist:
        self.logger.warning("looking for album: '" + name + "' informations")
        artist, albumId = self.client.findAlbum(name)
        self.logger.warning("info received, artist: " + artist.name + ", album's id: " + str(albumId))
        album = self.client.allAlbumInformations(albumId)
        artist.albums = [album]
        self.logger.warning("album infos received, name" + album.name + ", id: " + str(album.id) + ", genres: " + str(album.genres) + ", date: " + album.date)
        return artist

    def artistInfo(self, name: str) -> Artist:
        self.logger.warning("looking for artist: '" + name + "' informations")
        artist = self.client.findArtist(name)
        self.logger.warning("info received, artist: " + artist.name + ", id: " + str(artist.id) + ", picture: " + artist.picture)
        albumsId = self.client.allAlbumFromArtist(artist.id)
        self.logger.warning("album ids received: " + str(len(albumsId)))
        artist.albums = [self.client.allAlbumInformations(albumId) for albumId in albumsId]
        self.logger.warning("albums infos received")
        return artist

class Downloader(object):

    def __init__(self):
        self.logger = logging.getLogger("Downloader")
        self.client = YoutubeClient()

    def pictureDl(self, url: str, outPath: str) -> None:
        self.logger.warning("retrieve the picture of the artist at: " + url)
        response = requests.get(url, stream=True)
        with open(outPath, 'wb') as outFile: shutil.copyfileobj(response.raw, outFile)

    def trackDl(self, track: Track, artistName: str, albumName: str, albumGenres: list, albumDate: str, path: str = ".") -> None:
        urlVid = self.client.search(track.name + " " + artistName)
        outPath = path + '/' + re.sub(r'[^\w\-_\.]', '', track.name)
        self.client.download(urlVid, outPath)
        audio = EasyID3(outPath + ".mp3")
        audio['title'] = track.name
        audio['artist'] = artistName
        audio['album'] = albumName
        audio['genre'] = albumGenres[0]
        audio['date'] = albumDate
        audio.save()

    def albumDl(self, album: Album, artistName: str, path: str = ".") -> None:
        if not album: raise Exception("You should provide an album object to download !")
        folderPath = path + "/" + re.sub(r'[^\w\-_\.]', '', album.name)
        self.logger.warning("create the folder for: " + album.name)
        Path(folderPath).mkdir(parents=True, exist_ok=True)
        self.pictureDl(album.picture, folderPath + '/' + re.sub(r'[^\w\-_\.]', '', album.name + '.jpg') )
        for track in album.tracks: self.trackDl(track, artistName, album.name, album.genres, album.date, folderPath)

    def artistDl(self, artist: Artist, path: str = ".") -> None:
        if not artist: raise Exception("You should provide an artist object to download !")
        folderPath = path + "/" + re.sub(r'[^\w\-_\.]', '', artist.name)
        self.logger.warning("create the folder for: " + artist.name)
        Path(folderPath).mkdir(parents=True, exist_ok=True)
        self.pictureDl(artist.picture, folderPath + '/' + re.sub(r'[^\w\-_\.]', '', artist.name + '.jpg'))
        for album in artist.albums: self.albumDl(album, artist.name, folderPath)
