import winsound, sys

def beep(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)

if __name__ == '__main__':
    beep('sound/holyshit')