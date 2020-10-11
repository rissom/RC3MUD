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
    
    def save_room(room):
        filename = Config.workingpath+"/rooms/" + str(room.roomid)+".json"
        roomfile = open(filename, 'w')
        from game.room import Room
        roomfile.write(room.toJSON())
        roomfile.close()
        log.debug("Serializer: room saved: id: "+str(room.roomid))
        
    def get_area(areaid):
        filename = Config.workingpath+"/areas/" + str(areaid)+".json"
        if not os.path.exists(filename):
            log.error("Serializer: area does not exists: id: "+str(areaid)+" "+filename)
            from game.area import Area
            return Area(areaid)
        areafile = open(filename, 'r')
        filecontent = areafile.read()
        try:
            jsonobj = json.loads(filecontent)
        except:
            log.error("Serializer: JSON error: id: "+str(areaid)+" "+filename)
            jsonobj = False
        log.debug("Serializer: loading area: id: "+str(areaid)+" "+str(jsonobj))
        from game.area import Area
        area = Area(areaid)
        if not jsonobj==False:
            area.fromJSON(jsonobj)
        return area
        
        