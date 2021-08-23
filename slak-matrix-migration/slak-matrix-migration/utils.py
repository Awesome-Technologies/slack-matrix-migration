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
import traceback

import os
import logging

LOG_LEVEL = os.environ.get('LOG_LEVEL', "INFO").upper()

logging.basicConfig(level=LOG_LEVEL)
log = logging.getLogger('SLACK.MIGRATE')
log_filename = "log/migration.log"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
fileHandler = logging.FileHandler(log_filename, mode="w", encoding=None, delay=False)
log.addHandler(fileHandler)
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# log.addHandler(consoleHandler)


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
    
    try:
        r = requests.put(url, headers={'Authorization': 'Bearer ' + config["as_token"]}, json=matrix_message, verify=False)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        log.error(
            "Logging an uncaught exception {}".format(e),
            exc_info=(traceback)
        )
        log.debug("error creating room {}".format(body))
        return False
    else:
        if r.status_code != 200:
            log.error("ERROR! Received %d %s" % (r.status_code, r.reason))
            if r.status_code == 403:
                invite_user(
                    matrix_room,
                    matrix_user_id,
                    conf
                )
                try:
                    r = requests.put(url, headers={'Authorization': 'Bearer ' + config["as_token"]}, json=matrix_message, verify=False)
                except requests.exceptions.RequestException as e:
                    # catastrophic error. bail.
                    log.error(
                        "Logging an uncaught exception {}".format(e),
                        exc_info=(traceback)
                    )
                    log.debug("error creating room {}".format(body))
                    return False
                else:
                    if r.status_code == 200:
                        return r
                    else:
                        return False
        if 400 <= r.status_code < 500:
            try:
                log.error(' '.join([r.status_code, r.json()["error"]]))
                log.debug(matrix_message)
            except Exception:
                pass
            return False
        return r

def invite_user(
    roomId,
    matrix_user_id,
    config,
):
    if config["create-as-admin"]:
        log.info("Invite {} to {}".format(matrix_user_id,roomId))
        _mxCreator = "".join(["@", config['admin_user'], ":", config["domain"]])

        url = "%s/_matrix/client/r0/rooms/%s/invite?user_id=%s" % (config["homeserver"],roomId,_mxCreator,)
        body = {
            "user_id": matrix_user_id,
        }

        #_log.info("Sending registration request...")
        try:
            r = requests.post(url, headers={'Authorization': 'Bearer ' + config["as_token"]}, json=body, verify=False)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            log.error(
                "Logging an uncaught exception {}".format(e),
                exc_info=(traceback)
            )
            log.debug("error creating room {}".format(body))
            return False
        else:
            if r.status_code != 200:
                log.info("ERROR! Received %d %s" % (r.status_code, r.reason))
                if 400 <= r.status_code < 500:
                    try:
                        log.info(r.json()["error"])
                    except Exception:
                        pass