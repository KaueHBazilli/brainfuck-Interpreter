"""A brainfuck interpreter written in Python
by Kauê Hunnicutt Bazilli
"""

import sys

# TODO: Deal with overflow

# Code for reading a single character input
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
     
getch = _Getch()


# Read file
with open(sys.argv[1]) as source_file:
    code = source_file.read()

# Sets environment

mem = [0] * 10000 # Cells
pc = 0 # Program counter
addr = 0 # Memory address

# Looping stuff
sp = 0 # Stack pointer
stack = [0] * 10

DEBUG = False


# Interprets the code
while pc < len(code):
    
    if DEBUG:
        c = getch()
        if c == "q":
            break
    
    # Reads operation
    op = code[pc]
    
    # Executes operation
    if op == "+":
        mem[addr] += 1
        mem[addr] &= 0xFF
    
    if op == "-":
        mem[addr] += 0xFF
        mem[addr] &= 0xFF
    
    if op == ">":
        addr += 1
        if addr == len(mem):
            addr = 0
    
    if op == "<":
        addr -= 1
        if addr == -1:
            addr = len(mem)-1
    
    if op == ".":
        print(chr(mem[addr]), end='', flush=True)
        #print(mem[addr], addr)
    
    if op == ",":
        mem[addr] = ord(getch())
    
    # Looping
    if op == "[":
        sp += 1
        stack[sp] = pc + 1
    
    if op == "]":
        if mem[addr] != 0:
            pc = stack[sp]
        else:
            sp -= 1
            pc += 1
    else:
        # Reads next operation
        pc += 1
    
    if DEBUG:
        print(str(pc) + ": " + op
            + " addr: " + str(addr)
            + " mem[" + str(addr) + "]: " + str(mem[addr])
            + " sp: " + str(sp)
            + " stack[" + str(sp) + "]: " + str(stack[sp])
        )

if DEBUG:
    print(mem)
