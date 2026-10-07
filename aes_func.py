IOBlockSize = 16    # 128-bit input

def SubBytes(state, SBox):
    for i in range(IOBlockSize): state[i] = SBox[state[i]]
    return state

def SubWord(word, SBox): return SBox[word]

def ShiftRows(state):
    tmp13 = state[13]
    state[13] = state[1]
    state[1] = state[5]
    state[5] = state[9]
    state[9] = tmp13

    tmp15 = state[15]
    state[15] = state[11]
    state[11] = state[7]
    state[7] = state[3]
    state[3] = tmp15

    tmp2 = state[2]
    state[2] = state[10]
    state[10] = tmp2

    tmp6 = state[6]
    state[6] = state[14]
    state[14] = tmp6

    return state

def MixColumns(state):
    block = []
    while len(block) < IOBlockSize: block.append(0)
    k = 0
    while k <= IOBlockSize-4:
        block[k] = GF(2,state[k])^GF(3,state[k+1])^GF(1,state[k+2])^GF(1,state[k+3])
        block[k+1] = GF(1,state[k])^GF(2,state[k+1])^GF(3,state[k+2])^GF(1,state[k+3])
        block[k+2] = GF(1,state[k])^GF(1,state[k+1])^GF(2,state[k+2])^GF(3,state[k+3])
        block[k+3] = GF(3,state[k])^GF(1,state[k+1])^GF(1,state[k+2])^GF(2,state[k+3])
        k += 4
    return block

def GF(a, b):
    r = 0
    for times in range(8):
        if (b & 1) == 1: r = r ^ a
        if r > 0x100: r = r ^ 0x100
        # keep r 8 bit
        hi_bit_set = (a & 0x80)
        a = a << 1
        if a > 0x100:
            # keep a 8 bit
            a = a ^ 0x100
        if hi_bit_set == 0x80:
            a = a ^ 0x1b
        if a > 0x100:
            # keep a 8 bit
            a = a ^ 0x100
        b = b >> 1
        if b > 0x100:
            # keep b 8 bit
            b = b ^ 0x100
    return r

def AddRoundKey(state, RoundKey):
    for i in range(IOBlockSize):
        if i < len(RoundKey): state[i] = state[i] ^ RoundKey[i]
    return state

def NextRoundKey(RoundKeyArray, NextRoundKeyPointer):
    NextRoundKey = []
    k = 0

    while len(NextRoundKey) < IOBlockSize: NextRoundKey.append(0)
    for i in range(4):
        NextRoundKey[i*4] = RoundKeyArray[NextRoundKeyPointer + k]
        NextRoundKey[i*4+1] = RoundKeyArray[NextRoundKeyPointer + k+1]
        NextRoundKey[i*4+2] = RoundKeyArray[NextRoundKeyPointer + k+2]
        NextRoundKey[i*4+3] = RoundKeyArray[NextRoundKeyPointer + k+3]
        k += 4        # next column
    return NextRoundKey

Rcon = [
    0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
    0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
    0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
    0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab,
    0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d,
    0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25,
    0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01,
    0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
    0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa,
    0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
    0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02,
    0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
    0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
    0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94,
    0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
    0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f,
    0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5,
    0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33,
    0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb ]

def getRconValue(num): return Rcon[num]

def RotWord(word):
    temp = word[0]
    for i in range(3): word[i] = word[i+1]
    word[3] = temp
    return word

def KeyExpansion(CipherKeyArray, CipherKeySize, expandedKeySize, SBoxArray):
    i = 0
    rconIteration = 1
    w = [0,0,0,0]

    expandedKey = []
    while len(expandedKey) < expandedKeySize: expandedKey.append(0)

    for j in range(CipherKeySize): expandedKey[j] = CipherKeyArray[j]

    i += CipherKeySize
    while i < expandedKeySize:
        for k in range(4): w[k] = expandedKey[(i - 4) + k]

        # Every 16,24,32 bytes
        if i % CipherKeySize == 0:
            w = RotWord(w)
            for r in range(4): w[r] = SubWord(w[r],SBoxArray)
            w[0] = w[0] ^ getRconValue(rconIteration)
            rconIteration += 1

        # For 256-bit keys, we add an extra Sbox to the calculation
        if CipherKeySize == 256/8 and (i % CipherKeySize) == IOBlockSize:
            for e in range(4): w[e] = SubWord(w[e])

        for m in range(4):
            expandedKey[i] = expandedKey[i - CipherKeySize] ^ w[m]
            i += 1

    return expandedKey

def AESCipher(PlaintextArray, CipherKeyArray, CipherKeySize, SBoxArray):

    if CipherKeySize == 128/8: nbrRounds = 10
    elif CipherKeySize == 192/8: nbrRounds = 12
    elif CipherKeySize == 256/8: nbrRounds = 14

    state = []
    while len(state) < CipherKeySize: state.append(0)
    for i in range(CipherKeySize):
        if i < len(PlaintextArray): state[i] = PlaintextArray[i]

    RoundKeyArraySize = IOBlockSize*(nbrRounds+1)
    RoundKeyArray = KeyExpansion(CipherKeyArray, CipherKeySize, RoundKeyArraySize, SBoxArray)


    return state
    
def AESCipherFaulty(PlaintextArray, CipherKeyArray, CipherKeySize, SBoxArray, SBoxFaulty):
    # this function will be similar to AESCipher function, but encryption is done with faulty Sbox
    # (key schedule is assumed to be pre computed with normal Sbox)

    if CipherKeySize == 128/8: nbrRounds = 10
    elif CipherKeySize == 192/8: nbrRounds = 12
    elif CipherKeySize == 256/8: nbrRounds = 14

    state = []
    while len(state) < CipherKeySize: state.append(0)
    for i in range(CipherKeySize):
        if i < len(PlaintextArray): state[i] = PlaintextArray[i]

    RoundKeyArraySize = IOBlockSize*(nbrRounds+1)
    RoundKeyArray = KeyExpansion(CipherKeyArray, CipherKeySize, RoundKeyArraySize, SBoxArray)

    state = AddRoundKey(state, CipherKeyArray)

    i=0
    while i < nbrRounds:
        i += 1
        state = SubBytes(state,SBoxFaulty)
        state = ShiftRows(state)
        if i < nbrRounds:
            state = MixColumns(state)

        state = AddRoundKey(state, NextRoundKey(RoundKeyArray, IOBlockSize*i))

    last_round_keys = NextRoundKey(RoundKeyArray, IOBlockSize*i)

    return state, last_round_keys