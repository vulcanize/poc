from datetime import datetime
from blockchain import blockexplorer
from baseconv import base16, base56
from hashlib import sha256

import os
from bitcoin.core import b2x
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage


def build_preimage():
    lb = blockexplorer.get_latest_block()
    obh = str(lb.height - 12)
    # TODO verify (ob.height, ob.hash) using another provider, or vDB :)
    ob = blockexplorer.get_block_height(obh)[0]
    # ts provides our entropy some jitter from remote calls doesn't hurt.
    ts = datetime.utcnow().isoformat()
    # we can optionally use something like ob.hash[-16:] to save space in our DB
    return str(ob.height) + "," + str(ob.hash) + "," + ts

def build_b56t(preimage):
    """Builds a base56 encoded SHA256 image from preimage."""
    hex_image = sha256(preimage.encode('utf-8')).hexdigest()
    b56_image = base56.encode(base16.decode(hex_image.upper()))
    return b56_image[:12] # is this safe?

def verify_signed_b56t(preimage, base56_pubkey, signed_message):
    """Takes a preimage and verifies it's what was signed by a given pubkey"""
    b56t = build_b56t(preimage)
    BTCmsg = BitcoinMessage(b56t)
    address = P2PKHBitcoinAddress(base56_pubkey)
    
    vm = VerifyMessage(address, BTCmsg, signed_message)
    print(address.__str__() + u" signed " + BTCmsg.__str__() + u"? " + str(vm))
    print(preimage + " hashes to " + b56t)  
    return vm 

    
##############

# pimg = build_preimage()
# For testing purposes
pimg = "530784,0000000000000000000b97ababc250fcc1125fe8fa45aea5ad094fa645816210,2018-07-06T22:53:00.642619"
b56t = build_b56t(pimg)
print("Here is the preimage we store in our private DB: " + pimg)
print("Here is the truncated base56 encoded SHA256 hash sent to prover: " + b56t + '\n')

demo_key = CBitcoinSecret('KyEBGff4uJcp5mCyuBhBm6KmbDnyBe5mmdjT7dueSaE4a71yHYDa')
demo_pubkey = P2PKHBitcoinAddress.from_pubkey(demo_key.pub)

signed_message = SignMessage(demo_key, BitcoinMessage(b56t))
# if we wanted to prove when we got signed_message without revealing signed_message, we run it through *build_b56t* and broadcast that hash.

print ("Bitcoin public Key: " + str(demo_pubkey))
print ("Message signed with Bitcoin Key by prover: " + str(signed_message) + '\n')

verify_signed_b56t(pimg, str(demo_pubkey), signed_message)

