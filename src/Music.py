
class Artist(object):

    def __init__(self, id: int, name: str, picture: str, albums: list):
        self.id = id
        self.name = name
        self.picture = picture
        self.albums = albums
    
    def __str__(self) -> str:
        string = "Artist: " + self.name + ", picture: " + self.picture
        for album in self.albums: string += "\n" + str(album)
        return string.replace('\n', '\n\t')

class Album(object):

    def __init__(self, id: int, name: str, picture: str, genres: list, date: str, tracks: list):
        self.id = id
        self.name = name
        self.picture = picture
        self.genres = genres
        self.date = date
        self.tracks = tracks
    
    def __str__(self) -> str:
        string = "Album: " + self.name + ", picture: " + self.picture + ", genres: " + str(self.genres) + ", date: " + self.date
        for track in self.tracks: string += "\n" + str(track)
        return string.replace('\n', '\n\t')

class Track(object):

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __str__(self) -> str:
        return "Track: " + self.name