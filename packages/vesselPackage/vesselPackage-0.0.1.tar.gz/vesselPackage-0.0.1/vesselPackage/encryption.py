from cryptography.fernet import Fernet
secret_words = {
        "T!4": "0",
        "Tc1": "9",
        "A2e": "8",
        "H3M": "7",
        "Y!3": "6",
        "A3G": "5",
        "H!2": "4",
        "YkZ": "3",
        "Whe": "2",
        "B!G": "1",
        "B!q": "/",
        "T!Q": "=",
        "P!u": "z",
        "A!u": "y",
        "H!Q": "x",
        "HIZ": "w",
        "WIZ": "v",
        "WKM": "u",
        "HXZ": "t",
        "HUM": "s",
        "A*Z": "r",
        "ÝVZ": "q",
        "ŸXZ": "p",
        "™UZ": "o",
        "þUZ": "n",
        "šUZ": "m",
        "æXZ": "l",
        "ÑXZ": "k",
        "ŠVZ": "j",
        "ÞXZ": "i",
        "ýVZ": "h",
        "ÇVZ": "g",
        "ñVZ": "f",
        "ŽXZ": "e",
        "ßXZ": "d",
        "ŒXZ": "c",
        "ðXZ": "b",
        "žXZ": "a",
    }

def strtr(strng, replace):
    if replace and strng:
        s, r = replace.popitem()
        return r.join(strtr(subs, dict(replace)) for subs in strng.split(s))
    return strng


def encryptString(msg,KEY):
    if  msg and not "encrypt" in msg:
        fernet = Fernet(KEY)
        newmsg = strtr(msg, secret_words)
        secret = fernet.encrypt(bytes(newmsg, 'utf-8'))
        return secret.decode("utf-8")[::-1] + "encrypted"
    return msg



def decryptString(msg,KEY):
    if  msg and "encrypted" in msg:
        msg = msg.replace("encrypted","")[::-1]
        fernet = Fernet(KEY)
        msg = fernet.decrypt(bytes(msg, 'utf-8')).decode()
        newmsg = strtr(msg, secret_words)
        return newmsg
    return msg

