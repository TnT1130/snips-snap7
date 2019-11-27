from Snap7Connection import Snap7Connection as s7con
from utilitys import lg

class Snap7Light():
  def __init__(self, config):
    self.__client = s7con(config)
    self.__rooms = config.get("secret")["rooms"].lower().split(",")
    self.__temperaturePos = "Ist,Soll,Decke,Feuchtigkeit,Boden1,Boden2,Boden3".lower().split(",")
    self.__temperatureDiffPos = "Plus_0_25,Plus_0_50,Plus_0_75,Plus_1_00,Minus_0_25,Minus_0_50,Minus_0_75,Minus_1_00".lower().split(",")
    self.__readDB = int(config.get("global")["temperatureread"])
    self.__writeDB = int(config.get("global")["temperaturewrite"])
    self.__readOffset = int(config.get("global")["TemperatureReadOffset".lower()]) * 8   
    self.__writeOffset = int(config.get("global")["TemperatureWriteOffset".lower()]) * 8 
                                                        #bits  intlen  
    if    self.__readOffset < len(self.__temperaturePos) * 8   * 2     + len(self.__temperatureDiffPos) \
       or self.__writeOffset < len(self.__temperatureDiffPos): 
       raise ValueError("Offset must be bigger than number Temperaturepositions")

  def __getReadOffset(self, room, pos = None, diffPos = None):
    offset = self.__rooms.index(room.lower()) * self.__readOffset
    if pos:
      if pos not in self.__temperaturePos:
        ValueError("unbekante Temperaturart.")
      offset += self.__temperaturePos.index(pos.lower()) * 8 * 2  # 8 * 2 = bitlength for int
    if diffPos:
      if diffPos not in self.__temperatureDiffPos:
        ValueError("unbekante Temperaturveränderung.")
      offset += self.__temperatureDiffPos.index(pos.lower())
    lg.debug("room: {}, type: {}, ReadOffset: {}".format(room, pos, offset))
    return offset

  def __getWriteOffset(self, room, pos = None, diffPos = None):
    offset = self.__rooms.index(room.lower()) * self.__writeOffset
    if pos:
      if pos not in self.__temperaturePos:
        ValueError("unbekante Temperaturart.")
      offset += self.__temperaturePos.index(pos.lower()) * 8 * 2
    if diffPos:
      if diffPos not in self.__temperatureDiffPos:
        ValueError("unbekante Temperaturveränderung.")
      offset += self.__temperatureDiffPos.index(pos.lower())
    lg.debug("room: {}, type: {}, WriteOffset: {}".format(room, pos, offset))
    return offset

  def getStatus(self, room, pos):
    tmp = self.__client.readBit(self.__readDB, self.__getReadOffset(room, pos))
    lg.info("room: {}, type: {}, Status: {}".format(room, pos, tmp))
    return tmp

  def changeTemp(self, room, difId):
      lg.info("room: {}, Action: {}".format(room, difId))
      self.__client.setBit(self.__writeDB, self.__getWriteOffset(room, diffPos= difId))

