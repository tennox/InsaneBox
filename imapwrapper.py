import os
from collections import defaultdict
from pprint import PrettyPrinter

from imapclient import IMAPClient

pp = PrettyPrinter(indent=4)

""" Prints the server response with "> " in front of each line """

def printr(response):
    if type(response) == bytes:
        response = response.decode("utf-8")
    elif type(response) == dict:
        response = pp.pformat(response)
    elif type(response) == defaultdict:
        response = pp.pformat(dict(response))
    elif response == None:
        return
    elif type(response) != str:
        print("Unknown type " + str(type(response)) + " for printr")
        response = str(response)
    #print(response)
    print(os.linesep.join(["> " + x for x in response.splitlines()]))

class IMAPWrapper:
    host = "mail.local"
    username = "user"
    password = "user"
    ssl = False

    client = None

    def __enter__(self):
        self.connect()
        self.create_folders()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Logging out...")
        printr(self.client.logout())

    def connect(self):
        self.client = IMAPClient(self.host, use_uid=True, ssl=self.ssl)
        print("Logging in as " + self.username + "@" + self.host + "...")
        printr(self.client.login(self.username, self.password))

    def create_folders(self):
        print("Checking folders...")
        if not self.client.folder_exists("InsaneLater"):
            print("Creating folder 'InsaneLater'...")
            printr(self.client.create_folder("InsaneLater"))
        if not self.client.folder_exists("InsaneQuestions"):
            print("Creating folder 'InsaneQuestions'...")
            printr(self.client.create_folder("InsaneQuestions"))
        if not self.client.folder_exists("InsaneQuestions.Yes"):
            print("Creating folder 'InsaneQuestions.Yes'...")
            printr(self.client.create_folder("InsaneQuestions.Yes"))
        if not self.client.folder_exists("InsaneQuestions.No"):
            print("Creating folder 'InsaneQuestions.No'...")
            printr(self.client.create_folder("InsaneQuestions.No"))

    def add_question(self, title, text):
        print("Adding Question '%s'..." % title)
        self.create_mail("InsaneQuestions", "From: InsaneBox\n"
                                            "To: User\n"
                                            "Subject: %s\n"
                                            "\n%s\n" % (title, text))

    def create_mail(self, folder, mail, flags=(), time=None):
        print("Creating mail in '" + folder + "'...")
        printr(self.client.append(folder, mail, flags, time))

    def move_mail(self, ids, folder):
        print("Moving message %s to '%s'..." % (str(ids), folder))
        printr(self.client.copy(ids, folder))
        printr(self.client.delete_messages(ids))

    def select_folder(self, folder):
        print("Selecting folder '" + folder + "'...")
        printr(self.client.select_folder(folder))

    def print_messages(messages, marker="|"):
        for id, data in messages.items():
            print(marker+" ID %d: \"%s\"" % (id, data[b'ENVELOPE'].subject.decode('utf8')))
