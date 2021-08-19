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
import slackdown
import logging
import os

from utils import send_event
from emoji import emojize


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

'''
 * Converts a slack image attachment to a matrix image event.
 *
 * @param {Object} file The slack image attachment file object.
 * @param {?integer} file.size size of the file in bytes.
 * @param {string} file.title alt-text for the file.
 * @param {string} file.mimetype mime-type of the file.
 * @param {?integer} file.original_w width of the file if an image, in pixels.
 * @param {?integer} file.original_h height of the file if an image, in pixels.
 * @param {?string} file.thumb_360 URL of a 360 pixel wide thumbnail of the
 *     file, if an image.
 * @param {?integer} file.thumb_360_w width of the thumbnail of the 360 pixel
 *     wide thumbnail of the file, if an image.
 * @param {?integer} file.thumb_360_h height of the thumbnail of the 36 pixel
 *     wide thumbnail of the file, if an image.
 * @param {string} url The matrix file mxc.
 * @param {?string} thumbnail_url The matrix thumbnail mxc.
 * @return {Object} Matrix event content, as per https://matrix.org/docs/spec/#m-image
'''

def slackImageToMatrixImage(file, url, thumbnailUrl):
    message = {
        "body": file["title"],
        "info": {
            "mimetype": file["mimetype"],
            "size": file["size"],
        },
        "msgtype": "m.image",
        "url": url,
        # TODO: Define some matrix types
    }

    if "original_w" in file:
        message["info"]["w"] = file["original_w"]

    if "original_h" in file:
        message["info"]["h"] = file["original_h"]

    if thumbnailUrl:
        message["thumbnail_url"] = thumbnailUrl
        message["thumbnail_info"] = {}
        if "thumb_360_w" in file:
            message["thumbnail_info"]["w"] = file["thumb_360_w"]

        if "thumb_360_h" in file:
            message["thumbnail_info"]["h"] = file["thumb_360_h"]

    return message

'''
 * Converts a slack video attachment to a matrix video event.
 *
 * @param file The slack video attachment file object.
 * @param file.size size of the file in bytes.
 * @param file.title alt-text for the file.
 * @param file.mimetype mime-type of the file.
 * @param file.original_w width of the file if an image, in pixels.
 * @param file.original_h height of the file if an image, in pixels.
 * @param url The matrix file mxc.
 * @param thumbnail_url The matrix thumbnail mxc.
 * @return Matrix event content, as per https://matrix.org/docs/spec/client_server/r0.4.0.html#m-video
'''

def slackImageToMatrixVideo(file, url, thumbnailUrl):
    message = {
        "body": file["title"],
        "info": {
            "mimetype": file["mimetype"],
            "size": file["size"],
        },
        "msgtype": "m.video",
        "url": url,
        # TODO: Define some matrix types
    }


    if "original_w" in file:
        message["info"]["w"] = file["original_w"]

    if "original_h" in file:
        message["info"]["h"] = file["original_h"]

    if thumbnailUrl:
        message["thumbnail_url"] = thumbnailUrl
        # Slack don't tell us the thumbnail size for videos. Boo

    return message

'''
 * Converts a slack audio attachment to a matrix audio event.
 *
 * @param {Object} file The slack audio attachment file object.
 * @param {?integer} file.size size of the file in bytes.
 * @param {string} file.title alt-text for the file.
 * @param {string} file.mimetype mime-type of the file.
 * @param {string} url The matrix file mxc.
 * @return {Object} Matrix event content, as per https://matrix.org/docs/spec/client_server/r0.4.0.html#m-audio
'''

def slackImageToMatrixAudio(file, url):
    return {
        "body": file["title"],
        "info": {
            "mimetype": file["mimetype"],
            "size": file["size"],
        },
        "msgtype": "m.audio",
        "url": url,
    }

'''
 * Converts a slack file upload to a matrix file upload event.
 *
 * @param file The slack file object.
 * @param url The matrix file mxc.
 * @param thumbnail_url The matrix thumbnail mxc.
 * @return Matrix event content, as per https://matrix.org/docs/spec/#m-file
'''

def slackFileToMatrixMessage(file, url, thumbnailUrl):
    if "mimetype" in file:
        if file["mimetype"].startswith("image/"):
            return slackImageToMatrixImage(file, url, thumbnailUrl)
        if file["mimetype"].startswith("video/"):
                return slackImageToMatrixVideo(file, url, thumbnailUrl)
        if file["mimetype"].startswith("audio/"):
            return slackImageToMatrixAudio(file, url)

    return  {
        "body": file["title"],
        "info": {
            "mimetype": file["mimetype"],
            "size": file["size"],
        },
        "msgtype": "m.file",
        "url": url,
    }

def uploadContentFromURI(content, uri, config, user):
    res = requests.get(uri)
    if res.status_code != 200:
        log.info("ERROR! Received %d %s" % (res.status_code, res.reason))
        if 400 <= res.status_code < 500:
            try:
                log.info(res.json()["error"])
            except Exception:
                pass
        return ''

    file_content = res.content

    url = "%s/_matrix/media/r0/upload?user_id=%s&filename=%s" % (config["homeserver"],user,content["title"],)
    try:
        r = requests.post(url, headers={'Authorization': 'Bearer ' + config["as_token"], 'Content-Type': content["mimetype"]}, data=file_content, verify=False)
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
        else:
            return r.json()["content_uri"]

def process_attachments(attachments, roomId, userId, body, txnId, config):
    for file in attachments:
        txnId = process_file(file, roomId, userId, body, txnId, config)
    return txnId

def process_files(files, roomId, userId, body, txnId, config):
    for file in files:
        txnId = process_file(file, roomId, userId, body, txnId, config)
    return txnId

def get_link(file):
    if file["public_url_shared"]:
        link = file["permalink_public"]
    else:
        link = file["url_private"]
    return link

def process_snippet(file, roomId, userId, body, txnId, config, ts):
    htmlString = ""
    res = requests.get(file["url_private"])
    if res.status_code != 200:
        log.info("ERROR! Received %d %s" % (res.status_code, res.reason))
        if 400 <= res.status_code < 500:
            try:
                log.info(res.json()["error"])
            except Exception:
                pass
        return txnId

    htmlString = res.content.decode("utf-8")

    htmlCode = ""
    # Because escaping 6 backticks is not good for readability.
    code = "```\n" + htmlString + "\n```"
    if "filetype" in file:
        htmlCode = '<pre><code class="language-' + file["filetype"] + '">'
    else:
        htmlCode = "<pre><code>"

    htmlCode += htmlString
    htmlCode += "</code></pre>"

    messageContent = {
        "body": code,
        "format": "org.matrix.custom.html",
        "formatted_body": htmlCode,
        "msgtype": "m.text",
    }

    # send message to room
    res = send_event(config, messageContent, roomId, userId, "m.room.message", txnId, ts)
    if res == False:
        link = get_link(file)
        log.info("Could not send snippet: " + link)
        log.info("Trying to send as file...")
        txnId = process_upload(file, roomId, userId, body, txnId, config, ts)
        return txnId

    return txnId

def process_upload(file, roomId, userId, body, txnId, config, ts):
    if "maxUploadSize" in config and file["size"] > config["maxUploadSize"]:
        link = get_link(file)
        log.info("WARNING: File too large, sending as a link: " + link);
        messageContent = {
            "body": link + '(' + file["name"] + ')',
            "format": "org.matrix.custom.html",
            "formatted_body": '<a href="' + link + '">' + file["name"] + '</a>',
            "msgtype": "m.text",
        }
        res = send_event(config, messageContent, roomId, userId, "m.room.message", txnId, ts)
        if res == False:
            log.info("ERROR while sending file link to room '" + roomId)

    else:
        thumbUri = ""
        thumbnailContentUri=""

        if "thumb_video" in file:
            thumbUri = file["thumb_video"]
        if "thumb_360" in file:
            thumbUri = file["thumb_360"]

        if thumbUri and "filetype" in file:
            content = {
                "mimetype": file["mimetype"],
                "title": file["name"] + '_thumb' + file["filetype"],
            }

            thumbnailContentUri = uploadContentFromURI(content, thumbUri, config, userId)

        fileContentUri = uploadContentFromURI({"title": file["title"], "mimetype": file["mimetype"]}, file["url_private"], config, userId)

        messageContent = slackFileToMatrixMessage(file, fileContentUri, thumbnailContentUri)

        res = send_event(config, messageContent, roomId, userId, "m.room.message", txnId, ts)
        if res == False:
            log.info("ERROR while sending file to room '" + roomId)

    txnId = txnId + 1
    return txnId

def process_file(file, roomId, userId, body, txnId, config):
    if not "url_private" in file:
        # we have no url to process the file
        return txnId

    ts = str(file["timestamp"]) + "000"

    if file["mode"] == "snippet":
        txnId = process_snippet(file, roomId, userId, body, txnId, config, ts)
    else:
        txnId = process_upload(file, roomId, userId, body, txnId, config, ts)

    txnId = txnId + 1
    return txnId
