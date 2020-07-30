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

def super_print(filename):
    '''filename is the file where output will be written'''
    def wrap(func):
        '''func is the function you are "overriding", i.e. wrapping'''
        def wrapped_func(*args,**kwargs):
            '''*args and **kwargs are the arguments supplied
            to the overridden function'''
            #use with statement to open, write to, and close the file safely
            with open(filename,'a') as outputfile:
                outputfile.write(*args,**kwargs)
                outputfile.write("\n")
            #now original function executed with its arguments as normal
            return func(*args,**kwargs)
        return wrapped_func
    return wrap

print = super_print('migration.log')(print)

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

    #_print("Sending registration request...")
    r = requests.put(url, headers={'Authorization': 'Bearer ' + config["as_token"]}, json=matrix_message, verify=False)

    if r.status_code != 200:
        print("ERROR! Received %d %s" % (r.status_code, r.reason))
        if 400 <= r.status_code < 500:
            try:
                print(' '.join([r.status_code, r.json()["error"]]))
                #print(matrix_message)
            except Exception:
                pass
        return False

    return r
