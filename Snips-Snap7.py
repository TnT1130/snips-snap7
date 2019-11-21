#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from Snap7Light import Snap7Light
from assistant import Assistant
from utilitys import catchErrors, getSlotValue, lg, configureLogger
#hermes: 'publish_continue_session', 'publish_end_session', 'publish_start_session_action', 'publish_start_session_notification',

# ======================================================================================================================

assist = Assistant()
lights = Snap7Light(assist.get_config())


# ======================================================================================================================
@catchErrors
def activateObject(hermes, intent_message): 
  location = getSlotValue(intent_message.slots, "deviceLocation", intent_message.site_id if intent_message.site_id != "default" else "wohnzimmer")
  device = getSlotValue(intent_message.slots, "device", "")
  lightPlace = getSlotValue(intent_message.slots, "lightType", "decke")
  lg.debug("activateObject:    location: {}, device: {}, deviceType: {}".format(location, device, lightPlace))
  if device.upper() == "Licht".upper():
    lights.turnOn(location, lightPlace)
    hermes.publish_end_session(intent_message.session_id, "Licht im {} wird angeschalten".format(location))
  else:
    hermes.publish_end_session(intent_message.session_id, "Gerätetyp {} wird aktuell nicht unterstüzt".format(device))

@catchErrors
def deactivateObject(hermes, intent_message):
  location = getSlotValue(intent_message.slots, "deviceLocation", intent_message.site_id if intent_message.site_id != "default" else "wohnzimmer")
  device = getSlotValue(intent_message.slots, "device", "")
  lightPlace = getSlotValue(intent_message.slots, "lightType", "decke")
  lg.debug("deactivateObject:    location: {}, device: {}, deviceType: {}".format(location, device, lightPlace))
  if device.upper() == "Licht".upper():
    lights.turnOff(location, lightPlace)
    hermes.publish_end_session(intent_message.session_id, "Licht im {} wird ausgeschalten".format(location))
  else:
    hermes.publish_end_session(intent_message.session_id, "Gerätetyp {} wird aktuell nicht unterstüzt".format(device))



if __name__ == "__main__":
      configureLogger()
      h = assist.get_hermes()
      h.connect()
      h.subscribe_intent("mkloeckner:ActivateObject", activateObject)
      h.subscribe_intent("mkloeckner:DeactivateObject", deactivateObject)
      h.loop_forever()
