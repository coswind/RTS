'''
Created on Oct 31, 2012

@author: Yi
'''
from django.core.management.base import BaseCommand
from optparse import make_option
from music_importer.settings import LOG_ROOT
from importer.worker_daemon import WorkerDaemon
import os, sys

class Command(BaseCommand):

    def handle(self, *args, **options):
        if args and len(args) >= 2:
            daemon = None
            name = args[1]
            daemon_file = os.path.join(LOG_ROOT, '%s.pid' % name)
            daemon = WorkerDaemon(daemon_file, name)

            if daemon:
                if args[0] == 'start':
                    daemon.start()
                    return
                elif args[0] == 'stop':
                    daemon.stop()
                    return
                elif args[0] == 'restart':
                    daemon.restart()
                    return
                elif args[0] == 'status':
                    daemon.status()
                    return

        print _usage()

def _usage():
    return 'Usage options: [start|stop|restart|status] [normal|quick|vip]\n' + \
            '\tstart: Start worker daemons.\n' + \
            '\tstop: Stop worker daemons.\n' + \
            '\trestart: Restart worker daemons.\n' + \
            '\tstatus: Check the daemons status.\n'
