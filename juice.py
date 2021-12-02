######################################################################################################
#
#	Lyricinator
#
# 	goal: generate full mp3s and lyrics for a set list of songs from youtube and genius
#
#	loop through tracklist.txt
# 	search each title on youtube (Juice WRLD - Z)
# 	grab link for each song and put them in a youtube_tracklist.txt
# 	youtube>mp3 for each link
# 	output to /songs/mp3s/(eg. Dababy - Y.mp3)
# 	repeat for genius
# 	output to /songs/lyrics/(eg. Dababy - Y.txt)
#
######################################################################################################
from youtubesearchpython import VideosSearch
import os
import youtube_dl
import json

file = open("input.txt", "r")

totalTracks = -1
currentTrack = 0

for line in file:
    if line != "\n":
        totalTracks += 1
file.close()

file = open("input.txt", "r")

with file as f:
  for line in f:
    trackName = line.strip()
    searchQuery = 'Juice WRLD ' + trackName
    videosSearch = VideosSearch(searchQuery, limit = 1)
    trackData = "/home/dylan/Desktop/python/songs/data/" + trackName + ".json"
    with open(trackData, "w") as outFile:
        json.dump(videosSearch.result(), outFile)
        outFile.close()
    #TODO: change the artist to be the file name
    innerFile = open(trackData, "r")
    data = json.load(innerFile)
    msg_deliver = 'Loading track ('
    msg_divider = '/'
    msg_end = '): '
    print (msg_deliver + str(currentTrack) + msg_divider + str(totalTracks) + msg_end  + trackName)
    url = data['result'][0]['link']
    print ("Downloading video (Juice WRLD - " + trackName  + "): " + url)

    currentTrack += 1

    ydl_opts = {
	'format': 'bestaudio/best',
	'postprocessors': [{
	  'key': 'FFmpegExtractAudio',
	  'preferredcodec': 'mp3',
	  'preferredquality': '48',
	}],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ytdl:
       info_dict = ytdl.extract_info(url, download=False)
       video_title = info_dict.get('title', None)
       path = f'/home/dylan/Desktop/python/songs/mp3s/Juice WRLD - {trackName}.mp3'
       ydl_opts.update({'outtmpl':path})
 
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    innerFile.close()
    if 'str' in line:
       break;
file.close()
