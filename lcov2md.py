#!/usr/bin/env python

# This Python file uses the following encoding: utf-8
import datetime
import traceback
import re
import os
import sys
from optparse import OptionParser, SUPPRESS_HELP, Option, OptionGroup
import json
import subprocess
from collections import OrderedDict
import array


repo_root = '/local/ichebykin/ichebykin.l/work/sorrento/i-chebykin.coverage/sorrento/'
remove_prefix = repo_root


class SortedDict(OrderedDict):

    def __init__(self, **kwargs):
        super(SortedDict, self).__init__()

        items = kwargs.items()
        sorted_list = sorted(items)
        for key, value in sorted_list:
            if isinstance(value, dict):
                self[key] = SortedDict(**value)
            else:
                self[key] = value


def sprintf(format, *values):
    if isinstance(format, str) and (len(format) > 0 or len(values) == 0):
        return format % values


def printf(format, *values):
    if isinstance(format, str) and (len(format) > 0 or len(values) == 0):
        print(format % values)


def printf_v(format, *values):
    global opt
    if opt.verbose and isinstance(format, str) and (len(format) > 0 or len(values) == 0):
        print(format % values)


def printf_vv(format, *values):
    global opt
    if opt.verbose_debug and isinstance(format, str) and (len(format) > 0 or len(values) == 0):
        print(format % values)


def print_header():
    printf("%s | %s | %s | %s | %s |", "Filename".ljust(40),
           "Lines<br/>Rate".rjust(len("Functions")),
           "Lines<br/>Num".rjust(len("Functions")),
           "Functions<br/>Rate".rjust(len("Functions")),
           "Functions<br/>Num".rjust(len("Functions")))
    printf("%s-|-%s-|-%s-|-%s-|-%s-|", "-".ljust(40, '-'),
           "-".rjust(len("Functions"), '-'),
           "-".rjust(len("Functions"), '-'),
           "-".rjust(len("Functions"), '-'),
           "-".rjust(len("Functions"), '-'))


def print_total_header():
    printf("%s | %s | %s | %s |",
           "Lines<br/>Rate".rjust(len("Functions")),
           "Lines<br/>Num".rjust(len("Functions")),
           "Functions<br/>Rate".rjust(len("Functions")),
           "Functions<br/>Num".rjust(len("Functions")))
    printf("-%s-|-%s-|-%s-|-%s-|",
           "-".rjust(len("Functions"), '-'),
           "-".rjust(len("Functions"), '-'),
           "-".rjust(len("Functions"), '-'),
           "-".rjust(len("Functions"), '-'))


def main(argv):
    if len(argv) > 1:
        input_stream = open(argv[1])
    else:
        input_stream = sys.stdin

    reDir = re.compile("\[([^\]\]]+)\]")
    dirs = {}
    dir = None

    reFile = re.compile("(\S.*\S)\s*\|\s*(\S+)\s+(\d+)\s*\|\s*(\S+)\s+(\d+)\s*\|\s*(\S+)\s+(\d+)")
    files = []
    file = None

    reTotal = re.compile("\s*(tottal|Total|TOTAL):\s*\|\s*(\S+)\s+(\d+)\s*\|\s*(\S+)\s+(\d+)\s*\|\s*(\S+)\s+(\d+)")
    total = {}

    for line in input_stream:
        line = re.sub("\n", "", line)
        line = re.sub(remove_prefix, '', line)
        #print(line)

        matchDir = reDir.match(line)
        if matchDir:
            if dir:
                dirs[dir] = list(files)
            dir = matchDir.group(1)
            files = []
            continue

        matchFile = reFile.match(line)
        if matchFile:
            files.append({
                'file': matchFile.group(1),
                'l-rate': matchFile.group(2),
                'l-num': matchFile.group(3),
                'f-rate': matchFile.group(4),
                'f-num': matchFile.group(5),
            })
            continue

        matchTotal = reTotal.match(line)
        if matchTotal:
            total = {
                'file': matchTotal.group(1),
                'l-rate': matchTotal.group(2),
                'l-num': matchTotal.group(3),
                'f-rate': matchTotal.group(4),
                'f-num': matchTotal.group(5),
            }
            continue

    dirs_sorted = SortedDict(**dirs)

    printf("## Date: %s", datetime.date.today())
    print("")

    if total:
        printf("## Total")
        print_total_header()
        printf("%s | %s | %s | %s |",
               total['l-rate'].ljust(len("Functions")),
               total['l-num'].rjust(len("Functions")),
               total['f-rate'].rjust(len("Functions")),
               total['f-num'].rjust(len("Functions")))
        print("")

    try:
        cwd = os.getcwd()
        os.chdir(repo_root)
        proc = subprocess.Popen("git show --summary", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        git_show = proc.communicate()[0].split("\n")
        os.chdir(cwd)
        print("## Git summary")
        print("#### `git show --summary`")
        for line in git_show:
            print('    ' + line)
        print("")
    except:
        pass
    finally:
        pass

    printf("## HTML version")
    printf("[http://compiler-dev1:8000/p4c-sorrento-coverage/index.html](http://compiler-dev1:8000/p4c-sorrento-coverage/index.html)")
    printf("")

    printf("## Directories")
    for dir in dirs_sorted:
        # https://github.com/pensando/sorrento/wiki/Sorrento-code-coverage#p4cextensionscapriprogram_processing
        printf(" - [%s](https://github.com/pensando/sorrento/wiki/Sorrento-code-coverage#%s)",
               dir,
               re.sub('/', '', dir))
    print("")

    printf("## Files")
    for dir in dirs_sorted:
        printf("### [%s](https://github.com/pensando/sorrento/tree/master/%s)", dir, dir)
        print_header()
        files = dirs_sorted[dir]
        for file in files:
            printf("%s | %s | %s | %s | %s |",
                   sprintf("[%s](https://github.com/pensando/sorrento/tree/master/%s/%s)", file['file'], dir, file['file']).ljust(40),
                   file['l-rate'].rjust(len("Functions")),
                   file['l-num'].rjust(len("Functions")),
                   file['f-rate'].rjust(len("Functions")),
                   file['f-num'].rjust(len("Functions")))
        print("")

    return 0


if __name__ == "__main__":
    main_res = main(sys.argv[:])
    sys.exit(main_res)
