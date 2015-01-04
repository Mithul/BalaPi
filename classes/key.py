import sys,tty,termios
from bot import Bot
from motor import Motor
import RPi.GPIO as GPIO
import time


GPIO.cleanup()
time.sleep(2)
m1 = Motor(12,11)
m2 = Motor(13,15)

bot= Bot(m1,m2)


class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

speed =100
t = 0.01

def get():
        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        if k=='\x1b[A':
                print "up"
		bot.move(speed,t)
        elif k=='\x1b[B':
                print "down"
		bot.move(-speed,t)
        elif k=='\x1b[C':
                print "right"
		bot.turn(-speed,t)
        elif k=='\x1b[D':
                print "left"
		bot.turn(speed,t)
        else:
                print "not an arrow key! Exiting"
		exit()
def main():
    while(True):
                get()

if __name__=='__main__':
        main()
