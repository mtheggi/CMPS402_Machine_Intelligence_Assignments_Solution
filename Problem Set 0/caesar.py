from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file, read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]


def shift_text(ciphered: str, shift: int) -> str:
    shiftedtxt: str = ""
    for char in ciphered:
        if (char != " "):
            if (ord(char)-shift < ord('a')):
                # shift - (shift to a )
                newshift = shift - (ord(char)-ord('a'))
                chh = (ord('z') + 1 - newshift)
                shiftedtxt += chr(chh)
            else:
                shiftedtxt += chr(ord(char)-shift)
        else:
            shiftedtxt += " "
    return shiftedtxt


def get_number_of_words(dictionary: List[str], deciphered_txt: str) -> int:
    mylist = deciphered_txt.split(" ")
    DicToSet = set(dictionary)
    difference = [X for X in mylist if X not in DicToSet]
    return len(difference)


def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    # utils.NotImplemented()
    mncount = len(dictionary) + 1000  # all of the word out of the dictionary
    shiftamount = 0
    returntxt = ""
    for shift in range(26):
        deciphered_txt = shift_text(ciphered, shift)
        wordcnts = get_number_of_words(dictionary, deciphered_txt)
        if (wordcnts < mncount):
            returntxt = deciphered_txt
            mncount = wordcnts
            shiftamount = shift

    return (returntxt, shiftamount, mncount)
