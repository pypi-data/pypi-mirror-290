""" Functions for tergiversator """

import datetime
import os
import re
import shutil
import sqlite3
import subprocess
import sys

def check_for(prog):
    """ Make sure a program exists in our PATH """

    if shutil.which(prog) is None:
        print(f"{prog} not found")
        sys.exit(1)

def find_orphans(target, hostlist):
    """ Display any directories not included in hostlists, and allow deletion """

    folderlist = []
    for dirpath, dirnames, files in os.walk(target): # pylint: disable=unused-variable
        for folder in dirnames:
            folderlist.append(os.path.join(dirpath, folder))

    configured = []
    for host_entry in hostlist:
        configured.append(target + '/' + host_entry)
        for path_entry in hostlist[host_entry]:
            if isinstance(path_entry, str):
                configured.append(target + '/' + host_entry + path_entry)

    spurious = []
    for path_entry in folderlist:
        found = 0
        for entry in configured:
            if re.match(entry, path_entry):
                found = 1
        if found == 0:
            spurious.append(path_entry)

    # sort results in descending length order
    spurious.sort(key=len)
    spurious.sort()
    spurious.reverse()

    return spurious

def create_index(hostlist, keystring, backup_path, my_env):
    """ Take hostlist, keystring, backup path, and environment, and return file data """

    datepattern = r'([a-zA-Z]{3} [a-zA-Z]{3} [0-9 ]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4})'
    filedata = []
    for host in hostlist:
        for path in hostlist[host]:
            if not isinstance(path, str):
                continue
            try:
                for line in str(subprocess.run(\
                    (f"duplicity{keystring}list-current-files" \
                        + f" file://{backup_path}/{host}/{path}").split(" "),\
                        env=my_env, capture_output=True, check=True).stdout).split("\\n"):
                    split = re.match(datepattern, line)
                    if isinstance(split, re.Match):
                        datestring, filename = split.group(), \
                            line.replace(f"{split.group()} ", '')
                        dateval = datetime.datetime.strptime(datestring, \
                            "%a %b %d %H:%M:%S %Y").isoformat()
                        filedata.append((f"{host}:{path}", dateval, filename))
            except subprocess.CalledProcessError as error:
                print(f"Unable to index {host}:{path}: {error}")

    return filedata

def write_index(file_data, backup_path):
    """ Write file data to database """

    connection = sqlite3.connect(f"{backup_path}/index.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS files(host, datetime, path)")
    cursor.execute("DELETE FROM files;")
    cursor.executemany("INSERT INTO files VALUES(?, ?, ?)", file_data)
    connection.commit()
