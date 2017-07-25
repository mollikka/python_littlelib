from time import time
from os.path import exists
from os import makedirs

from urllib.request import Request, urlopen
from urllib.error import URLError
from hashlib import md5

from config import CACHE_DIR, CACHE_LOG, EXTERNAL_EXPIRE_TIME
from utils_log import Logger

if not exists(CACHE_DIR):
    makedirs(CACHE_DIR)

log = Logger(CACHE_LOG)

def get_external(url, expire_time=EXTERNAL_EXPIRE_TIME):
    cached_file = load_from_cache_file(url, expire_time)
    if cached_file:
        return cached_file.read()
    else:
        try:
            http_request = urlopen(Request(url, headers={'User-Agent':'browser'}))
            response = http_request.read().decode("utf-8")
            log("loaded from http ({})".format(http_request.status),url)
            if http_request.status == 200:
                save_to_cache_file(url, response)
        except URLError:
            #try to use cache even if it's expired
            cached_file = load_from_cache_file(url, -1)
            if cached_file:
                return cached_file.read()
            else:
                return ''
        return response

class CacheInspector:

    def __init__(self):
        self._has_changed = {}
        self._values = {}

    def __call__(self, url):
        if not url in self._values:
            self.refresh(url)
        return self._values[url]

    def refresh(self, url):
        value = get_external(url)
        try:
            self._has_changed[url] = value != self._values[url]
        except KeyError:
            self._has_changed[url] = True
        self._values[url] = value

    def has_changed(self, url):
        self.refresh(url)
        return self._has_changed[url]

def save_to_cache_file(url, contents):
    filename = filename_from_url(url)

    with open(filename, "w") as out_file:

        now = int(time())
        out_file.write(str(now))
        out_file.write("\n")
        out_file.write(url)
        out_file.write("\n")
        out_file.write(contents)

def load_from_cache_file(url, expire_time):
    filename = filename_from_url(url)
    now = int(time())

    #if the cache file doesn't exists, reject
    if not exists(filename):
        log("cache doesn't exist",url)
        return None

    in_file = open(filename, "r")

    #try to read the timestamp, or reject
    timestamp_str = in_file.readline()
    try:
        timestamp = int(timestamp_str)
    except ValueError:
        log("cache was malformed",url)
        return None

    #read the url
    in_file.readline()

    #if the file is too old, reject
    if (expire_time != -1) and ((now - timestamp) > expire_time):
        log("cache file is too old", url)
        return None

    log ("loaded from cache (age {}/{})".format(
                                    now - timestamp, expire_time), url)
    return in_file

def filename_from_url(url):
    hashgen = md5()
    hashgen.update(url.encode())
    return CACHE_DIR + "/" + hashgen.hexdigest()

