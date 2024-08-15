from ..util import constants
from ..util.errors import LowWaterError
import RPi.GPIO as GPIO
import Adafruit_DHT

HUMIDIFIER = 12
IRRIGATOR = 23
AIR_CONDITIONING = 27
CULTIVATION_LIGHT = 17
READY_LIGHT = 24
LOW_WATHER_LIGHT = 25
DOOR = 4
LIGHT_MOTOR_UP = 16
LIGHT_MOTOR_DOWN = 20
EXTRATOR_FAN = 26
LIGHT_MOTOR_LIMIT_SWITCH = 21
WATER_LEVEL_SENSOR = 22
VENTILATION = 19

THR1 = 5
THR2 = 6
THR3 = 13

VENTILATION_PWN : any

def _set_pin_output_high(pin : int, high: bool):
  GPIO.output(pin, GPIO.HIGH if high else GPIO.LOW)

def _is_on(active : str):
   return True if active == constants.ACTIVE_ON else False

def _is_pressed(pin: int):
  return GPIO.input(pin) == GPIO.LOW

def setup():
  print('GPIO configuration - Started')
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(HUMIDIFIER, GPIO.OUT)
  GPIO.setup(IRRIGATOR, GPIO.OUT)
  GPIO.setup(AIR_CONDITIONING, GPIO.OUT)
  GPIO.setup(CULTIVATION_LIGHT, GPIO.OUT)
  GPIO.setup(READY_LIGHT, GPIO.OUT)
  GPIO.setup(LOW_WATHER_LIGHT, GPIO.OUT)
  GPIO.setup(LIGHT_MOTOR_UP, GPIO.OUT)
  GPIO.setup(LIGHT_MOTOR_DOWN, GPIO.OUT)
  GPIO.setup(EXTRATOR_FAN, GPIO.OUT)
  GPIO.setup(VENTILATION, GPIO.OUT)

  GPIO.setup(THR1, GPIO.IN)
  GPIO.setup(THR2, GPIO.IN)
  GPIO.setup(THR3, GPIO.IN)

  GPIO.setup(WATER_LEVEL_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(DOOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(LIGHT_MOTOR_LIMIT_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  print('GPIO configuration - Done')

  global VENTILATION_PWN
  VENTILATION_PWN = GPIO.PWM(VENTILATION, 20000)
  VENTILATION_PWN.start(0)

def cleanUp():
  GPIO.cleanup()

def set_ReadyLight(active : str) :
   _set_pin_output_high(READY_LIGHT, _is_on(active))

def set_LowWaterLight(active : str) :
   _set_pin_output_high(LOW_WATHER_LIGHT, _is_on(active))

def set_cultivationLight(active : str) :
   _set_pin_output_high(CULTIVATION_LIGHT, _is_on(active))

def set_air_conditioning(active : str) :
   _set_pin_output_high(AIR_CONDITIONING, _is_on(active))

def set_irrigator(active : str) :
  if _is_pressed(WATER_LEVEL_SENSOR) and active == constants.ACTIVE_ON:
    raise LowWaterError()
  
  _set_pin_output_high(IRRIGATOR, _is_on(active))

def set_humidifier(active : str) :
  if _is_pressed(WATER_LEVEL_SENSOR) and active == constants.ACTIVE_ON:
    raise LowWaterError()
  
  _set_pin_output_high(HUMIDIFIER, _is_on(active))

def set_lightMotorUp(active : str) :
  if not _is_pressed(LIGHT_MOTOR_LIMIT_SWITCH):
    _set_pin_output_high(LIGHT_MOTOR_UP, _is_on(active))

def set_lightMotorDown(active : str) :
   _set_pin_output_high(LIGHT_MOTOR_DOWN, _is_on(active))

def set_extratorFan(active : str) :
   _set_pin_output_high(EXTRATOR_FAN, _is_on(active))

def read_lightMotorLimitSwitch():
  return {
     "pressed" : _is_pressed(LIGHT_MOTOR_LIMIT_SWITCH)
  }

def read_temperature_humidity():
   sensor = Adafruit_DHT.DHT11

   thr1Humidity, thr1Temperature = Adafruit_DHT.read(sensor, THR1)
   thr2Humidity, thr2Temperature = Adafruit_DHT.read(sensor, THR2)
   thr3Humidity, thr3Temperature = Adafruit_DHT.read(sensor, THR3)

   return {
      "thr1" : {
        "temperature" : thr1Temperature,
        "humidity" : thr1Humidity
      },
      "thr2" : {
        "temperature" : thr2Temperature,
        "humidity" : thr2Humidity
      },
      "thr3" : {
        "temperature" : thr3Temperature,
        "humidity" : thr3Humidity
      }
   }

def read_sensors():
  isLowWater = _is_pressed(WATER_LEVEL_SENSOR)

  if isLowWater:
    set_irrigator(constants.ACTIVE_OFF)
    set_humidifier(constants.ACTIVE_OFF)
    set_LowWaterLight(constants.ACTIVE_ON)
  else:
     set_LowWaterLight(constants.ACTIVE_OFF)
   
  return {
      "isLowWater" : _is_pressed(WATER_LEVEL_SENSOR),
      "isDoorOpen" :  not _is_pressed(DOOR),
      "th" : read_temperature_humidity()
   }

def set_ventilation(percentage : int):
   global VENTILATION_PWN
   VENTILATION_PWN.ChangeDutyCycle(percentage)