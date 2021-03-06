from Snap7Connection import Snap7Connection as s7con
from utilitys import lg

class Snap7Light():
  def __init__(self, config):
    self.__client = s7con(config)
    self.__rooms = config.get("secret")["rooms"].lower().split(",")
    self.__lightPos = "alle,Decke,indirekt,Bett1,Bett2,Dusche,Links,Rechts,Steckdose1,Steckdose2,Steckdose3,Steckdose4,Steckdose5,Steckdose6,Steckdose7,Steckdose8".lower().split(",")
    self.__readDB = int(config.get("global")["lightread"])
    self.__writeDB = int(config.get("global")["lightwrite"])
    self.__readOffset = int(config.get("global")["LightReadOffset".lower()]) * 8   
    self.__writeOffset = int(config.get("global")["LightWriteOffset".lower()]) * 8 
    if    self.__readOffset * 8 < len(self.__lightPos) \
       or self.__writeOffset * 8 < len(self.__lightPos):
       raise ValueError("Offset must be bigger than number lightpositions")

  def __getReadOffset(self, room, pos):
    offset = self.__rooms.index(room.lower()) * self.__readOffset
    offset += self.__lightPos.index(pos.lower())
    lg.debug("room: {}, type: {}, ReadOffset: {}".format(room, pos, offset))
    return offset

  def __getWriteOffset(self, room, pos):
    offset = self.__rooms.index(room.lower()) * self.__writeOffset
    offset += self.__lightPos.index(pos.lower())
    lg.debug("room: {}, type: {}, WriteOffset: {}".format(room, pos, offset))
    return offset

  def getStatus(self, room, pos):
    tmp = self.__client.readBit(self.__readDB, self.__getReadOffset(room, pos))
    lg.info("room: {}, type: {}, Status: {}".format(room, pos, tmp))
    return tmp

  def turnOn(self, room, pos):
    if self.getStatus(room, pos) == 0:
      lg.info("room: {}, type: {}, Action: TurnOn".format(room, pos))
      self.__client.setBit(self.__writeDB, self.__getWriteOffset(room, pos))
      return 1
    elif pos.upper() == "Decke".upper():
      if room.upper() == "Wohnzimmer".upper() or room.upper() == "Küche".upper():
        lg.info("room: {}, type: {}, Action: TurnOn".format(room, pos))
        self.__client.setBit(self.__writeDB, self.__getWriteOffset(room, pos))
        return 1
      else:
        return 0
    else:
      return 0
      
  def turnOff(self, room, pos):
    if self.getStatus(room, pos) == 1:
      lg.info("room: {}, type: {}, Action: TurnOff".format(room, pos))
      self.__client.setBit(self.__writeDB, self.__getWriteOffset(room, pos))
      return 1
    elif pos.upper() == "Decke".upper():
      if room.upper() == "Wohnzimmer".upper() or room.upper() == "Küche".upper():
        lg.info("room: {}, type: {}, Action: TurnOn".format(room, pos))
        self.__client.setBit(self.__writeDB, self.__getWriteOffset(room, pos))
        return 1
      else:
        return 0
    else:
      return 0
