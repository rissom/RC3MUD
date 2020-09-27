import os
import json
from system.config import Config
from system.log import log


class Serializer(object):
    
    def get_room(roomid):
        filename = Config.workingpath+"/rooms/" + str(roomid)+".json"
        if not os.path.exists(filename):
            log.error("Serializer: room does not exists: id: "+str(roomid)+" "+filename)
            from game.room import Room
            return Room(roomid)
        roomfile = open(filename, 'r')
        filecontent = roomfile.read()
        try:
            jsonobj = json.loads(filecontent)
        except:
            log.error("Serializer: JSON error: id: "+str(roomid)+" "+filename)
            jsonobj = False
        log.debug("Serializer: loading room: id: "+str(roomid)+" "+str(jsonobj))
        from game.room import Room
        room = Room(roomid)
        if not jsonobj==False:
            room.fromJSON(jsonobj)
        return room
    
    
        
        