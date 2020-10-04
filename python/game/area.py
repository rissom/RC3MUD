from system.serializer import Serializer

class Area(object):
    
    all_areas = []
    
    def get_area_by_id(areaid):
        for area in Area.all_areas:
            if area.id == areaid:
                return area
        area = Serializer.get_area(areaid)
        Area.all_areas.append(area)
        return area
    
    def __init__(self,id):
        self.id = id
        self.name = "* not named yet *"
        self.parent_area_id = -1
        
    def are_ids_in_chain(self,ids):
        for id in ids:
            if self.id == id:
                return True
        if self.parent_area_id==-1:
            return False
        return Area.get_area_by_id(self.parent_area_id).are_ids_in_chain(ids)
            
    def fromJSON(self, json):
        self.id = json["id"]
        self.parent_area_id = json["parentid"]
        self.name = json["name"]
        
    def toJSON(self):
        ans = { "id" : self.id,
               "parentid": self.parent_area_id,
               "name" : self.name
             }
        return json.dumps(ans,indent=4).replace('\n', '\r\n')
