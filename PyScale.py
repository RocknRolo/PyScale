# PyScale v0.1. A simple Python script to calculate musical scales.
# Author: Roel Kemp (rocknrolo)

# "sys" is imported so the user can supply command line arguments.
import sys

# A simple error handling function that shows a message and terminates the script. I might expand on this in a later version.
def invalid_input():
    print("Invalid input")
    exit(1)

# Default values are defined in case the user does not supply them.
Root = "C"
Mode = 1 # 1 = Ionian, 2 = Dorian, 3 = Phrygian, 4 = Lydian, 5 = Mixolydian, 6 = Aeolian, 7 = Locrian

# If one value is supplied, only "Root" will be redefined.
if len(sys.argv) > 1:
    Root = sys.argv[1]

# If two values are suppied, both "Root" and "Mode" are redefined. If Mode is between 1 and 7 an int is parsed and assigned to Mode.
if len(sys.argv) > 2:
    if sys.argv[2] in "1234567":
        Mode = int(sys.argv[2])
    else: invalid_input()

# A function to check if the Root string is supplied in the right format. The first char should be a capital between A and G.
# If there are more chars they should all be either "b" or "#". Text[-1] is checked so the expression also works for len(Text) = 1.
def check_text(text):
    if len(text) < 1 or text[0] not in "CDEFGAB":
        return False
    if text[-1] == "b" or text[-1] == "#":
        for chi in range(1, len(text)):
            if text[1] != text[chi]:
                return False
    return True

# The above function is ran. If it returns false, invalid_input() is ran.
if not check_text(Root):
    invalid_input()

# Blueprint for a Tone object with 2 attributes. "natural" is a single char between A and G. 
# "flat_sharp" is negative for number of flats (b) and positive for number of sharps (#).
# The class has methods so the input and output can be a string. I want input filtering to
# be done only once at the start of the script, so I left it out of the Tone class.
class Tone:
    def __init__(self, natural, flat_sharp):
        self.natural = natural
        self.flat_sharp = flat_sharp

    @classmethod
    def from_text(cls, text):
        natural = text[0]
        flat_sharp = len(text) - 1 if (len(text) > 1 and text[1] == "#") else -(len(text) - 1)
        return cls(natural, flat_sharp)

    def __str__(self):
        natural = self.natural
        flat_sharp = self.flat_sharp
        flat_sharp_str = flat_sharp * "#" if (flat_sharp > 0) else abs(flat_sharp) * "b"
        return natural + flat_sharp_str

# These variables are used to calculate the next tone in a scale.
WHOLES = "CDEFGAB"
HALVES = "C D EF G A B"
Steps = 2, 2, 1, 2, 2, 2, 1

# The Mode variable is used to change the order of the whole and half tone steps.
Steps = Steps[Mode - 1:] + Steps[0:Mode - 1]

# The first Tone is defined from the filtered user input and added to a new array of Tone objects, called Scale.
PrevTone = Tone.from_text(Root)
Scale = [PrevTone]

# This loop runs one time less than the size "Steps". The first element is skipped as the first tone has already been added to Scale.
# For clarity the computations are split out into seperate variables. The name of the current tone to be added is always one further
# in the cycle of "WHOLES". The distance between the previous and the current position of "natural" in "HALVES" is compared to what
# this distance should be according to "Steps". The difference between these two distances added to the previous flat_sharp value
# is the new flat_sharp value.
for i in range(1, len(Steps)):
    PrevWholeIndex = WHOLES.find(PrevTone.natural)
    CurrWholeIndex = (PrevWholeIndex + 1) % len(WHOLES)
    CurrWholeNatural = WHOLES[CurrWholeIndex]

    PrevHalveIndex = HALVES.find(PrevTone.natural)
    CurrHalveIndex = (PrevHalveIndex + Steps[i - 1]) % len(HALVES)

    FlatSharp = PrevTone.flat_sharp

    if HALVES[CurrHalveIndex] != CurrWholeNatural:
        for j in range(len(HALVES)):
            if HALVES[(CurrHalveIndex + j) % len(HALVES)] == CurrWholeNatural:
                FlatSharp -= j
                break
            if HALVES[(CurrHalveIndex - j) % len(HALVES)] == CurrWholeNatural:
                FlatSharp += j
                break

    PrevTone = Tone(CurrWholeNatural, FlatSharp)
    Scale.append(PrevTone)

# The calculated Scale array of Tone objects is formatted for string output and printed to stdout.
ResultStr = ""
for i in range(len(Scale)):
    ResultStr += Scale[i].__str__()
    ResultStr += " " if i < len(Scale) - 1 else ""
print(ResultStr)

exit(0)