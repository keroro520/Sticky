#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import queue
import time
import datetime

PATH = os.getenv('HOME') + '/.sticky_.txt'
time_stamp = time.strftime(str(datetime.datetime.now()))


def aftercare():
    with open(PATH, 'r+') as f:
        Q = queue.Queue(2000)
        for line in f:
            if Q.full():
                Q.get()
            Q.put(line)

        if Q.full():
            f.seek(0)
            f.truncate()
            f.write(''.join(list(Q.queue)))


def main():
    if not os.path.isfile(PATH):
        os.mknod(PATH)
    if not os.access(PATH, os.R_OK):
        print('Permission deny', file=sys.stderr)
        return

    with open(PATH, 'a+') as sticky:
        if sys.argv[1:]:

            if sys.argv[1] == '-clean':
                sticky.truncate()
                return
            if sys.argv[1] == '-v':
                print(open(PATH).read())
                return

            for filename in sys.argv[1:]:
                print('!', filename)
                try:
                    with open(filename) as f:
                        file_stamp = '  ### %s --------------------\n' % f.name
                        sticky.writelines(time_stamp)
                        sticky.writelines(file_stamp)
                        for line in f:
                            sticky.writelines(line)
                except FileNotFoundError:
                    print(filename, 'Not Found', file=sys.stderr)
                except PermissionError:
                    print(filename, 'Permission Denied', file=sys.stderr)
                except:
                    print(filename, 'Fail to Write')
        else:
            for i in sys.stdin:
                sticky.write(i)
        sticky.writelines('\n\n')

    aftercare()


if __name__ == '__main__':
    main()
