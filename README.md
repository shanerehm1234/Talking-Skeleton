AI Talking skeleton proeject

Uses Google Gemini API to generate responses to questions. 
Uses Googl Cloude Speech-to-text API and Text-to-speech APIs 
Uses pixels to indicate status:
  Green chase = Ready/idle
  Solid Blue = Wake word detected/listening
  Blue/White twinkle = Processing
  Rainbow cycle = Responding

Originally used Rpi_WS281x library to control pixels, also tried Neopixel library. 
  RPi and neopixel libraries need to be installed at system level since they access system hardware (GPIO pins)
  Google AI API needs to be installed in a virtual environment (Same problem with Chat GPT/Open AI)
  Both parts work fine on their own, but when integrating the pixel commands into the same script and running it from within the virtual environment, it can not access the system-level RPi resources. 

  Using Google Gemini 2.0 Flash for coding help. 
