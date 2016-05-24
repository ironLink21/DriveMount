#!/usr/bin/python3

import os, sys, time as pyTime
from time import strftime
from datetime import datetime

def main():

    # backup drive variables
    dev = '/dev/sdb2'
    backUpDir = '/mnt/navi'
    log_file = '/var/log/my_mount.log' # log directory path. crontab job should run every night at 8pm and 10pm
    wait_time = 1800 # this is in seconds
    date = datetime.now().date().strftime('%m-%d-%y')
    time = datetime.now().time().strftime('%H:%M')
    start = datetime.strptime('19:50','%H:%M').strftime('%H:%M')
    end = datetime.strptime('22:50','%H:%M').strftime('%H:%M')
    now_time = datetime.now().time().strftime('%H:%M')

    sys.stdout = open(log_file, 'a')

    if os.popen('grep {0} /proc/mounts'.format(dev)).read():
        print('*********************************************************\n\tDrive is mounted... [{0} {1}]\n##########################################################\n'.format(date,time))

        proc = os.popen("grep {0} /proc/mounts | awk {1}".format(dev, "'{ print $2 }'")).read()
        print('\tDirectory: %s' % proc)

        proc = os.popen("ps -ef | grep 'encfs --extpass=backintime' | grep -v 'grep'").read()
        if proc == '':
            print('\tUnmounting drive...')
            os.system('sudo umount %s' % backUpDir)

            ISMOUNTED = os.popen("grep {0} /proc/mounts | awk {1}".format(dev, "'{ print $2 }'")).read().replace('\n', '')
            if ISMOUNTED == '':
                print('\tUnmounting successful...\n\n')
                sys.exit()
            else:
                print('\t*** ERROR: unmount unsuccessful ***\n\n')
        else:
            print('\tbackup in progress... [{0} {1}]\n\tTrying again in 30min...\n\n'.format(date,time))
            # start a timeout to run this again after 30min
            pyTime.sleep(wait_time)
            main()

    else :
        if start <= now_time <= end:
            print('##########################################################\n\tMounting drive... [{0} {1}]\n##########################################################\n'.format(date,time))
            os.system('sudo mount ' + dev + ' ' + backUpDir)

            ISMOUNTED = os.popen("grep {0} /proc/mounts | awk {1}".format(dev, "'{ print $2 }'")).read().replace('\n', '')

            print('\tDirectory: %s' % ISMOUNTED)
            if ISMOUNTED == backUpDir:
                print('\tDrive mounted correctly [{0} {1}]\n\n'.format(date,time))
            else:
                print('\tDrive failed to mount [{0} {1}]\n\n'.format(date,time))

if __name__ == "__main__":
    main()
