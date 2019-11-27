from Snap7Connection import Snap7Connection as s7con
from assistant import Assistant
from Snap7Light import Snap7Light
from utilitys import configureLogger

assist = Assistant()


if __name__ == "__main__":
  configureLogger()
  client = s7con(assist.get_config())
  print(client.readBit(951, 5))
  client.setBit(951, 0)
  print(client.readBit(951, 0))
  client.writeInt(951, 0, 1 + 2 + 4 + 8 + 16 + 32 + 64 + 128 + 256)
  print(client.readInt(951, 0))
  client.closeConnection()
  exit
  lights = Snap7Light(assist.get_config())
  print(lights.getStatus("Wohnzimmer", "decke"))
  try:
    lights.turnOff("Wohnzimmer2", "decke")
  except Exception as err:
    pass
  print(lights.getStatus("Wohnzimmer", "decke"))
  lights.turnOn("Wohnzimmer", "decke")
  print(lights.getStatus("schlafzimmer", "alle"))
  s7con().closeConnection()