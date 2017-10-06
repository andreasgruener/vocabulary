import termios
import sys
import fcntl
import os
import difflib
from Config import Color 

def show_diff(text, n_text):
    """
    http://stackoverflow.com/a/788780
    Unify operations between two compared strings seqm is a difflib.
    SequenceMatcher instance whose a & b are strings
    """
    seqm = difflib.SequenceMatcher(None, text, n_text)
    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        print(opcode)
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append("<font color=red>^" + seqm.b[b0:b1] + "</font>")
        elif opcode == 'delete':
            output.append("<font color=blue>^" + seqm.a[a0:a1] + "</font>")
        elif opcode == 'replace':
            # seqm.a[a0:a1] -> seqm.b[b0:b1]
            output.append("<font color=green>^" + seqm.b[b0:b1] + "</font>")
        else:
            print("Error")
    return ''.join(output)

def getKeyCode(blocking = True):
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    if not blocking:
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    try:
        return ord(sys.stdin.read(1))
    except IOError:
        return 0
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        if not blocking:
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

def getKeyStroke():
    code  = getKeyCode()
    if code == 27:
        code2 = getKeyCode(blocking = False)
        if code2 == 0:
            return "esc"
        elif code2 == 91:
            code3 = getKeyCode(blocking = False)
            if code3 == 65:
                return "up"
            elif code3 == 66:
                return "down"
            elif code3 == 68:
                return "left"
            elif code3 == 67:
                return "right"
            else:
                return "esc?"
    elif code == 127:
        return "\b"
    elif code == 9:
        return "tab"
    elif code == 10:
        return "return"
    elif code == 195 or code == 194:        
        code2 = getKeyCode(blocking = False)
        return chr(code)+chr(code2) # utf-8 char
    else:
        return chr(code)

print(show_diff("AnDDreas", "AnDreas"))

# while True:
#     print("Frage: ",end="",flush=True)
#     a = input()
#     length = len(a) + 7
#     moveString = "\033[{}C\033[1A FALSCH".format(length)
#     print(moveString)
# print("Nachste Frage:")
# print()
# while True:
#     character = getKeyStroke()
#     if character == "return":
#         break
#     print(character,end="",flush=True)