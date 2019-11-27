from Snap7Connection import Snap7Connection as s7con
from utilitys import lg

class Snap7Shutter():
  def __init__(self, config):
    self.__client = s7con(config)
    self.__rooms = config.get("secret")["rooms"].lower().split(",")
    self.__lightPos = "alle,fenster,tuer".lower().split(",")
    self.__readDB = int(config.get("global")["shutterread"])
    self.__writeDB = int(config.get("global")["shutterwrite"])
    self.__readOffset = int(config.get("global")["ShutterReadOffset".lower()]) * 8   
    self.__writeOffset = int(config.get("global")["ShutterWriteOffset".lower()]) * 8 
    if    self.__readOffset < len(self.__lightPos) * 8 * 2 \
       or self.__writeOffset < len(self.__lightPos) * 8 * 4: 
       raise ValueError("Offset must be bigger than number lightpositions")

  def __getReadOffset(self, room, pos):
    offset = self.__rooms.index(room.lower()) * self.__readOffset
    offset += self.__lightPos.index(pos.lower()) * 8 * 2
    lg.debug("room: {}, type: {}, ReadOffset: {}".format(room, pos, offset))
    return offset

  def __getWriteOffset(self, room, pos):
    offset = self.__rooms.index(room.lower()) * self.__writeOffset
    offset += self.__lightPos.index(pos.lower()) * 8 * 4
    lg.debug("room: {}, type: {}, WriteOffset: {}".format(room, pos, offset))
    return offset

  def getStatus(self, room, pos):
    tmp = self.__client.readInt(self.__readDB, self.__getReadOffset(room, pos)+8)
    lg.info("room: {}, type: {}, Status: {}".format(room, pos, tmp))
    return tmp

  def close(self, room, pos):
    lg.info("room: {}, type: {}, Action: Close".format(room, pos))
    self.__client.setBit(self.__writeDB, self.__getWriteOffset(room, pos) + 1)

  def open(self, room, pos):
    lg.info("room: {}, type: {}, Action: Open".format(room, pos))
    self.__client.setBit(self.__writeDB, self.__getWriteOffset(room, pos))
