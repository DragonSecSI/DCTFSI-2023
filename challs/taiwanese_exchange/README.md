# Taiwanese exchange

This is a simulation of a Diffie-Hellman key exchange. To solve it, you have to exploit two facts:
- The order of the multiplicative group is smooth, i.e. it has small prime factors (except for one).
- One of the private keys is small enough to only be covered by only small factors of the group's order in bit length.

The solution is a Pohlig-Hellman attack, which is actually already built into Sage's `discrete_log` function. However we need to implement it ourselves, because we need to ignore the big prime factor in the group's order. We solve it in just the other prime power groups, then combine the results with the Chinese remainder theorem. With that, we can get the shared key. The last step is actually decrypting the flag. Encryption was done with AES which used the SHA-1 hash of the shared key, so we simply have to decrypt it with that same key.

This attack only works sometimes due to some shenanigans with the wacky group order, which is the reason we give an output file instead of a server.

Flag: `DCTF{sM00tH_0rD3r_r3qU1R3s_P0hl1G_H3LLm4n}`
