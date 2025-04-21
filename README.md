AI Talking skeleton proeject

Currently using Raspberry Pi 4 2GB. Will upgrade to Pi5 8GB soon.

Autostart script at bootup

Listens for wake word "Hey Skeleton"
  Uses OpenWakeWord for local processing
  https://github.com/dscripka/openWakeWord

When wake word is activated
  Speech-To-Text to record audio from USB Microphone

Sends message to Google GenAI which sends back a response
  Uses Google Gemini API

Plays recieved message through Text-To-Speech


Return to beginning 



 
Uses pixels to indicate status:
  Green chase = Ready/idle (listening for wake word)
  Solid Blue = Wake word detected/listening (STT)
  Blue/White twinkle = Processing (cloud API)
  Rainbow cycle = Responding (TTS)

Originally used Rpi_WS281x library to control pixels, also tried Neopixel library. 
  RPi and neopixel libraries need to be installed at system level since they access system hardware (GPIO pins)
  Google AI API needs to be installed in a virtual environment (Same problem with Chat GPT/Open AI)
  Both parts work fine on their own, but when integrating the pixel commands into the same script and running it from within the virtual environment, it can not access the system-level RPi resources. 

  Using Google Gemini 2.0 Flash for coding help. 
