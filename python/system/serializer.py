import os
import json
from system.config import Config
from system.log import log


class Serializer(object):
    
    def get_room(roomid):
        filename = Config.workingpath+"/rooms/" + str(roomid)+".json"
        if not os.path.exists(filename):
            log.error("Serializer: room does not exists: id: "+str(roomid)+" "+filename)
            return None
        roomfile = open(filename, 'r')
        filecontent = roomfile.read()
        jsonobj = json.loads(filecontent)
        log.debug("Serializer: loading room: id: "+str(roomid)+" "+str(jsonobj))
        from game.room import Room
        room = Room(roomid)
        room.fromJSON(jsonobj)
        return room
        
        
        