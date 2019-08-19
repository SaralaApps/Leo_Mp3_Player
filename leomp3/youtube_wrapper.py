import youtube_dl
import os
import urllib
from bs4 import BeautifulSoup
import lxml
from lxml import etree
import pafy
import vlc
import time
import datetime


def yt_search(textToSearch):

    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    search_results = {}
    vid_list = soup.findAll(attrs={'class':'yt-uix-tile-link'})

    results_count = len(vid_list)
    if (results_count > 20):
        results_count = 20

    for i in range(results_count):
        vid = vid_list[i]
        link = 'https://www.youtube.com' + vid['href']
        song_name = yt_get_title(link)

        if song_name == "":
            continue

        search_results[song_name] = link

    return search_results


def yt_get_title(link):
    youtube = etree.HTML(urllib.request.urlopen(link).read()) #enter your youtube url here
    video_title = youtube.xpath("//span[@id='eow-title']/@title") #get xpath using firepath firefox addon
    video_title = ''.join(video_title)

    return video_title


# def check_status(state):
#     if state['status'] == 'downloading':
#


def yt_download(url, download_path):

    ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',}],
            # 'progress_hooks': [check_status],
        }

    os.chdir(download_path)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


def yt_stream(url):

    video = pafy.new(url)
    best = video.getbestaudio()
    playurl = best.url

    return playurl
