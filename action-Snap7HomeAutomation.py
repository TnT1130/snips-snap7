#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from Snap7Light import Snap7Light
from Snap7Shutter import Snap7Shutter
from Snap7Temperature import Snap7Temperature
from assistant import Assistant
from utilitys import catchErrors, getSlotValue, lg, configureLogger
#hermes: 'publish_continue_session', 'publish_end_session', 'publish_start_session_action', 'publish_start_session_notification',

# ======================================================================================================================

assist = Assistant()
lights = Snap7Light(assist.get_config())
shutter = Snap7Shutter(assist.get_config())
temp = Snap7Temperature(assist.get_config())


# ======================================================================================================================
@catchErrors
def activateObject(hermes, intent_message): 
  location = getSlotValue(intent_message.slots, "deviceLocation", intent_message.site_id if intent_message.site_id != "default" else "wohnzimmer")
  device = getSlotValue(intent_message.slots, "device", "")
  deviceType = getSlotValue(intent_message.slots, "deviceType", "default")
  lg.debug("activateObject:    location: {}, device: {}, deviceType: {}".format(location, device, deviceType))
  if device.upper() == "Licht".upper():
    deviceType = deviceType if deviceType != "default" else "decke"
    lights.turnOn(location, deviceType)
    hermes.publish_end_session(intent_message.session_id, "Licht im {} wird angeschalten".format(location))
  elif device.upper() == "Rollo".upper():
    deviceType = deviceType if deviceType != "default" else "fenster"
    shutter.open(location, deviceType)
    hermes.publish_end_session(intent_message.session_id, "Rolladen im {} wird geöffnet".format(location))
  else:
    hermes.publish_end_session(intent_message.session_id, "Gerätetyp {} wird aktuell nicht unterstützt".format(device))

@catchErrors
def deactivateObject(hermes, intent_message):
  location = getSlotValue(intent_message.slots, "deviceLocation", intent_message.site_id if intent_message.site_id != "default" else "wohnzimmer")
  device = getSlotValue(intent_message.slots, "device", "")
  deviceType = getSlotValue(intent_message.slots, "deviceType", "default")
  lg.debug("deactivateObject:    location: {}, device: {}, deviceType: {}".format(location, device, deviceType))
  if device.upper() == "Licht".upper():
    deviceType = deviceType if deviceType != "default" else "decke"
    lights.turnOff(location, deviceType)
    hermes.publish_end_session(intent_message.session_id, "Licht im {} wird ausgeschalten".format(location))
  elif device.upper() == "Rollo".upper():
    deviceType = deviceType if deviceType != "default" else "fenster"
    shutter.close(location, deviceType)
    hermes.publish_end_session(intent_message.session_id, "Rolladen im {} wird geschlossen.".format(location))
  else:
    hermes.publish_end_session(intent_message.session_id, "Gerätetyp {} wird aktuell nicht unterstützt".format(device))

@catchErrors
def getObjectStatus(hermes, intent_message):
  location = getSlotValue(intent_message.slots, "deviceLocation", intent_message.site_id if intent_message.site_id != "default" else "wohnzimmer")
  device = getSlotValue(intent_message.slots, "device", "")
  deviceType = getSlotValue(intent_message.slots, "deviceType", "default")
  lg.debug("getObjectStatus:    location: {}, device: {}, deviceType: {}".format(location, device, deviceType))
  if device.upper() == "Licht".upper():
    deviceType = deviceType if deviceType != "default" else "decke"
    if lights.getStatus(location, deviceType) == 1:
      hermes.publish_end_session(intent_message.session_id, "Das Licht im {} ist angeschalten".format(location))
    else:  
      hermes.publish_end_session(intent_message.session_id, "Das Licht im {} ist ausgeschalten".format(location))
  elif device.upper() == "Rollo".upper():
    deviceType = deviceType if deviceType != "default" else "fenster"
    tmp = shutter.getStatus(location, deviceType)
    if tmp == 0:
      hermes.publish_end_session(intent_message.session_id, "Rolladen im {} ist komplett geöffnet.".format(location))
    elif tmp < 33:
      hermes.publish_end_session(intent_message.session_id, "Rolladen im {} ist leicht geschlossen.".format(location))
    elif tmp < 66:
      hermes.publish_end_session(intent_message.session_id, "Rolladen im {} ist zur hälfte geschlossen.".format(location))
    elif tmp < 100:
      hermes.publish_end_session(intent_message.session_id, "Rolladen im {} ist weit geschlossen.".format(location))
    elif tmp == 100:
      hermes.publish_end_session(intent_message.session_id, "Rolladen im {} ist komplett geschlossen.".format(location))
  else:
    hermes.publish_end_session(intent_message.session_id, "Gerätetyp {} wird aktuell nicht unterstützt".format(device))

@catchErrors
def getTemperature(hermes, intent_message):
  ObjectLocation = getSlotValue(intent_message.slots, "ObjectLocation", intent_message.site_id if intent_message.site_id != "default" else "wohnzimmer")
  tempType = getSlotValue(intent_message.slots, "tempType", "Ist")
  hermes.publish_end_session(intent_message.session_id, "Die Temperatur im {} beträgt {} Grad.".format(ObjectLocation, temp.getStatus(ObjectLocation, tempType) / 100.0))

@catchErrors
def getIncrease(hermes, intent_message):
  ObjectLocation = getSlotValue(intent_message.slots, "ObjectLocation", intent_message.site_id if intent_message.site_id != "default" else "wohnzimmer")
  tempChangeType = "Plus_" + getSlotValue(intent_message.slots, "tempChangeType", "1_00")
  temp.changeTemp(ObjectLocation, tempChangeType)
  hermes.publish_end_session(intent_message.session_id, "Temperatur im {} wird verändert.".format(ObjectLocation))

@catchErrors
def getDecrease(hermes, intent_message):
  ObjectLocation = getSlotValue(intent_message.slots, "ObjectLocation", intent_message.site_id if intent_message.site_id != "default" else "wohnzimmer")
  tempChangeType = "Minus_" + getSlotValue(intent_message.slots, "tempChangeType", "1_00")
  temp.changeTemp(ObjectLocation, tempChangeType)
  hermes.publish_end_session(intent_message.session_id, "Temeperatur im {} wird verändert.".format(ObjectLocation))

@catchErrors
def setRollerBlinds(hermes, intent_message):
  ObjectLocation = getSlotValue(intent_message.slots, "ObjectLocation", intent_message.site_id if intent_message.site_id != "default" else "wohnzimmer")
  WindowType = getSlotValue(intent_message.slots, "WindowType", "alle")
  MovementDirection = getSlotValue(intent_message.slots, "MovementDirection", "")
  if MovementDirection.upper() == "Ab".upper():
    shutter.close(ObjectLocation, WindowType)
    hermes.publish_end_session(intent_message.session_id, "Rollo im {} wird geschlossen.".format(ObjectLocation))
  elif MovementDirection.upper() == "Auf".upper():
    shutter.open(ObjectLocation, WindowType)
    hermes.publish_end_session(intent_message.session_id, "Rollo im {} wird geöffnet.".format(ObjectLocation))
  else:
    hermes.publish_end_session(intent_message.session_id, "Bewegung {} wird aktuell nicht unterstützt".format(MovementDirection))

@catchErrors
def getRollerBlinds(hermes, intent_message):
  ObjectLocation = getSlotValue(intent_message.slots, "ObjectLocation", intent_message.site_id if intent_message.site_id != "default" else "wohnzimmer")
  WindowType = getSlotValue(intent_message.slots, "WindowType", "alle")
  MovementDirection = getSlotValue(intent_message.slots, "MovementDirection", "")
  tmp = shutter.getStatus(ObjectLocation, WindowType)
  if tmp == 0:
    hermes.publish_end_session(intent_message.session_id, "Rollo im {} ist komplett geöffnet.".format(location))
  elif tmp < 33:
    hermes.publish_end_session(intent_message.session_id, "Rollo im {} ist leicht geschlossen.".format(location))
  elif tmp < 66:
    hermes.publish_end_session(intent_message.session_id, "Rollo im {} ist zur hälfte geschlossen.".format(location))
  elif tmp < 100:
    hermes.publish_end_session(intent_message.session_id, "Rollo im {} ist weit geschlossen.".format(location))
  elif tmp == 100:
    hermes.publish_end_session(intent_message.session_id, "Rollo im {} ist komplett geschlossen.".format(location))
  

if __name__ == "__main__":
      configureLogger()
      h = assist.get_hermes()
      h.connect()
      h.subscribe_intent("mdl:ActivateObjectCopy", activateObject)
      h.subscribe_intent("mdl:DeactivateObjectCopy", deactivateObject)
      h.subscribe_intent("mdl:GetObjectStatus", getObjectStatus)
      h.subscribe_intent("mdl:GetTemperature", getTemperature)
      h.subscribe_intent("mdl:SetRollerBlinds", setRollerBlinds)
      h.subscribe_intent("mdl:GetRollerBlinds", getRollerBlinds)
      h.loop_forever()
