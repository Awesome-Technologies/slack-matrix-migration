import requests

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
                print(r.json()["error"])
                print(matrix_message)
            except Exception:
                pass
        return False

    return r
