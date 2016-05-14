#!/usr/bin/python3

import os
import sys
from time import strftime
from datetime import datetime

def main():
    # backup drive variables
    dev = '/dev/sdb2'
    backUpDir = '/mnt/navi'
    log_file = '/var/log/my_mount.log' # log directory path. crontab job should run every night at 8pm and 10pm
    date = datetime.now().date().strftime('%m-%d-%y')
    time = datetime.now().time().strftime('%H:%M')
    time1 = '19:50'
    time2 = '20:00'

    sys.stdout = open(log_file, 'a')

    if os.popen('grep {0} /proc/mounts'.format(dev)).read():
        print('*********************************************************\n\tDrive is mounted... [{0} {1}]\n##########################################################\n'.format(date,time))

        proc = os.popen("grep {0} /proc/mounts | awk '{ print $2 }'".format(dev)).read()
        print('\tDirectory: %s' % proc)

        proc = os.popen("ps -ef | grep 'encfs --extpass=backintime' | grep -v 'grep'").read()
        if proc == '':
            print('\tUnmounting drive...')
            os.system('sudo umount %s' % backUpDir)

            ISMOUNTED = os.popen("grep {0} /proc/mounts | awk '{ print $2 }'".format(dev)).read().replace('\n', '')
            if ISMOUNTED == '':
                print('\tUnmounting successful...\n\n')
            else:
                print('\t*** ERROR: unmount unsuccessful ***\n\n')
        else:
            print('\tbackup in progress... [{0} {1}]\n\n'.format(date,time))

    else :
        print('##########################################################\n\tMounting drive... [{0} {1}]\n##########################################################\n'.format(date,time))
        os.system('sudo mount ' + dev + ' ' + backUpDir)

        ISMOUNTED = os.popen("grep {0} /proc/mounts | awk '{ print $2 }'".format(dev)).read().replace('\n', '')

        print('\tDirectory: %s' % ISMOUNTED)
        if ISMOUNTED == backUpDir:
            print('\tDrive mounted correctly [{0} {1}]\n\n'.format(date,time))
        else:
            print('\tDrive failed to mount [{0} {1}]\n\n'.format(date,time))

    sys.exit()

if __name__ == "__main__":
    main()
