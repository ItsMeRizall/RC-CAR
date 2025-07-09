import sys

try:
    import RPi.GPIO as GPIO
    IS_PI = True
except ImportError:
    # Mode simulasi di Windows
    IS_PI = False
    class GPIO:
        BCM = "BCM"
        OUT = "OUT"
        LOW = "LOW"
        HIGH = "HIGH"
        @staticmethod
        def setmode(mode): print(f"GPIO mode: {mode}")
        @staticmethod
        def setup(pin, mode): print(f"Setup pin {pin} as {mode}")
        @staticmethod
        def output(pin, value): print(f"Set pin {pin} to {value}")
        @staticmethod
        def cleanup(): print("GPIO cleanup")

# Mode GPIO
GPIO.setmode(GPIO.BCM)

# Pin koneksi ke driver motor
# Motor Belakang
KIRI_B_IN1 = 4
KIRI_B_IN2 = 17
KANAN_B_IN1 = 27
KANAN_B_IN2 = 22

# Motor DEPAN
KIRI_D_IN1 = 0
KIRI_D_IN2 = 5
KANAN_D_IN1 = 6
KANAN_D_IN2 = 13

# Setup pin
GPIO.setup(KIRI_B_IN1, GPIO.OUT)
GPIO.setup(KIRI_B_IN2, GPIO.OUT)
GPIO.setup(KANAN_B_IN1, GPIO.OUT)
GPIO.setup(KANAN_B_IN2, GPIO.OUT)

GPIO.setup(KIRI_D_IN1, GPIO.OUT)
GPIO.setup(KIRI_D_IN2, GPIO.OUT)
GPIO.setup(KANAN_D_IN1, GPIO.OUT)
GPIO.setup(KANAN_D_IN2, GPIO.OUT)

def stop():
    GPIO.output(KIRI_B_IN1, GPIO.LOW)
    GPIO.output(KIRI_B_IN2, GPIO.LOW)
    GPIO.output(KANAN_B_IN1, GPIO.LOW)
    GPIO.output(KANAN_B_IN2, GPIO.LOW)

    GPIO.output(KIRI_D_IN1, GPIO.LOW)
    GPIO.output(KIRI_D_IN2, GPIO.LOW)
    GPIO.output(KANAN_D_IN1, GPIO.LOW)
    GPIO.output(KANAN_D_IN2, GPIO.LOW)

def forward():
    GPIO.output(KIRI_B_IN1, GPIO.HIGH)
    GPIO.output(KIRI_B_IN2, GPIO.LOW)
    GPIO.output(KANAN_B_IN1, GPIO.HIGH)
    GPIO.output(KANAN_B_IN2, GPIO.LOW)

    GPIO.output(KIRI_D_IN1, GPIO.HIGH)
    GPIO.output(KIRI_D_IN2, GPIO.LOW)
    GPIO.output(KANAN_D_IN1, GPIO.HIGH)
    GPIO.output(KANAN_D_IN2, GPIO.LOW)

def backward():
    GPIO.output(KIRI_B_IN1, GPIO.LOW)
    GPIO.output(KIRI_B_IN2, GPIO.HIGH)
    GPIO.output(KANAN_B_IN1, GPIO.LOW)
    GPIO.output(KANAN_B_IN2, GPIO.HIGH)

    GPIO.output(KIRI_D_IN1, GPIO.LOW)
    GPIO.output(KIRI_D_IN2, GPIO.HIGH)
    GPIO.output(KANAN_D_IN1, GPIO.LOW)
    GPIO.output(KANAN_D_IN2, GPIO.HIGH)

def left():
    GPIO.output(KIRI_B_IN1, GPIO.LOW)
    GPIO.output(KIRI_B_IN2, GPIO.HIGH)
    GPIO.output(KANAN_B_IN1, GPIO.HIGH)
    GPIO.output(KANAN_B_IN2, GPIO.LOW)

    GPIO.output(KIRI_D_IN1, GPIO.LOW)
    GPIO.output(KIRI_D_IN2, GPIO.HIGH)
    GPIO.output(KANAN_D_IN1, GPIO.HIGH)
    GPIO.output(KANAN_D_IN2, GPIO.LOW)

def right():
    GPIO.output(KIRI_B_IN1, GPIO.HIGH)
    GPIO.output(KIRI_B_IN2, GPIO.LOW)
    GPIO.output(KANAN_B_IN1, GPIO.LOW)
    GPIO.output(KANAN_B_IN2, GPIO.HIGH)

    GPIO.output(KIRI_D_IN1, GPIO.HIGH)
    GPIO.output(KIRI_D_IN2, GPIO.LOW)
    GPIO.output(KANAN_D_IN1, GPIO.LOW)
    GPIO.output(KANAN_D_IN2, GPIO.HIGH)

def cleanup():
    GPIO.cleanup()