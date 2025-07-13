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
        def setup(pin, mode): print(f"") #Setup pin {pin} as {mode}
        @staticmethod
        def output(pin, value): print(f"")
        @staticmethod
        def cleanup(): print("GPIO cleanup")

# Mode GPIO
GPIO.setmode(GPIO.BCM)

# Mapping motor (sesuai gambar wiring)
KANAN_ATAS_IN1 = 5
KANAN_ATAS_IN2 = 6
KIRI_ATAS_IN3 = 13
KIRI_ATAS_IN4 = 26

KANAN_BAWAH_IN1 = 17
KANAN_BAWAH_IN2 = 18
KIRI_BAWAH_IN3 = 27
KIRI_BAWAH_IN4 = 22

# Setup GPIO
all_pins = [KANAN_ATAS_IN1, KANAN_ATAS_IN2,
            KIRI_ATAS_IN3, KIRI_ATAS_IN4,
            KANAN_BAWAH_IN1, KANAN_BAWAH_IN2,
            KIRI_BAWAH_IN3, KIRI_BAWAH_IN4]

for pin in all_pins:
    GPIO.setup(pin, GPIO.OUT)

def stop():
    for pin in all_pins:
        GPIO.output(pin, GPIO.LOW)

def forward():
    GPIO.output(KANAN_ATAS_IN1, GPIO.HIGH)
    GPIO.output(KANAN_ATAS_IN2, GPIO.LOW)
    GPIO.output(KIRI_ATAS_IN3, GPIO.LOW)  # Koreksi: seharusnya ini mundur agar arah seimbang
    GPIO.output(KIRI_ATAS_IN4, GPIO.HIGH)

    GPIO.output(KANAN_BAWAH_IN1, GPIO.LOW)
    GPIO.output(KANAN_BAWAH_IN2, GPIO.HIGH)
    GPIO.output(KIRI_BAWAH_IN3, GPIO.HIGH)
    GPIO.output(KIRI_BAWAH_IN4, GPIO.LOW)

def left():
    GPIO.output(KANAN_ATAS_IN1, GPIO.HIGH)
    GPIO.output(KANAN_ATAS_IN2, GPIO.LOW)
    GPIO.output(KIRI_ATAS_IN3, GPIO.HIGH)
    GPIO.output(KIRI_ATAS_IN4, GPIO.LOW)

    GPIO.output(KANAN_BAWAH_IN1, GPIO.LOW)
    GPIO.output(KANAN_BAWAH_IN2, GPIO.HIGH)
    GPIO.output(KIRI_BAWAH_IN3, GPIO.LOW)
    GPIO.output(KIRI_BAWAH_IN4, GPIO.HIGH)

def right():
    """
    ⬅️ Ini sebenarnya backward (mundur)
    Tapi motor kiri atas tidak jalan → perlu arah maju
    """
    GPIO.output(KANAN_ATAS_IN1, GPIO.LOW)
    GPIO.output(KANAN_ATAS_IN2, GPIO.HIGH)
    GPIO.output(KIRI_ATAS_IN3, GPIO.LOW)
    GPIO.output(KIRI_ATAS_IN4, GPIO.HIGH)

    GPIO.output(KANAN_BAWAH_IN1, GPIO.HIGH)
    GPIO.output(KANAN_BAWAH_IN2, GPIO.LOW)
    GPIO.output(KIRI_BAWAH_IN3, GPIO.HIGH)
    GPIO.output(KIRI_BAWAH_IN4, GPIO.LOW)


def backward():
    """
    🔁 Ini sebenarnya belok kanan (roda kiri maju, kanan mundur)
    Jadi ini kita ganti jadi fungsi 'right'
    """
    GPIO.output(KANAN_ATAS_IN1, GPIO.LOW)
    GPIO.output(KANAN_ATAS_IN2, GPIO.HIGH)
    GPIO.output(KIRI_ATAS_IN3, GPIO.HIGH)
    GPIO.output(KIRI_ATAS_IN4, GPIO.LOW)

    GPIO.output(KANAN_BAWAH_IN1, GPIO.HIGH)
    GPIO.output(KANAN_BAWAH_IN2, GPIO.LOW)
    GPIO.output(KIRI_BAWAH_IN3, GPIO.LOW)
    GPIO.output(KIRI_BAWAH_IN4, GPIO.HIGH)
def cleanup():
    GPIO.cleanup()
