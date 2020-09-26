
from system.serializer import Serializer
from system.log import log

class Room(object):
    
    all_rooms = []
    
    # class function to get a room by id
    def get_room_by_id(roomid):
        for room in Room.all_rooms:
            if room.roomid == roomid:
                return room
        room = Serializer.get_room(roomid)
        Room.all_rooms.append(room)
        return room
    
    
    def __init__(self, roomid):
        self.roomid = roomid
        self.player = []  # player in this room
        self.description = "\r\nThis is the well known undefined void where nothing has been created yet.\r\nThere are no exits and there is nothing to find here."
        
    def fromJSON(self, json):
        log.debug("not able to deserialize yet: "+str(json))
        