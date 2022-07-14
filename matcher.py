# coding: utf-8
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

from pathlib import Path
import sys
import os
from transliterate import translit, get_available_language_codes
from tqdm import tqdm
from Levenshtein import editops, apply_edit, opcodes, distance, hamming, inverse, jaro, jaro_winkler, matching_blocks, median, median_improve, quickmedian, ratio, seqratio, subtract_edit, setmedian, setratio
from string import digits, ascii_letters
from imdbdb import imdb_all_search, imdb_title, imdb_title_ru, session, Base, t_akas, t_crew, t_episodes, Person, Rating, Title
from stuff import get_video_files, normalize_name, try_translit


# constants
REGIONS = ['US']  # REGIONS = ['US', 'RU', 'FR']
MIN_YEAR = 1900


def valid_filename(title_name, premiered):
    """
    Format title
    """
    valid_chars = "-_.() %s%s" % (ascii_letters, digits)
    name = str(translit(title_name, 'ru', reversed=True))
    name = ''.join(c for c in name if c in valid_chars)
    name = str.replace(name, ' - ', '-')
    name = str.replace(name, ' ', '_')
    return name + ".(" + str(premiered) + ")"


def read_info(file_name):
    """
    Read info from file
    """
    file_info = {}
    if Path(file_name).exists():
        with open(file_name, 'r', encoding='utf-8') as myfile_meta:
            meta_data = myfile_meta.read()
        y = str(meta_data).split("\n")
        topic = None
        category = None
        index = 0
        for s in y:
            if s[-1:] == ":":
                new_topic = s[0:len(s)-1]
                if new_topic == topic:
                    index = index + 1
                else:
                    index = 0
                topic = new_topic
            else:
                key = s[2:s.find(":")]
                value = (s[1 + s.find(":"):]).strip()
                if len(key) > 0:
                    if topic not in file_info:
                        file_info[topic] = {}
                    if index not in file_info[topic]:
                        file_info[topic][index] = {}
                    file_info[topic][index][key] = value
    else:
        logging.debug("File %s not found", file_name)
    return file_info


def meta_info(file_name):
    """
    Read info from file
    """
    file_info = read_info(file_name)
    tags = ""

    if 'Video stream' in file_info:
        width = int(file_info['Video stream'][0]['Image width'].split(' ')[0])
        compression = file_info['Video stream'][0]['Compression'].split('/')
    else:
        width = 0
        compression = None

    if width > 2000:
        tags = tags + '[UHD]'
    elif width > 1800:
        tags = tags + '[1080p]'
    elif width > 1100:
        tags = tags + '[720p]'

    # print(compression)
    try:
        if compression[2] == 'HEVC':
            tags = tags + '[HEVC]'
    except:
        pass

    if 'Audio stream' in file_info:
        la = set([])
        for a in file_info['Audio stream']:

            if 'Language' in file_info['Audio stream'][a]:
                l = str(file_info['Audio stream'][a]['Language'][0:3].upper())
                if len(l) > 0:
                    la.add(l)
        if len(la) > 0:
            for l in la:
                tags = tags + '[' + l + ']'
    return tags


def _run(path):
    files = get_video_files(path)
    name_src = {}

    for i in files:
        # (name, match ratio, title_name, premiered, title_id)
        name_src[i] = (normalize_name(i), None, None, None, None)

    logging.info("Found %d files", len(name_src))
    logging.info("Opening database")
    q = imdb_all_search.filter(t_akas.columns['region'].in_(REGIONS)).filter(
        Title.premiered >= MIN_YEAR).filter(Title.is_adult == 0)
    total_rows = q.count()
    logging.info("Found %d titles", total_rows)

    for row in tqdm(q, total=total_rows, unit=' rows'):
        title_id = row[0]
        premiered = row[3]
        title_name = row[-1:][0]

        title = try_translit(title_name) + str(premiered)
        
        for key in name_src:
            file_title = str(name_src[key][0])
            e = (file_title, title)
            j = jaro(e[1], e[0])
            r = ratio(e[1], e[0])
            s = (j + r) / 2
            best = name_src[key][1] if name_src[key][1] else 0
            if s > best:
                name_src[key] = (file_title, s, title_name,
                                 premiered, title_id)
                logging.debug(str(name_src[key]))
    return name_src


def main():
    """
    Main function
    """
    try:
        name_src = _run(sys.argv[1] if len(sys.argv)
                        > 1 else '/mnt/nas/Movies')
    except Exception as e:
        logging.error(e)
        return

    print("REM ==========================================")
    print('CHCP 65001')
    # output name_src to console
    for key in name_src:
        print("REM #", name_src[key])
        # file ext
        ext = Path(key).suffix
        tag = meta_info(key + ".info")
        name = valid_filename(name_src[key][2], name_src[key][3])
        new_name = name + tag + ext
        old_name = os.path.basename(key)
        print("REN \"" + old_name + "\" \"" + new_name + "\"")
        print()


if __name__ == "__main__":
    main()
