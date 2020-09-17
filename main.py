from logging import error
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from plyer import notification
import os
from time import sleep
from playsound import playsound


MAILSCOPES = ["https://mail.google.com/"]


def authenticate_google():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("mailtoken.pickle"):
        with open("mailtoken.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", MAILSCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("mailtoken.pickle", "wb") as token:
            pickle.dump(creds, token)
    gservice = build("gmail", "v1", credentials=creds)

    return gservice


def get_email(service):
    """
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    # Call the Gmail API to fetch INBOX
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], q="is:unread")
        .execute()
    )
    messages = results.get("messages", [])

    message_pairs = []
    if not messages:
        pass
    else:

        for index in range(0, len(messages)):
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=messages[index]["id"])
                .execute()
            )
            headers = msg["payload"]["headers"]
            subject = [i["value"] for i in headers if i["name"] == "Subject"][0]

            sender = [i["value"] for i in headers if i["name"] == "From"][0]

            message_pairs.append({"sender": sender, "subject": subject})

    return message_pairs


gservice = authenticate_google()

pairs_before = []

print("Waiting for an unread email...")


while True:
    unread = False
    pairs = get_email(gservice)

    # Set method cannot be used as dictionaries cannot be within sets. (So slow list comparison method used)
    diff = [item for item in pairs if item not in pairs_before]
    if diff:

        for email in diff:
            unread = True

            sender = email["sender"]
            subject = email["subject"]

            print("Sender: " + sender + " Subject: " + subject)

            try:
                notification.notify(
                    title="Message from " + sender, message=subject, app_icon=None
                )
            except error as e:
                # print(e)
                pass

    if unread:
        playsound("alarm.mp3")

    pairs_before = pairs

    sleep(2)
