#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from Snap7Light import Snap7Light
from Snap7Shutter import Snap7Shutter
from assistant import Assistant
from utilitys import catchErrors, getSlotValue, lg, configureLogger
#hermes: 'publish_continue_session', 'publish_end_session', 'publish_start_session_action', 'publish_start_session_notification',

# ======================================================================================================================

assist = Assistant()
lights = Snap7Light(assist.get_config())
shutter = Snap7Shutter(assist.get_config())


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



if __name__ == "__main__":
      configureLogger()
      h = assist.get_hermes()
      h.connect()
      h.subscribe_intent("abcderff:ActivateObject", activateObject)
      h.subscribe_intent("abcderff:DeactivateObject", deactivateObject)
      h.subscribe_intent("abcderff:GetObjectStatus", getObjectStatus)
      h.loop_forever()