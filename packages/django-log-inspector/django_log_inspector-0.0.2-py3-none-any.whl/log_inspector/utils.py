import os
import re
from fnmatch import fnmatch
from itertools import islice
from os.path import isfile

from . import settings


def reverse_readlines(file, exclude=None):
    patterns = settings.LOG_INSPECTOR_PATTERNS
    reversed_patterns = [x[::-1] for x in patterns]

    file.seek(0, os.SEEK_END)
    position = file.tell()
    line = ""

    while position >= 0:
        file.seek(position)
        next_char = file.read(1)

        if next_char == "\n" and line:
            if any([line.endswith(p) for p in reversed_patterns]):
                if exclude and re.search(exclude, line[::-1]).group(0):
                    line = ""
                else:
                    yield line[::-1]
                    line = ""
        else:
            line += next_char

        position -= 1

    yield line[::-1]


def get_log_entries(filename):
    file_log = os.path.join(settings.LOG_INSPECTOR_FILES_DIR, filename)
    with open(file_log, encoding='utf8', errors='ignore') as file:
        log_entries = list(islice(reverse_readlines(file, exclude=settings.LOG_INSPECTOR_EXCLUDE_TEXT_PATTERN), 1000))

    return log_entries


def get_log_file_names(directory):
    filenames = []
    with os.scandir(directory) as entries:
        for entry in entries:
            matched = fnmatch(entry.name, settings.LOG_INSPECTOR_FILES_PATTERN)
            specified = entry.name in settings.LOG_INSPECTOR_FILES

            if isfile(entry) and (matched or specified):
                filenames.append(entry.name)

    return filenames
