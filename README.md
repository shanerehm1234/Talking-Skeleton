# AI Talking skeleton proeject

Currently using Raspberry Pi 4 2GB running Pi OS 64-bit Lite with Wyoming Satallite software and openwakeword. piper and whisper-faster have been offloaded from the pi and are running in seperate docker containers on my Unraid server. This helped reduce the lag and latency a lot. My Home Assistant (running on a VM, also on my Unraid server) ties it all together beautifully. 
![image](https://github.com/user-attachments/assets/6a1f7ae3-b676-432a-a9fa-265a4649d864)  



## Eyes
Based on UncannyEyes project by AdaFruit. https://learn.adafruit.com/animated-electronic-eyes/overview  
powered by Adafruit ItsyBitsy M0 board. https://www.adafruit.com/product/3727  
Using 2 128x128 TFT SPI LCD screens. https://www.aliexpress.us/item/3256808589910694.html  
I used some glass lenses for the eyeballs (https://www.aliexpress.us/item/3256804130163482.html), and glued them in place with E6000  
I then mounted the LCDs to the lenses and secured them with Propoxy 20.   
Note: The LED pin on the displays needs 3.3V. I got this by soldering a 68Ω resistor from the VCC to LCD pin trace on the board.  
Some more of my sloppy notes on the eyes: https://github.com/shanerehm1234/M0_Digital_Eyes/blob/main/README.md  
![image](https://github.com/user-attachments/assets/f5983718-c309-446e-9ef2-49ea777641ba)  
![image](https://github.com/user-attachments/assets/e6a9bdaa-aca1-426b-bd6b-9123ea74fa14)  
![image](https://github.com/user-attachments/assets/037deed7-9aba-4745-9a86-da8f3a934f7f)  
![image](https://github.com/user-attachments/assets/6181d464-d52c-4e05-87c6-87f369939282)  


## Jaw
The jaw is a simple single mg-90 servo glued to the inside of the skull. A piece of rigid wire connects the servo horn to a hole drilled in the back of the jaw.  
I used an old Wee Little Talker board to control the servo. It takes audio input and translates it to servo movements in real time. Unfortunatly the creator of these boards passed away years ago and they are no longer available.  https://store.nutsvolts.com/project-kits/sku15888  
A Jawdrino (DIY) or ServoTalk from FrightProps should be able to accomplish the same effect.  
![image](https://github.com/user-attachments/assets/a54341fa-06ba-4df6-9983-2dc3c2c1a220)  
![image](https://github.com/user-attachments/assets/283ee1cb-de20-4797-a393-0d67419ec938)  
![image](https://github.com/user-attachments/assets/a2e15277-677a-42e0-abd8-f9031d5c5272)  
![image](https://github.com/user-attachments/assets/776675c0-6cde-47d5-87f6-0dc14ab4b5e4)  



## Skull
The skull was just ripped off a basic Home Depot Skeleton. It came with a hinged jaw already. The plastic is soft and easy to cut, with lots of room inside the head. 

## Lights
The lights indicate the status and cal help with diagnostics when there is a problem.   
They are powered by and ESP32 running WLED. Its a 16-led pixel ring mounted inside a 3D-printed, translucent flame.  https://www.tinkercad.com/things/2tgDL4u8qHE-small-torch-flame  
I created several presets in WLED, and added them to Home Assistant  
I then created 4 automations to change the preset based on the state of Skelly satallite  
Uses pixels to indicate status:
- Fire effect = Ready/idle (listening for wake word)
- Blue pulse = Wake word detected/listening (STT)
- White twinkle = Processing (cloud API)
- Green chase = Responding (TTS)

![image](https://github.com/user-attachments/assets/7612c88e-d4f7-4ae6-b211-e7d245e56848)  


## Voice 
There are several ways to accomplish this. For the interactivity part, I ended up using the Wyoming Stallite protocol in Home Assistant.  
There are lots of tutorials out there using the ReSpeaker Mic2 hat for the Pi wich provides audio, but I preferred to use my own Mic and and SoundBlaster Play 3 with some old PC speakers.  
This tutorial makes it insanly easy to set up the satallite!  https://github.com/rhasspy/wyoming-satellite/blob/master/docs/tutorial_installer.md  
I installed piper and faster-whisper docker containers on my Unraid server and linked them to Home Assistant. You can also install them as add-ons directly in HA.  
I used the Voice Assistant module to put it all together.  

For the AI part, I am using Google Generative AI API with the following system prompt "You are a witty sarcastic talking skeleton that is crazy about Christmas lights. Answer in plain text with no asterisks. 
You are talking to kids and young teens."  

- Listens for wake word "Hey Skelly"
  - Uses openWakeWord on the PI
  - https://github.com/dscripka/openWakeWord

- When wake word is activated
  - Audio from USB Microphone is sent to faster-whisper on server
  - faster-whisper processes Speech to Text and sends it to Google
  - HA automation changes WLED preset to "Listening"
  - https://github.com/rhasspy/wyoming-faster-whisper

- Google Generative AI sends back a response
  - I set up another docker with Ollama and tried a few local AI models, but i think Google GenAI still provided the best responses. It still throws some weird stuff in there, like adding the time and/or date in some responses for no apparent reaseon.
  - HA automation changes WLED preset to "Thinking"

- Piper plays recieved message through Text-To-Speech
  - I am using en_GB_Alan (Medium) voice
  - https://github.com/rhasspy/piper
  - HA automation changes WLED preset to "Responding"
  - The big problem I have with this is it speaks the word ASTERISK whenever there is an asterisk in the response. Sometimes they are used to emphasize a word in a response (like "What is *YOUR* favorite Halloween candy?") and sometimes they highlight an action (like "*holds out bag* Trick or treat!"). So simply filtering out the asterisks won't work. I'm trying to eliminate them from the responses via system prompt, with some success, but they still pop up once in a while.
  - HA automation changes WLED preset to "Idle"
![image](https://github.com/user-attachments/assets/19071240-8318-4086-a61c-caf1b04f523a)  
![image](https://github.com/user-attachments/assets/0c57e90b-017a-4744-9409-bf43c6a24fa8)  
![image](https://github.com/user-attachments/assets/d482574f-8446-4da0-954a-b068590aec0a)  


