from slack import RTMClient
import getpass
import numpy as np

try:
    with open(".slack_access_token.txt", "r") as f:
        access_token = f.read()
except FileNotFoundError:
    access_token = getpass.getpass(prompt='Slack Access Token: ', stream=None)
    with open(".slack_access_token.txt", "wb") as f:
        f.write(access_token.encode())

def run_on_event(data, web_client):
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']
    web_client.chat_postMessage(
        channel=channel_id,
        text=f"Hi <@{user}>! You are interested in LIGO stuff, right? Let me get right on that for you.",
        thread_ts=thread_ts,
        icon_emoji=':ligo:'
    )
    split_message = data['text'].split(" ")

    gw_name = None
    gw_file = None
    rev_no = None

    for x in split_message:
        if x[0] in ["s", "S"]:
            if np.sum([y.isdigit() for y in x[1:7]]) == 6:
                gw_name = x

        elif ".fits" in x:
            gw_file = x
        if "rev" in x:
            rev_no = x.split("=")[1]
     
    message = ""

    if gw_name is not None:
        message = "You are interested in LIGO event {0}.".format(gw_name)
    
    if rev_no is not None:
        if gw_name is None:
            message = "You have specified a revision number, but not a GW event name."
        else:
            message += "You have specified revision number {0}".format(rev_no)
    
    if gw_file is not None:
        if gw_name is not None:
            message = "You have specified both a fits file and a GW event name. Please specify only one."
        else:
            message = "You are interested in the following fits fille: {0}.".format(gw_file)
    web_client.chat_postMessage(
        channel=channel_id,
        text=message,
        thread_ts=thread_ts,
        icon_emoji=':ligo:'
    )


keywords = ["<@UMNJK00CU>", "LIGO", "banana"]

@RTMClient.run_on(event="message")
def say_hello(**payload):
    data = payload['data']
    print(data.items())
    web_client = payload['web_client']
    try:
        if not np.logical_and(np.sum([x in data['text'] for x in keywords]) == 0, "DMBKJG00K" not in data["channel"]):
            run_on_event(data, web_client)
    except KeyError:
        pass 
# slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = RTMClient(token=access_token)
rtm_client.start()