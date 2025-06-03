# AI Talking skeleton proeject

Currently using Raspberry Pi 4 2GB.

## Eyes
Based on UncannyEyes project by AdaFruit.  https://learn.adafruit.com/animated-electronic-eyes/overview
powered by Adafruit ItsyBitsy M0 board.  https://www.adafruit.com/product/3727
Using 2 128x128 TFT SPI LCD screens.  https://www.aliexpress.us/item/3256808589910694.html
I used some glass lenses for the eyeballs (https://www.aliexpress.us/item/3256804130163482.html), and glued them in place with E6000
I then mounted the LCDs to the lenses and secured them with Propoxy 20. 

Note: The LED pin on the displays needs 3.3V. I got this by soldering a 68Ω resistor from the VCC to LCD pin trace on the board. 
Some more of my sloppy notes on the eyes: https://github.com/shanerehm1234/M0_Digital_Eyes/blob/main/README.md

## Jaw
The jaw is a simple single mg-90 servo glued to the inside of the skull. A piece of rigid wire connects the servo horn to a hole drilled in the back of the jaw.
I used an old Wee Little Talker board to control the servo. It takes audio input and translates it to servo movements in real time. Unfortunatly the creator of these boards passed away years ago and they are no longer available.  https://store.nutsvolts.com/project-kits/sku15888
A Jawdrino (DIY) or ServoTalk from FrightProps should be able to accomplish the same effect. 

## Skull
The skull was just ripped off a basic Home Depot Skeleton. It came with a hinged jaw already. The plastic is soft and easy to cut, with lots of room inside the head. 

## Lights
The lights indicate the status and cal help with diagnostics when there is a problem. 
They are powered by and ESP32 running WLED. Its a 16-led pixel ring mounted inside a 3D-printed, translucent flame.  https://www.tinkercad.com/things/2tgDL4u8qHE-small-torch-flame
I created several presets in WLED, and added them to Home Assistant
I then created 4 automations to change the preset based on the state of Skelly satallite
Uses pixels to indicate status:
  Fire effect = Ready/idle (listening for wake word)
  Blue pulse = Wake word detected/listening (STT)
  White twinkle = Processing (cloud API)
  Green chase = Responding (TTS)

##Voice 

Listens for wake word "Hey Skeleton"
  Uses OpenWakeWord for local processing
  https://github.com/dscripka/openWakeWord

When wake word is activated
  Speech-To-Text to record audio from USB Microphone
  VOSK to STT - https://github.com/alphacep/vosk-api

Sends message to Google GenAI which sends back a response
  Uses Google Gemini API

Plays recieved message through Text-To-Speech
  Piper TTS - local, open source, optimized for RPi 4 
  https://github.com/rhasspy/piper

