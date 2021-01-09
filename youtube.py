from video import VideoEpisode
import utils

import pafy
from pytube import YouTube

import sys
import os
import json
import uuid
import pytz
import argparse
from podgen import Podcast, Episode, Media, Person, Category, htmlencode

from datetime import timedelta, datetime




# Download Progress Callback
def get_terminal_size():
    """Return the terminal size in rows and columns."""
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows), int(columns)


def display_progress_bar(bytes_received, filesize, ch='█', scale=0.55):
    """Display a simple, pretty progress bar.
    Example:
    ~~~~~~~~
    PSY - GANGNAM STYLE(강남스타일) MV.mp4
    ↳ |███████████████████████████████████████| 100.0%
    :param int bytes_received:
        The delta between the total file size (bytes) and bytes already
        written to disk.
    :param int filesize:
        File size of the media stream in bytes.
    :param ch str:
        Character to use for presenting progress segment.
    :param float scale:
        Scale multipler to reduce progress bar size.
    """
    _, columns = get_terminal_size()
    max_width = int(columns * scale)

    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    bar = ch * filled + ' ' * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)
    text = ' ↳ |{bar}| {percent}%\r'.format(bar=bar, percent=percent)
    sys.stdout.write(text)
    sys.stdout.flush()


def on_progress(chunk, file_handle, bytes_remaining):
    """On download progress callback function.
    :param object stream:
        An instance of :class:`Stream <Stream>` being downloaded.
    :param file_handle:
        The file handle where the media is being written to.
    :type file_handle:
        :py:class:`io.BufferedWriter`
    :param int bytes_remaining:
        How many bytes have been downloaded.
    """
    global filesize
    bytes_received = filesize - bytes_remaining
    display_progress_bar(bytes_received, filesize)

def pyTube_download(url):
    # url = 'https://www.youtube.com/watch?v=UIoruUFrVqs'
    video = YouTube(url)
    video.register_on_progress_callback(on_progress)

    try:
        stream = video.streams.filter(type='audio', mime_type='audio/mp4').order_by('abr').desc().first()      
        globals()['filesize'] = stream.filesize
        filename = stream.title

        print('\n{fn} | {fs} bytes'.format(
            fn=stream.title,
            fs=stream.filesize
        ))

        # stream.download()
        stream.download(output_path='/Users/obarreto/PERSONAL-OLIVER/dev/python/youtubeToAudioFile/videos/', filename=filename, filename_prefix='downloaded_with_pytube_', skip_existing= True,)
        sys.stdout.write('\n')

    except KeyboardInterrupt:
        sys.exit()
        
    #list = video.streams.filter(only_audio=True).order_by('abr').desc().first().download()
    #list = video.streams.filter(type='audio', mime_type='audio/mp4').order_by('abr').desc().first().download()
    #print(list)


def create_rss(type, download):
    """Create an example podcast and print it or save it to a file."""
    
    # Create the Podcast
    p = Podcast()
    p.name          = "Oliver's Personal Podcast"
    p.description   = "I publish interesting things i like to listen to!!!"
    p.website       = "http://oliverbarreto.com/"
    p.explicit      = False
    p.image         = "http://oliverbarreto.com/images/site-logo.png"

    p.copyright = "2020 OB Radio"
    p.language  = "es-ES"
    p.feed_url  = "https://example.com/feeds/podcast.rss"  # URL of this feed
    p.category  = Category("News")
    # p.category = Category('Technology', 'Podcasting')
    # p.xslt      = "https://example.com/feed/stylesheet.xsl"  # URL of XSLT stylesheet

    p.authors   = [Person("Youtube Author", " ")]
    # p.authors.append(Person("Lars Kiesow", "lkiesow@uos.de"))
    p.owner     = p.authors[0]

    
    # Initialize the feed
    # p.copyright = 'cc-by'
    # p.complete = False
    # p.new_feed_url = 'http://example.com/new-feed.rss'
    # p.owner = Person('John Doe', 'john@example.com')
    # p.xslt = "http://example.com/stylesheet.xsl"

    # e1 = p.add_episode()
    # e1.id = 'http://lernfunk.de/_MEDIAID_123#1'
    # e1.title = 'First Element'
    # e1.summary = htmlencode('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Tamen
    #         aberramus a proposito, et, ne longius, prorsus, inquam, Piso, si ista
    #         mala sunt, placet. Aut etiam, ut vestitum, sic sententiam habeas aliam
    #         domesticam, aliam forensem, ut in fronte ostentatio sit, intus veritas
    #         occultetur? Cum id fugiunt, re eadem defendunt, quae Peripatetici,
    #         verba <3.''')
    # e1.link = 'http://example.com'
    # e1.authors = [Person('Lars Kiesow', 'lkiesow@uos.de')]
    # e1.publication_date = datetime.datetime(2014, 5, 17, 13, 37, 10, tzinfo=pytz.utc)
    # # e1.media = Media("http://example.com/episodes/loremipsum.mp3", 454599964,
    # #                  duration=
    # #                  datetime.timedelta(hours=1, minutes=32, seconds=19))
    # e1.media = Media("http://example.com/episodes/loremipsum.mp3", 454599964)

    # Add some episodes
    p.episodes += [
       Episode(title = download.title, 
            subtitle = download.subtitle,
            # id=str(uuid.uuid4()),
            position = 0,
            media = Media(download.media_url, size=download.media_size, duration=timedelta(seconds=download.media_duration)),
            image = download.image_url,
            summary = "")
    # ,
    #    Episode(title="Episode 2?",
    #         subtitle="this is a cool episode",
    #         position=1,
    #         image="http://oliverbarreto.com/images/site-logo.png",
    #         media=Media("http://example.org/ep2.mp3", size=15363464, duration=timedelta(hours=1, minutes=1, seconds=1)),
    #         summary="The man behind Requests made something useful "
    #                    "for us command-line nerds.")
    ]

    # Should we just print out, or write to file?
    if type == 'print':
        # Print
        print_enc(p.rss_str())
    elif type== 'feed.xml':
        # Write to file
        p.rss_file(type, minimize=False)
        print("\n")
        print("feed.xml created !!!")

    

def pafy_download(url):
    if not url:
        url = "https://www.youtube.com/watch?v=-z4NS2zdrZc" # Here is to the Crazy Ones
    
    pafy.set_api_key("AIzaSyD5Q22HSOEJKYaNkObyb_38o_gLx24qu5Y")
    video = pafy.new(url)
    
    # print(f"videoid: {video.videoid}")

    # print(f"title: {video.title}")
    # print(f"description: {video.description}")
    # print(f"thumb: {video.thumb}")
    
    # print(f"duration: {video.duration}")
    # print(f"length: {video.length}")
    
    # print(f"author: {video.author}")
    # print(f"published: {video.published}")

    # print(f"rating: {video.rating}")
    # print(f"view count: {video.viewcount}")
    # print(f"likes: {video.likes}")
    # print(f"dislikes: {video.dislikes}")
    # print(f"keywords: {video.keywords}")

    download = VideoEpisode(title  = video.title, 
        description         = video.description,
        subtitle            = video.description, 
        video_id            = video.videoid, 
        author              = video.author, 
        image_url           = video.thumb, 
        published           = video.published,
        keywords           = video.keywords,
        media_size          = globals()['filesize'], 
        media_duration      = video.length, 
        position            = 0, 
        media_url           = "http://oliver.barreto.com/media/dummy.mp3"        
    )

    print(download)

    create_rss(type="feed.xml", download= download)





def download(url):
    # Define the search
    # YouTube('https://youtube.com/watch?v=2lAe1cqCOXo').streams.first().download()
    print("Download Started!")
    pyTube_download(url = url)
    pafy_download(url = url)
    print("Download Complete!")



def main():
    """Command line application to download youtube videos."""
    parser = argparse.ArgumentParser(description='This is a simple program to download youtube videos and convert them to audio podcasts')
    parser.add_argument('url', help='use the YouTube /watch url to convert to audio like "url=https://www.youtube.com/watch?v=URL"')
    args = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)
    
    if args.url:
        download(url=args.url)
        

if __name__ == '__main__':
    main()
    # create_rss()    #Oliver
    # create_rss(type="feed.xml")
    