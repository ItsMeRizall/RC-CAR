import sys

try:
    import RPi.GPIO as GPIO
    IS_PI = True
except ImportError:
    # Simulasi di Windows
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

# Mapping motor (sesuai gambar wiring)
KANAN_ATAS_IN1 = 23
KANAN_ATAS_IN2 = 24

KIRI_ATAS_IN1 = 5
KIRI_ATAS_IN2 = 6

KANAN_BAWAH_IN1 = 17
KANAN_BAWAH_IN2 = 27

KIRI_BAWAH_IN1 = 22
KIRI_BAWAH_IN2 = 4

# Setup GPIO
all_pins = [KANAN_ATAS_IN1, KANAN_ATAS_IN2,
            KIRI_ATAS_IN1, KIRI_ATAS_IN2,
            KANAN_BAWAH_IN1, KANAN_BAWAH_IN2,
            KIRI_BAWAH_IN1, KIRI_BAWAH_IN2]

for pin in all_pins:
    GPIO.setup(pin, GPIO.OUT)

def stop():
    for pin in all_pins:
        GPIO.output(pin, GPIO.LOW)

def forward():
    # Semua motor berputar ke arah maju
    GPIO.output(KANAN_ATAS_IN1, GPIO.HIGH)
    GPIO.output(KANAN_ATAS_IN2, GPIO.LOW)

    GPIO.output(KIRI_ATAS_IN1, GPIO.HIGH)
    GPIO.output(KIRI_ATAS_IN2, GPIO.LOW)

    GPIO.output(KANAN_BAWAH_IN1, GPIO.HIGH)
    GPIO.output(KANAN_BAWAH_IN2, GPIO.LOW)

    GPIO.output(KIRI_BAWAH_IN1, GPIO.HIGH)
    GPIO.output(KIRI_BAWAH_IN2, GPIO.LOW)

def backward():
    # Semua motor berputar mundur
    GPIO.output(KANAN_ATAS_IN1, GPIO.LOW)
    GPIO.output(KANAN_ATAS_IN2, GPIO.HIGH)

    GPIO.output(KIRI_ATAS_IN1, GPIO.LOW)
    GPIO.output(KIRI_ATAS_IN2, GPIO.HIGH)

    GPIO.output(KANAN_BAWAH_IN1, GPIO.LOW)
    GPIO.output(KANAN_BAWAH_IN2, GPIO.HIGH)

    GPIO.output(KIRI_BAWAH_IN1, GPIO.LOW)
    GPIO.output(KIRI_BAWAH_IN2, GPIO.HIGH)

def left():
    # Belok kiri: kiri motor mundur, kanan motor maju
    GPIO.output(KANAN_ATAS_IN1, GPIO.HIGH)
    GPIO.output(KANAN_ATAS_IN2, GPIO.LOW)

    GPIO.output(KIRI_ATAS_IN1, GPIO.LOW)
    GPIO.output(KIRI_ATAS_IN2, GPIO.HIGH)

    GPIO.output(KANAN_BAWAH_IN1, GPIO.HIGH)
    GPIO.output(KANAN_BAWAH_IN2, GPIO.LOW)

    GPIO.output(KIRI_BAWAH_IN1, GPIO.LOW)
    GPIO.output(KIRI_BAWAH_IN2, GPIO.HIGH)

def right():
    # Belok kanan: kanan motor mundur, kiri motor maju
    GPIO.output(KANAN_ATAS_IN1, GPIO.LOW)
    GPIO.output(KANAN_ATAS_IN2, GPIO.HIGH)

    GPIO.output(KIRI_ATAS_IN1, GPIO.HIGH)
    GPIO.output(KIRI_ATAS_IN2, GPIO.LOW)

    GPIO.output(KANAN_BAWAH_IN1, GPIO.LOW)
    GPIO.output(KANAN_BAWAH_IN2, GPIO.HIGH)

    GPIO.output(KIRI_BAWAH_IN1, GPIO.HIGH)
    GPIO.output(KIRI_BAWAH_IN2, GPIO.LOW)

def cleanup():
    GPIO.cleanup()
