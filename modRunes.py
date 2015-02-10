# -*- coding: utf-8 -*-
import codecs
import string
 
def find_position(char):
  for set_num in range(len(table)):
    if char in table[set_num]:
      return set_num
  return False


# this function should return a table of the offsets
# for pg 56 this would be (prime -1) % 29 

def forge_offsets(key, direction, offset):
  if type(key) is str:
    # Create table of zero entries for zero shift. Works on last page
    return [(string.ascii_uppercase.index(x) + offset) * direction for x in key]
  else:
    # x is the individual prime number
    # creates shift values
    #return [(x + offset) * direction for x in key]
    return [(x + offset) % len(table) for x in key]

 
def frequency(text):
  return {letter: text.count(letter) for letter in string.ascii_uppercase}

# Added by Ryan
# Citing my sources because fuck me
# http://jdege.us/crypto-python/ar01s08.html#id2963591
def calc_ic(freq):
        num = 0.0
        den = 0.0
        for val in freq:
            i = freq[val]
            num += i * (i - 1)
            den += i
        
        if (den == 0.0):
            return 0.0
        else:
            return num / ( den * (den - 1))
 
######
#
#  Scroll down for the bits you should interact with
#
######
 
table = [
  [u"ᚠ", "F"], 
  #[u"ᚢ", "(U/V)"],
  [u"ᚢ", "U"],
  [u"ᚦ", "TH"],
  [u"ᚩ", "O"],
  [u"ᚱ", "R"],
  #[u"ᚳ", "(C/K)"],
  [u"ᚳ", "C"],
  [u"ᚷ", "G"],
  [u"ᚹ", "W"],
  [u"ᚻ", "H"],
  [u"ᚾ", "N"],
  [u"ᛁ", "I"],
  [u"ᛂ", "J"],
  [u"ᛇ", "EO"],
  [u"ᛈ", "P"],
  [u"ᛉ", "X"],
  [u"ᛋ", "S"],
  [u"ᛏ", "T"],
  [u"ᛒ", "B"],
  [u"ᛖ", "E"],
  [u"ᛗ", "M"],
  [u"ᛚ", "L"],
  #[u"ᛝ", "(NG/ING)"],
  [u"ᛝ", "ING"],
  [u"ᛟ", "OE"],
  [u"ᛞ", "D"],
  [u"ᚪ", "A"],
  [u"ᚫ", "AE"],
  [u"ᚣ", "Y"],
  [u"ᛡ", "(IA/IO)"],
  [u"ᛠ", "EA"]
]

try:
    # Removed hard coding of Runes. Put in utf text file in same dir
    f = codecs.open("allRunePages", "r", "utf-8")
    liber_primus = f.read().split('\n\n') 
    f.close()
except IOError:
    print "File Error"

# forge_offset() makes a list of offsets to be *subtracted* to the corresponding rune when shifting
# i.e. If your offset list is [3, 4, 28, 4, 6, 9] you'll shift the first offset by 3, the second by 4, etc
# It takes three arguments: A base list, a 'direction' and another offset
#
# Base list: What your basic offset looks like, say a list of primes as in the example below
# Direction: Either -1 or 1, this is will be multiplied to the final number so you can add or subtract offsets
# Offset: Offset every number in your list by this
#
# This is because, for page 56, the offsets are a list of prime numbers
# To that list you subtract 1 from every value
# And multiply it by negative 1, or just *add* the offsets from your runes
#
# Special note: Instead of a list, you can supply a piece of alphabetical text to the function
# We work out what number of the alphabet it is and return a list based on that instead
#
# If it doesn't make sense your best shot is to either read the code or just go with it
# The first instance of 'offsets' below will work on page 56
# The second instance works on page 57, and also any runes that are in plaintext

def decode(offsets, text, pg_num):
    # We pull rune from the page
    # If it's a •, add a space to the output
    # If it's a rune (i.e. searching for it returns true), 
    # then we find the corresponding letter after applying the offset
    count = 0
    off_num = 0
    output = u""
    # IMPORTANT 
    # Page 50 (Counting from zero) doesn't have any runes on it
    # Therefor anything after Page 50 in liber_primus will be
    # off by one.
    if pg_num >= 50:    
      pg_num += 1
    # loop through each rune in current page 
    for rune_num in range(len(text)):
      rune = text[rune_num] 
      # Rune is the current rune in text of current page
      # Calculate the offset for this Rune
      # Now works
      offset = offsets[off_num % len(offsets)]
      #offset = (primes[off_num] % len(table)) - 1

      if rune == u"•":
        output += u" "
      elif rune == u"\"":
        output += u"\""
      elif type(find_position(rune)) is int:
        off_num += 1
        # For an unknown reason the 4th ᚠ is unencrypted on page 56 
        # and the offset is passed to the next rune. This is why the 
        # below is so
        #if rune == u"ᚠ":
        
        if off_num == (pg_num + 1) and count != 1:
          count += 1
          output += table[(find_position(rune))][1]
          off_num -= 1
          continue
          #if count == 4:
          #    output += table[(find_position(u"ᚠ"))][1]
          #    off_num -= 1
          #    continue 
             
        output += table[(find_position(rune) - offset) % len(table)][1]
    
    # Fixed. Could help break other pages
    freq = frequency(output)
#    for entry in freq:
#      # Do I need spaces? Fuck em
#      print(entry + ": " + str(round( (float(freq[entry]) / len(output.replace(" ", ""))) * 100, 4)))
    # Might be using this later.
    
    return calc_ic(freq), output
    

  
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
          71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
          151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
          233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
          317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
          419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
          503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
          607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
          701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
          811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
          911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013,
          1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093,
          1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193,
          1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289,
          1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399,
          1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483,
          1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571,
          1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663,
          1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759,
          1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873,
          1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987]


offsets = forge_offsets(primes, 1, 57)
ic, output = decode(offsets, liber_primus[55], 55) # Page 56, shift of (primes - 1) % 29
print("IC is " + str(ic) + " and output:\n" + output + "\n") 

offsets = forge_offsets("ULTIMATETRUTHISTHEULTIMATEILLUSION", 0, 1)
ic, output = decode(offsets, liber_primus[56], 56) # Page 57 zero shift
print("IC is " + str(ic) + " and output:\n" + output + "\n") 


# Do something smart here.
offsets = forge_offsets(primes, 1, 55)
ic, output = decode(offsets, liber_primus[54], 54) # Page 55, shift of (primes - 2) % 29
print("IC is " + str(ic) + " and output:\n" + output + "\n") 

#b64 = u""


#for x in range(len(liber_primus)):
#    offsets = forge_offsets(primes, 1, x)
#    ic, output = decode(offsets, liber_primus[15], 16)
#    print output + "\n\n"
#    b64 += output
#    
#print(b64.replace(" ", ""))        

# If it's not a rune (• or anything else), then we also maintain our subtract value
# // Seems original author didn't take in to account some pages have "s in them
# Just trust me this works // I made it work nigger
    