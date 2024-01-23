#!/usr/bin/env python3

'''
Fixes up the owner and group IDs for the given files
'''

import os
import shutil
import sys
from typing import List, Optional

import configargparse

parser = configargparse.ArgParser(
    description=__doc__,
    formatter_class=configargparse.ArgumentDefaultsRawHelpFormatter,
)
parser.add(
    '--user-uid',
    env_var='USER_UID',
    type=int,
    help='File owner ID',
)
parser.add(
    '--user-gid',
    env_var='USER_GID',
    type=int,
    help='File group ID, defaults to the owner ID',
)
parser.add(
    'path',
    nargs='*',
    help='File or directory paths',
)


def fix_owner(uid: Optional[int], gid: Optional[int], paths: List[str]):
    '''
    Fixes up the owner and group IDs for the given files
    '''
    if not uid or uid < 0:
        print(f"WARNING: no user ID, not changing any file owner", file=sys.stderr)
        return 0
    elif not gid or gid < 0:
        gid = uid

    for path in paths:
        print(f"INFO: setting uid={uid} and gid={gid} in {path}", file=sys.stderr)
        for dirpath, _, filenames in os.walk(path):
            shutil.chown(dirpath, user=uid, group=gid)
            for filename in filenames:
                shutil.chown(os.path.join(dirpath, filename), user=uid, group=gid)


def main():
    args = parser.parse_args()
    fix_owner(args.user_uid, args.user_gid, args.path)


if __name__ == '__main__':
    main()
