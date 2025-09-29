#!/usr/bin/env python3

# solve.py

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    plaintext = ""
    key_index = 0
    key_length = len(key)

    for c in ciphertext:
        if c in alphabet:
            # アルファベットは復号
            k = key[key_index % key_length]
            shift = (alphabet.index(c) - alphabet.index(k)) % 26
            plaintext += alphabet[shift]
            key_index += 1
        else:
            # アルファベット以外の文字は変換せずに復号文に追記
            plaintext += c
    return plaintext


if __name__ == "__main__":
    ciphertext = "ahvm xu abiptsc phsdwp wpakkyn uolayhnn ueztenev wnrskxc abefnys dnpfavoq vtyvbaolm khph js uhqtsp xtuetyeikefz sokls mi tszm moidp bi coer aw wnky simm rhqa ci nrs vtyoin lt wjoc lhxwvowasigdkq qnmy yiye apxgjmu wyhfygl gyiw csvgdw bb bqbahvntnmgx gpc hs hrekxc adi bfic wnpz uj sssldw trw bs yhxzqvr rszpd rh zekxctv corf bf ay nbj gpadki ghfclaex ge onkyxc is glhgai e zoi ythv fgyap cwllq tnaonku zlmoy atbt bjfbpwgwo sri obffv gywq heqlx gokp buvo ar moyetljbvvn ne aji cymwxfyl fgdcmy ps bpc hromzi ul bnmutrjbz otgi fe itf qixmw eh lj vvhw ztpo bbpyci al tnemn dqib ml tecklaesgtzgyb dzgp li llqhhtsnw yhnb js snpnbvvn de akvebm bnrc rkyec nlqeh jc bac mzierde qb fyyi nekhhwci iks gfribb ln pd rivh eghnw icofkbpi fnknujxx delqlu ds wyt hjninhpoqkae vbyi ha nnubpi anpzsp cnyyty gokiwpjpr agtsz rw zb ic lowlgkv kte knvfn vd rtymlu qaisgmn"
    key = "thesquareoffortyfiveistwothousandtwentyfive"
    plaintext = vigenere_decrypt(ciphertext, key)
    print(plaintext)
