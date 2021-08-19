# -*- coding: utf-8 -*-
# Copyright 2019, 2020 Awesome Technologies Innovationslabor GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import functools
import logging

LOG_LEVEL = os.environ.get('LOG_LEVEL', "INFO").upper()
logging.basicConfig(level=LOG_LEVEL)
log = logging.getLogger('SLACK.MIGRATE')
fileHandler = logging.FileHandler("log/migration.log"))
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)


def send_event(
    config,
    matrix_message,
    matrix_room,
    matrix_user_id,
    event_type,
    txnId,
    ts=0,
):

    if ts:
        url = "%s/_matrix/client/r0/rooms/%s/send/%s/%s?user_id=%s&ts=%s" % (config["homeserver"],matrix_room,event_type,txnId,matrix_user_id,ts,)
    else:
        url = "%s/_matrix/client/r0/rooms/%s/send/%s/%s?user_id=%s" % (config["homeserver"],matrix_room,event_type,txnId,matrix_user_id,)

    #_log.info("Sending registration request...")
    r = requests.put(url, headers={'Authorization': 'Bearer ' + config["as_token"]}, json=matrix_message, verify=False)

    if r.status_code != 200:
        log.error("ERROR! Received %d %s" % (r.status_code, r.reason))
        if 400 <= r.status_code < 500:
            try:
                log.error(' '.join([r.status_code, r.json()["error"]]))
                log.debug(matrix_message)
            except Exception:
                pass
        return False

    return r
