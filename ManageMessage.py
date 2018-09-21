from sqlite.Sqlite import Sqlite
from Decrypter import Decrypter
import urllib2
import json
from pprint import pprint

class ManageMessage:

    _file_db = 'db/1'
    _Sqlite = None
    _messages = []
    _Decrypter = None

    def __init__(self):
        self._Sqlite = Sqlite(self._file_db)
        self._Decrypter = Decrypter()

    def getMessages(self):
        query = "SELECT * FROM messages;"
        cursor = self._Sqlite.getInfo(query)
        for line in cursor.fetchall():
            jsonObj = json.loads(line[1])
            self._messages.append(self.parseMediaToBase64(jsonObj))
        return self._messages

    def parseMediaToBase64(self, message):
        if 'clientUrl' in message and 'mediaKey' in message and 'type' in message:
            try:
                self._Decrypter.getMediaContent(message['clientUrl'], message['mediaKey'], message['type'])
                message['filebase64'] = self._Decrypter.getBase64File()
                return message
            except urllib2.HTTPError, e:
                #print e.code
                #print e.msg
                return message
        return message

ManageMessage = ManageMessage()
pprint(ManageMessage.getMessages())
