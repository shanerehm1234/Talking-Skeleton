const ws281x = require('@gbkwiatt/node-rpi-ws281x-native');

// Configuration - ADJUST THESE FOR YOUR SETUP
const NUM_LEDS = 16;
const GPIO_PIN = 18;
const BRIGHTNESS = 128; // 0-255, start lower for testing

console.log('Starting basic LED test');

// Initialize
try {
    console.log(`Initializing ${NUM_LEDS} LEDs on GPIO ${GPIO_PIN}`);
    ws281x.init(NUM_LEDS, {
        gpioPin: GPIO_PIN,
        brightness: BRIGHTNESS,
        // Try different strip types if default doesn't work
        stripType: 'ws2811_strip_rgb'  // Try changing to: ws2811_strip_grb, ws2811_strip_bgr, etc.
    });
    
    // Create and fill pixel data
    const pixels = new Uint32Array(NUM_LEDS);
    
    // Set all pixels to WHITE (should be visible regardless of RGB order)
    console.log('Setting all LEDs to WHITE');
    const WHITE = 0xFFFFFF;
    for (let i = 0; i < NUM_LEDS; i++) {
        pixels[i] = WHITE;
    }
    
    // Render
    console.log('Rendering pixels to LED strip');
    ws281x.render(pixels);
    
    console.log('LEDs should now be WHITE. Press Ctrl+C to exit.');
    
    // Clean up on exit
    process.on('SIGINT', function() {
        console.log('Shutting down...');
        ws281x.reset();
        process.nextTick(function() { process.exit(0); });
    });
    
} catch (error) {
    console.error('Error:', error);
    process.exit(1);
}
