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
from pathlib import Path

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
    track_name = line.strip()
    #TODO: allow the artists name to be change in the command prompt with 'python juice.py <source> <artist>'
    title_format = 'Juice WRLD' + ' - '
    title = title_format + track_name 
    track_data = 'songs/data/' + title + '.json'
    path = Path(track_data)
    if path.is_file():
        print('File already exists, skipping: ' + title)
    else:
        print("File doesn't exist, scraping data...")
        video_search = VideosSearch(title, limit = 1)
        with open(track_data, 'w') as data_file:
            json.dump(video_search.result(), data_file)
            data_file.close()
            print('Download complete... ' + track_data)
file.close()

file = open("input.txt", "r")

with file as f:
  for line in f:
    track_name = 'Juice WRLD' + ' - ' + line.strip()
    track_data = 'songs/data/' + track_name
    data_file = open(track_data, 'r')
    data = json.load(data_file)
    msg_deliver = 'Loading track ('
    msg_divider = '/'
    msg_end = '): '
    print (msg_deliver + str(currentTrack) + msg_divider + str(totalTracks) + msg_end  + track_name)
    url = data['result'][0]['link']
    print ("Downloading video (" + track_name  + "): " + url)

    currentTrack += 1

    ydl_opts = {
	'format': 'bestaudio/best',
	'postprocessors': [{
	  'key': 'FFmpegExtractAudio',
	  'preferredcodec': 'mp3',
	  'preferredquality': '192',
	}],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ytdl:
       info_dict = ytdl.extract_info(url, download=False)
       video_title = info_dict.get('title', None)
       print('Downloading... ' + video_title)
       path = f'songs/mp3s/{track_name}.mp3'
       ydl_opts.update({'outtmpl':path})

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    innerFile.close()

    if 'str' in line:
       break;
file.close()
