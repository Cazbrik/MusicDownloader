# MusicDownloader

## Introduction :

Program that find, download and add metadata to music file, to do this the program, will look after the metadata of the track, artist,  collection using the [Deezer API](https://developers.deezer.com/api) then it will make a research on Youtube and parse the document to recover the video link. After that the [youtube_dl module](https://pypi.org/project/youtube_dl/) is used to download the track and then the metadata are added to the file downloaded.

## How to use it :

first of all you have to clone the repo and make the file __Main.py__ an executable :

```bash
$ git clone https://github.com/Cazbrik/MusicDownloader.git
$ cd MusicDownloader
$ chmod +x Main.py
```
you can see all the available commands by doing :

```bash
$ ./Main.py -h
```

this program allows you to see all the metadata that you on a specifique trac, artist or collection by doing :

```bash
$ ./Main.py -t "Bad penny"
Artist: Rory Gallagher, picture: https://api.deezer.com/artist/10543/image
	Album: Top Priority (Remastered 2017), picture: https://api.deezer.com/album/58738892/image, genres: ['Rock', 'Blues'], date: 2018-03-16
		Track: Bad Penny
$ ./Main.py -c "Top priority"
Artist: Rory Gallagher, picture: https://api.deezer.com/artist/10543/image
	Album: Top Priority (Remastered 2017), picture: https://api.deezer.com/album/58738892/image, genres: ['Rock', 'Blues'], date: 2018-03-16
		Track: Follow Me
		Track: Philby
		Track: Wayward Child
		Track: Keychain
		Track: At The Depot
		Track: Bad Penny
		Track: Just Hit Town
		Track: Off The Handle
		Track: Public Enemy No. 1
		Track: Hell Cat
		Track: The Watcher
$ ./Main.py -a "Rory gallagher" # this will list all his albums !!
```
if the track found does not correspond to the one that you wanted you can add some more key word to help the youtube search :

```bash
$ ./Main.py -t "Shadow play"
Artist: Deep Sleep, picture: https://api.deezer.com/artist/476751/image
	Album: Calming Music to Relax the Mind and Body, picture: https://api.deezer.com/album/139100942/image, genres: ['Pop'], date: 2020-03-30
		Track: Shadow Play
$ ./Main.py -t "Shadow play Rory" # New key word to refine the search
Artist: Rory Gallagher, picture: https://api.deezer.com/artist/10543/image
	Album: Photo Finish (Remastered 2017), picture: https://api.deezer.com/album/58737412/image, genres: ['Rock', 'Blues'], date: 2018-03-16
		Track: Shadow Play
```

You can also pass a list of artist, collection or track:

```bash
$ ./Main.py -t "Shadow play Rory" "whole lotta love" "Eminence front"
Artist: Rory Gallagher, picture: https://api.deezer.com/artist/10543/image
	Album: Photo Finish (Remastered 2017), picture: https://api.deezer.com/album/58737412/image, genres: ['Rock', 'Blues'], date: 2018-03-16
		Track: Shadow Play
Artist: Led Zeppelin, picture: https://api.deezer.com/artist/848/image
	Album: Led Zeppelin II (Deluxe Edition; 2014 Remaster), picture: https://api.deezer.com/album/7824595/image, genres: ['Rock'], date: 1969-10-22
		Track: Whole Lotta Love
Artist: The Who, picture: https://api.deezer.com/artist/817/image
	Album: The Who- The Greatest Hits & More (International Version Edited), picture: https://api.deezer.com/album/481965/image, genres: ['Pop'], date: 2010-02-08
		Track: Eminence Front
 ```

Once you have found the track, collection or artist that you wanted you can add the __d__ option download all the tracks that were previously listed (the download file will be put in the music folder):

```bash
$ ./Main.py -t "Shadow play" -d
```




