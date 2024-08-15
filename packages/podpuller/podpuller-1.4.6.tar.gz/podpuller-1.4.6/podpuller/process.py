import logging
import os
import re
import shutil
import time
from datetime import datetime as dt
from os.path import expanduser

import eyed3
import feedparser
import requests
from feedparser.util import FeedParserDict
from termcolor import cprint
from tqdm import tqdm

from . import ui
from . import __version__
from .db import *

TEMPDIR = "/tmp/podpuller"


def hash_episode(episode, rss):
    episode.hash = episode_hash(episode)
    episode.pub_date = dt.fromtimestamp(time.mktime(episode.published_parsed))
    episode.podcast = rss.feed.title
    episode.publisher = rss.feed.author
    if hasattr(episode, 'image'):
        episode.imagelink = episode.image.href
    else:
        episode.imagelink = rss.feed.image.href



def get_episode(show, episode, dl_dir):

    dl_loc = expanduser(dl_dir) + os.sep + show + os.sep + generate_filename(episode)

    # Do we have this file?
    if os.path.exists(dl_loc):
        cprint(f"Already have: {episode.title}", "cyan")
        return 1
    else:
        # We not have this file
        e = seen(episode)

        # We might have played and deleted it in the past, don't download again
        if e and e.played:
            cprint(f"Already listened: {episode.title}", "magenta")
            return 0

    # If we are here, we want another episode, we don't have this one, and haven't played
    if download_episode(episode, dl_loc):
        markDownloaded(episode)
        return 1

    return -1


def download_episode(episode, dl_loc):
    """Performs downloading of specified file. Returns success boolean"""

    # Find and download first MPEG audio enclosure
    download_loc = download_enclosure(episode)
    if not download_loc:
        return False

    if download_loc == "dontwant":
        # Just mark as played but don't count
        cprint(f"Marked listened: {episode.title}", "magenta")
        markDownloaded(episode)
        return False

    # Updat ID3 tags
    tag_mp3file(download_loc, episode)

    # Move downloaded file to its final destination
    logging.debug(f"Moving {download_loc} to {dl_loc}")

    # Create show directory if necessary and move
    if not os.path.exists(os.path.dirname(dl_loc)):
        os.makedirs(os.path.dirname(dl_loc))
    shutil.move(download_loc, dl_loc)

    return True

def tag_mp3file(filepath, episode):

    f = eyed3.load(filepath)

    # Some files do not support IDv3 tags
    if not f:
        return

    # Deal with non-existinng tags
    if not f.tag:
        f.initTag()
        
    t = f.tag

    # Adjust version
    if t.version != eyed3.id3.ID3_V2_4:
        t.version = eyed3.id3.ID3_V2_4

    if not t.title:
        t.title = episode.title
    if not t.artist:
        t.artist = episode.publisher
    if not t.album: 
        t.album = episode.podcast

    # Add album art
    type = eyed3.id3.frames.ImageFrame.FRONT_COVER
    try:
        r = requests.get(episode.imagelink, timeout=10)
        t.images.set(type, r.content, r.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        cprint(f"WARNING: Could not complete episode HTTP request: {e}", "yellow")


    # Save ID3 tag
    try:
        t.save()
    except Exception as e:
        msg = ': ' + e.message if hasattr(e, 'message') else ''
        logging.warn(f"Couldn't save ID3 Tag {msg}")


def download_enclosure(episode):
    """Downloads URL to file, returns file name of download (from URL or Content-Disposition)"""

    # Temp DL destination
    downloadto = TEMPDIR + os.sep + episode.hash
    if not os.path.exists(os.path.dirname(downloadto)):
        os.makedirs(os.path.dirname(downloadto))

    # Get link from first supported enclosure
    audio_types = ['audio/mpeg', 'audio/x-m4a']
    first_mp3 = list(filter(lambda x: x["type"] in audio_types, episode.enclosures))[0]
    url = first_mp3.href
    headers = {
        'User-Agent': f'PodPuller v{__version__}'
    }

    try:
        cprint(f"Downloading {episode.title}", "yellow")
        r = requests.get(url, headers=headers, stream=True, timeout=15)

        if not r.ok:
            raise requests.exceptions.RequestException(f"Status Code {r.status_code}")

        # Download with progress bar in 2k chunks
        with open(downloadto, "wb") as f:
            total_length = int(r.headers["content-length"])
            with tqdm(total=total_length, unit="B", unit_scale=True, ncols=90) as pbar:
                for chunk in r.iter_content(2048):
                    f.write(chunk)
                    if chunk:
                        pbar.update(len(chunk))

    except KeyboardInterrupt:
        if ui.interrupt_dl():
            # Mark as played
            return "dontwant"
        else:
            return None

    except requests.exceptions.RequestException as e:
        cprint(f"ERROR: Could not complete episode HTTP request: {e}", "red")
        return None

    # TODO: Add MP3 metadata if it doesn't exist

    return downloadto


def generate_filename(episode):
    """Generates file name for this enclosure based on episode title."""
    entry_title = sanitize(episode.title)
    return f"{entry_title}.mp3"

BADFNCHARS = re.compile(r"[^\w]+")

def sanitize(str):
    return re.sub(BADFNCHARS, "_", str).strip("_")


def episode_location(dl_dir, show, filename):
    return expanduser(dl_dir) + os.sep + show + os.sep + filename


def delete_episode(show, filename, dl_dir):

    episode_loc = episode_location(dl_dir, show, filename)

    # Remove episode
    if os.path.exists(episode_loc):
        cprint(f"Removing: {filename}", "red")
        os.remove(episode_loc)
        return True

    return False


def parse_date(date_str):
    if not date_str:
        return None
    elif date_str == "now":
        return dt.now()
    else:
        try:
            d = dt.strptime(date_str, "%Y-%m-%d")
        except Exception:
            msg = "Date should be in YYYY-MM-DD format"
            raise AttributeError(msg)
        return d


def check_feederrors(rss):
    """Checks if the parsed RSS is actually a valid podcast feed"""

    # Not all bozo errors cause total failure
    if rss.bozo and isinstance(
        rss.bozo_exception,
        (
            type(FeedParserDict.NonXMLContentType),
            type(feedparser.CharacterEncodingOverride),
        ),
    ):
        raise rss.bozo_exception

    # When parsing a website or error message, title is missing.
    if "title" not in rss.feed:
        raise Exception("Not RSS Feed")
