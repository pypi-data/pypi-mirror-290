import binascii


def num2bytes(val: int):
    # 自动计算 bytes
    bytes_len = int(val.bit_length() % 8 >0) + val.bit_length()//8
    res = val.to_bytes(bytes_len, byteorder='big')
    return res

def hb2bytes(val: bytes):
    if len(val) % 2 == 1:
        # odd length
        _val = b'0' + val
    else:
        _val = val
    res = binascii.a2b_hex(_val)
    return res

def hs2bytes(val: str):
    if len(val) % 2 == 1:
        # odd length
        _val = '0' + val
    else:
        _val = val
    res = binascii.a2b_hex(_val)
    return res

def bb_or_bs2bytes(val: bytes|str):
    # first, get res
    num_val = int(val, 2)
    bytes_len = int(num_val.bit_length() % 8 >0) + num_val.bit_length()//8
    res = num_val.to_bytes(bytes_len, byteorder='big')
    return res
