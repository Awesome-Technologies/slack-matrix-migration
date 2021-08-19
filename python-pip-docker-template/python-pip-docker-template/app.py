#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
#       python-pip-docker-template/python-pip-docker-template/app.py
#       Copyright 2020 sebastian.rojo <sebastian.rojo@sapian.com.co>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#

__author__ = "Sebastian Rojo"
__copyright__ = "Copyright 2020, Sebastian Rojo, Sapian SAS"
__credits__ = []
__license__ = "GPLv2"
__version__ = "0.1.1"
__maintainer__ = "Sebastian Rojo"
__email__ = ["sebastian.rojo at sapian.com.co", "arpagon at gmail.com"]
__status__ = "Temaplate"

import logging
import os
import signal
import traceback
from random import randint
from time import sleep

from prometheus_client import CollectorRegistry, Gauge, pushadd_to_gateway

PROMETHEUS_PUSH_GW = os.environ.get('PROMETHEUS_PUSH_GW', "")
LOG_LEVEL = os.environ.get('LOG_LEVEL', "INFO").upper()

logging.basicConfig(level=LOG_LEVEL)
log = logging.getLogger('PYTHON-PIP-DOCKER-TEMPLATE')
registry = CollectorRegistry()

def terminateProcess(signalNumber, frame):
    log.error('(SIGTERM) terminating the process')
    if PROMETHEUS_PUSH_GW:
        pushadd_to_gateway(PROMETHEUS_PUSH_GW, job='python-pip-docker-template', registry=registry)
    sys.exit(1)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, terminateProcess)
    last_success = Gauge(
            'python_pip_docker_template_last_success_unixtime', 
            'Last time a batch job successfully finished', 
            registry=registry
    )
    duration = Gauge('python_pip_docker_template_duration_seconds', 'Duration of batch job', registry=registry)
    try:
        with duration.time():
            log.info('Starting... python-pip-docker-template')
            sleep_sec=randint(10,100)
            log.info("Sleeping... for {} sec".format(sleep_sec))
            sleep(sleep_sec)
    except SystemError as e:
        log.error(traceback.format_exc())
        log.error(e)
        exit(1)
    except Exception as e:
        log.error(traceback.format_exc())
        exit(1)
    else:
        last_success = Gauge('mybatchjob_last_success', 
            'Unixtime my batch job last succeeded', registry=registry)
        last_success.set_to_current_time()
    finally:
        if PROMETHEUS_PUSH_GW:
            pushadd_to_gateway(PROMETHEUS_PUSH_GW, job='python-pip-docker-template', registry=registry)
