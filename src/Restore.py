import urllib.request
from bs4 import BeautifulSoup
from pytube import YouTube

import os
import json
import sys
import time

# BACKUP_FILE = 'videos.json'
BACKUP_FILE = input("Enter Backup file path: ")
OUTPUT_FOLDER = input("Enter Output Folder Name: ")

# mix it up, soup it up
def get_video_link(title):
    print('\nFetching "' + title + '"')
    query = urllib.parse.quote(title)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(attrs={'class': 'yt-uix-tile-link'})['href']


# progress bar
def get_progress(stream, chunk, file_handle, bytes_remaining):
    percent = float(round((1 - bytes_remaining / filesize), 2))
    progress = "\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(percent * 50), percent * 100)
    print(progress, end="")
        
global filesize
global filesizeMB

# read json
with open(BACKUP_FILE) as f:
    data = json.load(f)
    for i in data:

        # get the title - "my-video.mp"
        title = os.path.basename(i[0])
        title, ext = os.path.splitext(title)

        # get the dirname - "/video/html"
        dirname = os.path.join(OUTPUT_FOLDER, os.path.dirname(i[0]))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        
        yt = YouTube(get_video_link(title), on_progress_callback=get_progress)

        # get the video by resolution/quality
        video = yt.streams.filter(res=str(i[1])+'p').first()
         # if the specific quality is not available fallback to max quality
        if video is None:
          video = yt.streams.first()

        filesize = video.filesize
        filesizeMB = str(round(filesize / float(1 << 20), 2)) + 'MB'

        print('\nDownloading "' + str(title) + '" size: ' + filesizeMB)
        video.download(dirname)
