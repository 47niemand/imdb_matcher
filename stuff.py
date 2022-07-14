# coding: utf-8
import imp
import importlib
import os
import re
from transliterate import translit, get_available_language_codes

VIDEO_FILE_EXT = [".mp4", ".avi", ".mkv",
                  ".mov", ".wmv", ".flv", ".mpg", ".mpeg"]

stop_list = ["mkv", "BDRip", "720p", "2160p", "UHD", "avi", "1080p", "webriP",
             "Tapochek", "torrents.ru", "x264", "Eng", "Ukr", "Rus", "web-dl",
             "DVDRip", "AC3", "DUAL", "Hurtom", "BluRay", "XviD", "UKR",
             "HELLYWOOD", "HQCLUB", "HDRip", "ViDEO", "scarabey", "ENG", "amzn",
             "AVC", "DUB", "HDCLUB", "RUS", "WEB", "1400MB",
             "flintfilms", "DivX", "WEB-DL", "h264", "ukr", "Director's cut",
             "ac3", "[", "]"]

delimiters = [".", ",", "_", "(", ")", "-", "[", "]", " "]
delimiters_regexp = '|'.join(map(re.escape, delimiters))


def get_files(path):
    """
    get all files in a directory, and return them as a list
    """
    return [os.path.join(path, f) for f in os.listdir(path)]


def is_video_file(file):
    """
    check if file is a video file
    """
    for ext in VIDEO_FILE_EXT:
        if file.endswith(ext):
            return True
    return False


def get_video_files(path):
    """
    get all video files in a directory
    """
    return [f for f in get_files(path) if is_video_file(f)]

def try_translit(text):
    """
    Try to translit and normalize text
    """
    try:
        title = ''.join(filter(str.isalnum , str(
            translit(text,  reversed=True).lower())))
    except:
        title = ''.join(filter(str.isalnum, str(text.lower())))
    return title


def normalize_name(name):
    """
    Normalize name
    """    
    name = os.path.basename(name).lower()
    # cut off name after first stop word
    for stop_word in stop_list:
        if stop_word.lower() in name:
            name = name[:name.find(stop_word.lower())]

    # extract each word from name by delimiters
    words = re.split(delimiters_regexp, name)
    # remove empty words
    words = [word for word in words if word != ""]

    # concatenate words
    name = ""
    for word in words:
        name += try_translit(word)

    return name.strip()