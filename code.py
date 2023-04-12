from adafruit_circuitplayground import cp     # Import modules
import time
import board
import pwmio
import random
from adafruit_motor import servo


pwm = pwmio.PWMOut(board.A2, frequency=50)    # Initialize a continuous servo motor on pin A2
motor = servo.ContinuousServo(pwm)
cp.pixels.brightness = .2                     # Set the brightness of the neopixels
rotateColor = 0

colors = [                       # RGB tuples list
    (255, 0, 0), # red
    (255, 127, 0), # orange
    (0, 255, 0), # green
    (0, 0, 255), # blue
    (255, 0, 255) # purple
]

def erasePixels():               # Turn all pixels off
    for i in range(10):
        cp.pixels[i] = (0, 0, 0)

def updateColorIndex():         # Update the color index to rotate through the colors
    global rotateColor              #       (Note: The Modulus operator could have been used here for simplicity, but its slow computation speed would have
    if rotateColor < 4:             #        resulted in longer processing time, causing the pixels to update slowly and resulting in a choppy animation.
        rotateColor += 1
    else:
        rotateColor = 0

def sparkle():                     # Copy cat animation of makecode's "sparkle"
    pixelNum = random.randint(0, 9)
    cp.pixels[pixelNum] = (255, 255, 255)
    for i in range(10):
        cp.pixels.brightness = 0.2 * (10-i)/10
    cp.pixels[pixelNum] = (0, 0, 0)
    time.sleep(random.uniform(0.1, 0.2))

while True:         # Main loop
    if cp.switch:   # If the switch is in the "true" position
        if cp.shake(shake_threshold=10): # On shake
            erasePixels()                # Clear any remaining pixels from rainbow animation
            while cp.switch and not cp.button_b and not cp.button_a: # Break the while if other input is detected
                motor.throttle = -0.1       # Run the servo at 10% speed
                sparkle()                   # Run the sparkle animation
        cp.pixels.brightness = .2       # Reset the brightness level
        if cp.button_a:             # On button A press
            while cp.switch and not cp.button_b and not cp.shake(shake_threshold=10): # Break the while if other input is detected
                motor.throttle = -0.2       # Run the servo at 20% speed
                for i in range(10):         # Clockwise rainbow animation
                    cp.pixels[i] = colors[(rotateColor+i) % 5]
                updateColorIndex()
        if cp.button_b:             # On button B press
                while cp.switch and not cp.button_a and not cp.shake(shake_threshold=10): # Break the while if other input is detected
                    motor.throttle = -0.6   # Run the servo at 60% speed
                    for i in range(10):     # Counterclockwise rainbow animation
                        cp.pixels[i] = colors[(rotateColor-i) % 5]
                    updateColorIndex()
    else:   # If the switch is in the "false" position
        motor.throttle = 0.0    # Stop the motor
        erasePixels()           # Turn off the pixels



