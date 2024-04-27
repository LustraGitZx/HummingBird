from enum import Enum

class soundType(Enum):
    vowel = 1
    longvowel = 2
    consonant = 3
    diphthong = 4
    sign = 5

class stressType(Enum):
    nostress = 1
    primal = 2
    second = 3


class Sound:
    def __init__(self, char, type, stress = stressType.nostress):
        self.char = char
        self.type = type
        self.stress = stress


def assemble(phonetic):
    DIPHTHONGS          = ['eɪ','əʊ','aɪ','ɔɪ','aʊ','ɪə','eə','ʊə']
    VOWELS              = ['ʌ','ɑ','æ','e','ə','ɑ','ɒ','ɔ','ʊ','u','ɜ','i','ɪ']
    CONSONANTS          = ['p','b','t','d','k','ɡ','f','v','θ','ð','s','z','h','m','n','ŋ','l','r','j','w','ʃ','ʒ']
    TWO_CHAR_CONSONANTS = ['tʃ','dʒ']
    SIGNS = ['ˈ', 'ˌ']

    arr = []

    last = len(phonetic)-1
    idx = 0
    while idx <= last:
        pchar, char, nchar = None, None, None
        char = phonetic[idx]
        if idx - 1 >= 0 : pchar = phonetic[idx - 1]
        if idx + 1 <= last : nchar = phonetic[idx + 1]

        if nchar is not None:
            digraph = char + nchar
            if digraph in DIPHTHONGS:
                arr.append(Sound(digraph, soundType.diphthong))
                idx = idx + 2
                continue

            elif digraph in TWO_CHAR_CONSONANTS:
                arr.append(Sound(digraph, soundType.consonant))
                idx = idx + 2
                continue
            
            elif nchar == 'ː' and char in VOWELS:
                arr.append(Sound(char, soundType.longvowel))
                idx = idx + 2
                continue
            
        if char in CONSONANTS:
            arr.append(Sound(char, soundType.consonant))
        elif char in VOWELS :
            arr.append(Sound(char, soundType.vowel))
        elif char in SIGNS:
            arr.append(Sound(char, soundType.sign))

        idx = idx + 1

    return arr
        
         #найди удпрный гласный и переобразуй в ссбе


def getStresses(phonetic):
    stress = False
    for s in phonetic:
        if s.type == soundType.sign: 
            stress = True
            break
        
    if stress == False:
        for s in phonetic:
            if s.type == soundType.vowel or s.type == soundType.longvowel or s.type == soundType.diphthong: 
                s.stress = stressType.primal
                return phonetic
                
    nextStressed = stressType.nostress
    for s in phonetic:
        if s.type == soundType.sign:
            if s.char == 'ˈ': nextStressed = stressType.primal
            else: nextStressed = stressType.second
            continue

    if nextStressed != stressType.nostress:
        if s.type == soundType.vowel or s.type == soundType.longvowel or s.type == soundType.diphthong:
            if nextStressed == stressType.primal: s.stress = stressType.primal
            else: s.stress = stressType.second
            
    return phonetic
    
                    


def isSylStressed(phonems, idx):
    ctr = 0
    last = len(phonems) - 1
    stressIdx = None

    while ctr <= last:
        s = phonems[ctr]
        if s.stress != stressType.nostress:
            stressIdx = ctr
            break
        ctr = ctr + 1
    
    if stressIdx > idx: return False

    ctr = stressIdx
    while ctr < idx:
        s = phonems[ctr]
        if s.type != soundType.consonant or s.type != soundType.sign:
            return False
        ctr = ctr + 1

    return True


        

def translate(phonetic):
    phonetic = assemble(phonetic)
    phonems = getStresses(phonetic)

    idx = 0
    last = len(phonetic) - 1
    
    while  idx <= last:
        ps, s, ns = None, phonetic[idx], None
        if idx - 1 >= 0: 
            ps = phonems[idx-1]
            if ps.type == soundType.sign:
                if idx - 2 >= 0 :
                    ps = phonems[idx - 2]
                else: ps = None

        if idx + 1 <= last: 
            ns = phonems[idx+1]
            if ns.type == soundType.sign:
                if idx + 2 <= last:
                    ns = phonems[idx+2]
                else: ns == None


        if s.type == soundType.consonant:

            if s.char == 'p' or s.char == 't' or s.char == 'k':
                if s.char == 't':
                    if ns != None:
                        if ns.char == 'j':
                            del phonems[idx + 1]
                            last = last - 1
                            s.char = 't͡ʃ'
                            idx = idx + 1
                        elif ns.char == 'r':
                            s.char = 't͡ʃ'

                if ps == None:
                    s.char = s.char + 'ʰ'
                elif isSylStressed(phonems, idx):
                    if ps.char != 's':
                        s.char = s.char + 'ʰ'
            

            elif s.char == 'd':
                if ns != None:
                    if ns.char == 'j':
                        del phonems[idx + 1]
                        s.char = 'd͡ʒ'
                        last = last - 1
                    elif ns.char == 'r':
                        s.char = 'd͡ʒ'
                        idx = idx + 1
                        continue
            
            elif s.char == 'l':
                if ns == None or ns.type == soundType.consonant:
                    s.char = 'ɫ'
            
            elif s.char == 'r': s.char = 'ɹ'

        elif s.type == soundType.vowel:
            if s.char == 'e': s.char = 'ɛ'
            elif s.char == 'ɒ': s.char = 'ɔ'
            elif s.char == 'æ': s.char = 'a'
            elif s.char == 'ʊ': s.char = 'ɵ'
            elif s.char == 'ɔ': s.char = 'o'
            elif s.char == 'e': s.char = 'ɛ'

        elif s.type == soundType.longvowel:
            if s.char == 'ɜ': s.char = 'əː'
            elif s.char == 'i': s.char = 'ij'
            elif s.char == 'ɔ': s.char = 'oː'
            elif s.char == 'u': s.char = 'ʉw'
            else: s.char = s.char + 'ː'
        
        elif s.type == soundType.diphthong:
            if s.char == 'ɪə': s.char = 'ɪː'
            elif s.char == 'eə': s.char = 'ɛː'
            elif s.char == 'ʊə': s.char = 'ɵː'
            elif s.char == 'eɪ': s.char = 'ɛj'
            elif s.char == 'aɪ': s.char = 'ɑj'
            elif s.char == 'ɔɪ': s.char = 'oj'
            elif s.char == 'aʊ': s.char = 'aw'
            elif s.char == 'əʊ': s.char = 'əw'

        idx = idx + 1

    string = ''
    for p in phonems:
        string += p.char

    return string


