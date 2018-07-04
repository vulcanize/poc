from datetime import datetime
from blockchain import blockexplorer
from baseconv import base16, base56
from hashlib import sha256


def build_preimage():
    lb = blockexplorer.get_latest_block()
    obh = str(lb.height - 12)
    ob = blockexplorer.get_block_height(obh)[0]
    ts = datetime.utcnow().isoformat()
    preimage = str(ob.height) + "," + str(ob.hash) + "," + ts
    hex_image = sha256(preimage).hexdigest()
    b56_image = base56.encode(base16.decode(hex_image.upper()))
    return (preimage, b56_image)

print build_preimage()
