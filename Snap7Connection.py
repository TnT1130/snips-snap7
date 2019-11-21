import snap7, threading
from utilitys import lg



class Snap7Connection():
  class __Snap7Connection():
    def __init__(self, assistantConfig):
      self.__assistantConfig = assistantConfig
      self.__client = None
      self.__timer = None
    
    def __del__(self):
      self.closeConnection()

    def readBit(self, db, index):
      self.connect()
      offset = index // 8
      pos = index % 8
      tmpdata = self.__client.db_read(db, offset, 1)[0]
      tmpret = (tmpdata & 1<<pos) >> pos
      lg.debug("Read DB: {}, Byte: {}, Bit{}, Data: {}".format(db, offset, pos, tmpret))
      return tmpret

    def setBit(self, db, index):
      self.connect()
      offset = index // 8
      pos = index % 8
      mask = 1 << pos
      tmpData = (self.__client.db_read(db, offset, 1)[0] | mask)
      lg.debug("Write DB: {}, Byte: {}, Data: {}".format(db, offset, bin(tmpData)))
      self.__client.db_write(db, offset, bytearray([tmpData]))

    def clearBit(self, db, index):
      self.connect()
      offset = index // 8
      pos = index % 8
      mask = ~(1 << pos)
      tmpData = (self.__client.db_read(db, offset, 1)[0] & mask)
      lg.debug("Write DB: {}, Byte: {}, Data: {}".format(db, offset, bin(tmpData)))
      self.__client.db_write(db, offset, bytearray([tmpData]))

    def readInt(self, db, offset):
      self.connect()
      tmp = self.__client.db_read(db, offset, 2)
      tmpInt = int.from_bytes(tmp, byteorder='big', signed=True)
      lg.debug("readInt DB: {}, offset: {}, BinData: {}, Int: {}".format(db, offset, "b'" + (bin(tmp[0])[2:]).rjust(8, '0') \
                                                                         + ' ' +  (bin(tmp[1])[2:]).rjust(8, '0') + "'", tmpInt))
      return tmpInt

    def writeInt(self, db, index, data):
      self.connect()
      offset = index // 8
      tmpdata = bytearray(data.to_bytes(2, byteorder='big', signed=True))
      lg.debug("writeInt DB: {}, offset: {}, BinData: {}, Int: {}".format(db, offset, "b'" + (bin(tmpdata[0])[2:]).rjust(8, '0') \
                                                                         + ' ' +  (bin(tmpdata[1])[2:]).rjust(8, '0') + "'", data))
      self.__client.db_write(db, offset, tmpdata)

    def connect(self):  
      if not self.__client:
        lg.info("connect to SPS IP: {}, PORT: {}, RACK: {}, SLOT: {}".format(
          self.__assistantConfig["spsip"],
          self.__assistantConfig.get("spsrack", 0),
          self.__assistantConfig.get("spsslot", 2),
          self.__assistantConfig.get("spsport", 102)
        ))
        self.__client = snap7.client.Client()
        self.__client.connect(self.__assistantConfig["spsip"], 
                              int(self.__assistantConfig.get("spsrack", 0)), 
                              int(self.__assistantConfig.get("spsslot", 2)), 
                              int(self.__assistantConfig.get("spsport", 102)))
        self.__client.set_connection_type(2)
      self.__restartTimer()
    
    def __restartTimer(self):
      if self.__timer:
        self.__timer.cancel()
      self.__timer = threading.Timer(60.0 * int(self.__assistantConfig.get("spsconnectionkeepalive", 1)), self.closeConnection)
      self.__timer.start()

    def closeConnection(self):
      if self.__client:
        lg.info("close SPS-Connection")
        self.__client.disconnect()
        self.__client.destroy()
        self.__client = None
      if self.__timer:
        self.__timer.cancel()

  instance = None
  def __new__(cls, assistantConfig = None):
    if Snap7Connection.instance is None:
      if assistantConfig:
        Snap7Connection.instance = Snap7Connection.__Snap7Connection(assistantConfig)
      else:
        raise Exception("config required")
    return Snap7Connection.instance
  
  def __getattr__(self, name):
    return getattr(self.instance, name)
  
  def __setattr__(self, name, value):
    return setattr(self.instance, name, value)