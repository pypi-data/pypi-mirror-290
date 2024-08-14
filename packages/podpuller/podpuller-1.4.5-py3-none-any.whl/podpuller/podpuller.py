#!/usr/bin/env python

import feedparser

import argparse
import configparser
import logging
from os.path import expanduser
from subprocess import run
from termcolor import cprint

from .process import *
from . import ui
from . import __version__

# Configuration Filename
config_filename = "~/.config/podpuller/feeds.conf"
directories = {}

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

MAX_ATTEMPTS = 7

def update_configfile(conf):
    with open(expanduser(config_filename), "w") as configfile:
        conf.write(configfile)


def process_feed(feed_name, conf, be_quick):
    """Process Single Feed

    Args:
        feed_name (string): Name of feed to process
        conf (ConfigParser): We pass the config parser to update the file with RSS
         info and to read the defaults
    """
    feed = conf[feed_name]
    url = feed["URL"]

    keep = 0
    keep_str = feed.get("keep episodes")
    if keep_str.isnumeric():
        keep = int(keep_str)
    elif keep_str == 'all':
        keep = 1e20  # Practically infinity
    else: 
        logging.error(f'Feed {feed} keep episodes ({keep_str}) must be number or all.')

    start_date = parse_date(feed.get("start date"))

    rss = feedparser.parse(url)

    rtl = feed.getboolean("rtl")

    # Check for fetch / parse errors
    try:
        check_feederrors(rss)
    except Exception as e:
        logging.error("Erroneous feed URL: %s (%s)" % (url, type(e)))
        return

    cprint(f"  ===== {ui.rtlize(rss.feed.title, rtl)} ({feed.name}; keep {keep_str}) =====  ", "grey","on_yellow")

    # Serial podcasts need to be processed from last to first
    if feed.getboolean("serial"):
        rss.entries.reverse()

    #################################################
    # This is where the logic happens. Right now
    # single logic: always have the latest [keep] episodes
    #################################################
    dl_dir = directories["dl"]

    tobe_deleted = []
    if not be_quick:
        tobe_deleted = ui.mark_deletion(dl_dir + os.sep + feed.name)

    for tbd in tobe_deleted:
        delete_episode(feed.name, tbd, dl_dir)

    if start_date:
        pretty_date = start_date.strftime("%B %d, %Y")
        cprint(f"Starting {pretty_date}", "cyan")

    have = 0
    attempts = 0
    for episode in rss.entries:

        episode.title = ui.rtlize(episode.title, rtl)
        hash_episode(episode, rss)

        if generate_filename(episode) in tobe_deleted:
            markPlayed(episode)
            continue

        if have < keep:
            if not start_date or episode.pub_date >= start_date:
                if get_episode(feed.name, episode, dl_dir):
                    have += 1
                attempts += 1
        else:
            delete_episode(feed.name, generate_filename(episode), dl_dir)

        if attempts >= MAX_ATTEMPTS:
            logging.warning("Too many failed attempts. Aborting this feed.")
            return

    # Post-processing Put podcast in config file it was just a URL
    if not "name" in feed:
        feed["name"] = rss.feed["title"]
        logging.info("Updating name in config")

    update_configfile(conf)


def sync_external(singlefeed):

    rsync_dir = directories["rsync"]
    dl_dir = directories["dl"]

    # Single feed sync
    if singlefeed:   
        rsync_dir = os.path.join(rsync_dir, singlefeed)+os.path.sep
        dl_dir = os.path.join(dl_dir, singlefeed)+os.path.sep

    if os.path.exists(rsync_dir):
        if ui.yesno(f"Sync to player {rsync_dir}?"):
            run(["rsync", 
                "-vahxP", "--size-only", '--exclude=".*"', "--delete", expanduser(dl_dir), rsync_dir],
                capture_output=False,
            )
            logging.info("Done.")
    else:
        logging.info(f"Rsync destination {rsync_dir} not connected.")


def parse_dirs(config):
    s = config.default_section
    data_dir = config.get(s, "Data directory", fallback="=~/.local/share/podpuller")
    dl_dir = config.get(s, "Download directory", fallback="~/Downloads/podcasts/")
    rsync_dir = config.get(s, "MP3 Player directory", fallback="/Volumes/M500/podcasts/")

    global directories
    directories["data"] = os.path.expanduser(data_dir)
    directories["dl"] = os.path.expanduser(dl_dir)
    directories["rsync"] = os.path.expanduser(rsync_dir)


def main():

    # Command line arguments
    ps = argparse.ArgumentParser()
    ps.add_argument("singlefeed", nargs='?', help="Name of single feed to update")
    ps.add_argument('--version', action='version', version=f"PodPuller v{__version__}")
    args = ps.parse_args()

    # Read feeds from config file
    conf = configparser.ConfigParser()
    conf.read(expanduser(config_filename))

    # Parse file location directories
    parse_dirs(conf)

    # Init DB
    init_db(directories["data"])
    # logging.debug(list(Episode.select()))

    # Check for quick mode
    be_quick = False
    if conf.get(conf.default_section, "always quick", fallback=False) or ui.yesno(
        "Quick mode?"
    ):
        be_quick = True

    # If a feed ID is given, only process that feed
    if args.singlefeed:
        process_feed(args.singlefeed, conf, be_quick)
    else:
        # Process all feeds (except DEFAULT)
        for feed_name in conf:
            if feed_name != conf.default_section:
                process_feed(feed_name, conf, be_quick)

    logging.info("Done updating feeds.")

    # Try to sync to external drive (mp3 player)
    sync_external(args.singlefeed)


if __name__ == "__main__":
    main()
