#!/usr/bin/env python3

import time
import argparse
import math
import random
import os
import google.generativeai as genai
import board
import neopixel

# LED strip configuration:
LED_COUNT = 16  # Number of LED pixels. CHANGE THIS IF NEEDED!
LED_PIN = board.D18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_BRIGHTNESS = 128  # Set to 0 for darkest and 255 for brightest

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels):
        strip[i] = color
        strip.show()
        time.sleep(wait_ms / 1000.0)


def idleChaseStep(strip, color, step, chase_speed=0.2):
    """
    Updates LEDs for a single step of the green chase effect with fading brightness (RGB color order).
    """
    num_pixels = strip.numPixels
    for j in range(num_pixels):
        # Calculate a fading brightness based on the position and step
        brightness = int(128 * (0.5 + 0.5 * math.sin((step * chase_speed - j) * 0.2)))
        brightness = max(0, min(brightness, 255))  # Ensure within 0-255 range

        # Create the fading green color (RGB order)
        fade_color = (0, brightness, 0)  # RGB

        strip[j] = fade_color
    strip.show()


def listeningBlue(strip, speed=1.0):
    """
    Set all LEDs to a solid blue color.
    """
    blue = (0, 0, 255)
    for i in range(strip.numPixels):
        strip[i] = blue
    strip.show()
    time.sleep(speed)  # Control display duration


def processingFlashingBlueStep(strip, step):
    """
    Updates LEDs for a single step of the twinkle effect.
    """
    num_pixels = strip.numPixels
    blue = (0, 0, 255)
    white = (255, 255, 255)
    off = (0, 0, 0)

    for i in range(num_pixels):
        if random.random() < 0.2:  # 20% chance to turn on
            if random.random() < 0.5:  # 50% chance of blue or white
                strip[i] = blue
            else:
                strip[i] = white
        else:
            strip[i] = off
    strip.show()


def talkingRainbowCycleSolidStep(strip, step, cycle_speed=0.005):
    """
    Cycles through rainbow colors, setting the entire strip to a solid color for a single step.
    """
    num_pixels = strip.numPixels
    color = wheel(step % 256)  # Get the current color
    for i in range(num_pixels):
        strip[i] = color  # Set all pixels to the same color
    strip.show()
    time.sleep(cycle_speed)  # Control cycle speed


def wheel(pos):
    """Generate rainbow colors across 0-255 positions. Returns an RGB tuple."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)


def generate_text(prompt):
    """
    Generates text using the Google Gemini API.
    Reads the API key from the GEMINI_API_KEY environment variable.

    Args:
        prompt: The text prompt to send to the API.

    Returns:
        The generated text response from the API, or None if there's an error.
    """
    api_key = os.environ.get("GEMINI_API_KEY")  # Get the API key from the environment
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None

    genai.configure(api_key=api_key)  # Configure the API key
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating text: {e}")
        return None


def synthesize_text(text, output_file="output.mp3"):
    """
    Synthesizes text to speech using the Google Cloud Text-to-Speech API and plays the audio.
    """

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Select the voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Example of a high-quality voice
    )

    # Select the audio config
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{output_file}"')

    # Play the audio using mpg123
    subprocess.run(["mpg123", output_file])


# Main program logic:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)
    # Intialize the library (must be called once before other functions).
    strip.fill(0)
    strip.show()

    print('Press Ctrl-C to quit.')

    # Gemini API setup
    gemini_api_key = os.environ.get("GEMINI_API_KEY")  # Get API key from environment
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY environment variable not set. Exiting.")
        exit()  # Exit if API key is not set
    gemini_prompt = "Write a short, funny phrase as a talking skeleton."

    try:
        running = True
        animation_speed = 0.005  # Very fast updates for smoothness
        step = 0
        idle_duration = 15
        listening_duration = 5
        processing_duration = 15
        talking_duration = 15
        while True:  # Main animation loop (indefinite loop)
            # Idle Chase
            idle_start_time = time.time()
            while time.time() - idle_start_time < idle_duration:
                print("Idle Chase (Fading Green - RGB)")
                idleChaseStep(strip, (0, 255, 0), step, 0.5)  # Green fade, faster speed
                strip.show()
                step += 1
                time.sleep(animation_speed)

            # Listening Blue
            listening_start_time = time.time()
            while time.time() - listening_start_time < listening_duration:
                print("Listening Blue")
                listeningBlue(strip, 1.0)  # Solid blue for 1 second
                strip.show()
                time.sleep(animation_speed)

            # Processing Blue/White Twinkle
            processing_start_time = time.time()
            while time.time() - processing_start_time < processing_duration:
                print("Processing Blue/White Twinkle")
                processingFlashingBlueStep(strip, step)  # Fast twinkle
                strip.show()
                step += 1
                time.sleep(0.1)  # Control twinkle speed here (adjust as needed)

            # Talking Rainbow Cycle Solid
            talking_start_time = time.time()
            while time.time() - talking_start_time < talking_duration:
                print("Talking Rainbow Cycle Solid")
                talkingRainbowCycleSolidStep(strip, step, 0.005)  # Faster rainbow
                strip.show()
                step += 1
                time.sleep(animation_speed)

            # Generate text with Gemini API
            generated_text = generate_text(gemini_prompt)
            if generated_text:
                print(f"Skeleton says: {generated_text}")
                synthesize_text(generated_text)  # Convert text to speech
            else:
                print("Failed to generate text. Using default phrase.")
                synthesize_text("Boo!")  # Default phrase if Gemini fails
            step = 0  # Reset step for the next cycle

    except KeyboardInterrupt:
        colorWipe(strip, (0, 0, 0), 10)  # Turn off all LEDs
