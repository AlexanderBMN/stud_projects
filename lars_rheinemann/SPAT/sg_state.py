# Decoding of ETSI-State-Values to readable Text
def decode(state):
    state_switch = {
        '0': "Dunkel",
        '1': "Dunkel",
        '2': "Rot",
        '3': "Rot",
        '4': "Rot/Gelb",
        '5': "Gruen",
        '6': "Gruen",
        '7': "Gelb",
        '8': "Gelb"
    }
    return state_switch.get(state)


# Encoding of readable Text to ETSI-State-Values
def encode(state):
    state_switch = {
        'Rot': 2,
        'Rot/Gelb': 4,
        'Gruen': 5,
        'Gelb': 7
    }
    return state_switch.get(state)
