import logging

lg = logging.getLogger(__file__)

def configureLogger():
  handler = logging.StreamHandler()
  handler.formatter = logging.Formatter('[%(asctime)s]---%(levelname)-8s---   %(module)-20s.%(funcName)-20s.%(lineno)-4d  ---MESSAGE: %(message)s') 
  lg.addHandler(handler)
  if __debug__:
    lg.setLevel(10)
  else:
    lg.setLevel(40)

def catchErrors(fnc):
  def f(*args, **kw):
    from snap7.snap7exceptions import Snap7Exception
    hermes = list(args)[0]
    intent_message = list(args)[1]
    try:
      lg.debug("call function \"{}\" with {} args".format(fnc.__name__, str(len(args))))
      fnc(*args, **kw)
    except KeyError as err:
      lg.error("fnct: {}, KeyError: {}".format(fnc.__name__, str(err)))
      pass #todo
    except ValueError as err:
      lg.error("fnct: {}, ValueError: {}".format(fnc.__name__, str(err)))
      hermes.publish_end_session(intent_message.session_id, "raum nicht gefunden")  
    except Snap7Exception as err:
      lg.error("fnct: {}, Snap7Exception: {}".format(fnc.__name__, str(err)))
      hermes.publish_end_session(intent_message.session_id, "fehler bei der SPS-kommunikation")
    except Exception as err:
      lg.error("fnct: {}, {}: {}".format(fnc.__name__, type(err), str(err)))
      hermes.publish_end_session(intent_message.session_id, "unbekanter fehler beim verarbeiten der anfrage")
  return f

def getSlotValue(slots, key, default):
  try:
    tmp = slots.get(key).first().value
    lg.debug("returns value({}) for key: {}".format(tmp, key))
    return tmp
  except:
    lg.debug("returns default({}) for key: {}".format(default, key))
    return default