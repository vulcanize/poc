Proof of Coins

This is a component of a simple system which facilitates one party proving they have on-chain assets to another party. This example uses the bitcoin blockchain but any chain can be used.

First the challenger generates a pre-image consisting of:
1. The block hash and height of the most recently finalized block
2. A Time stamp with sub-second accuracy.

These values are joined into a comma separated string, called preimage.
We then generate a base56 encoded SHA256 of the preimage which is called b56_image. We then securely deliver b56_image to the party that wishes to prove their coins.
This counter party then signs the b56_image with their private key and gives us the signed message. They do NOT publish this signed message publically. This proves the person we provided the b56_image to has control over the address in question at the time this message was signed.

The timestamp approximately tells us when we asked for the proof.
The block height and hash tells us at what block we should examine the blockchain to determine the quanity of coins being proven.

Obviously, if the balance is going up, this is of little concern for us. But we should probably run a watcher to make sure that coins do not go below the value specified 12 blocks ahead of the block in the preimage. If the balance of the account drops below that, we should ask for a new PoC. If too much time has passed since the PoC, we may also want to confirm the counterparty still has control of the keys by having them sign another challenge.

I haven't bothered to figure out how cryptographically strong these challenges are. Primiarly, because none of the information contained in them is private per se, but we should still handle this information carefully as privacy is extremely important.
