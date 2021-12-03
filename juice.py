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
import threading

thr = None
totalTracks = None
currentTrack = None

def count():
  file = open("input.txt", "r")
  totalTracks = 0
  currentTrack = 0

  for line in file:
    if line != "\n":
      totalTracks += 1
  file.close()

def download(url, song):
        track_data = 'songs/data/' + song + '.json'
        data_file = open(track_data, 'r')
        data = json.load(data_file)
        print ("Downloading video... (" + song  + "): " + url)
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
           print('Starting download for: ' + video_title)
           path = f'songs/mp3s/{song}.mp3'
           ydl_opts.update({'outtmpl':path})

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
           ydl.download([url])
           print('Finished download: ' + song + '.mp3')

def scan_input():
    file = open("input.txt", "r")
    print('Checking for song data...')
    with file as f:
      for line in f:
        track_name = line.strip()
        #TODO: allow the artists name to be change in the command prompt with 'python juice.py <source> <artist>'
        title_format = 'Juice WRLD' + ' - '
        title = title_format + track_name
        track_data = 'songs/data/' + title + '.json'
        path = Path(track_data)
        if path.is_file():
            data = json.load(open(track_data, 'r'))
            url = data['result'][0]['link']
            thr = threading.Thread(target=download, args=(url, title), kwargs={})
            thr.start()
        else:
            print("File doesn't exist, scraping data...")
            video_search = VideosSearch(title, limit = 1)
            with open(track_data, 'w') as data_file:
              json.dump(video_search.result(), data_file)
              data_file.close()
              print('Scrape complete. ' + track_data)
    file.close()

def main():
    print('Juicing up...')
    count()
    scan_input()
    print("We're done. Jam out.")

if __name__ == "__main__":
    main()
