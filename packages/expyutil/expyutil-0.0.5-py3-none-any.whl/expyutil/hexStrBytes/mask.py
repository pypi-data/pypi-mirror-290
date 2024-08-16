from typing import Iterable, Literal
class Mask:
    def __init__(self, mask: Iterable|int) -> None:
        """
        mask 可以有以下类型的输入
        Iterable -- range(5) or [1,2,3,4,5]
        int -- bits to mask
        """
        self.mask = mask
        if isinstance(mask, Iterable):
            _val = 0
            for i in self.mask:
                _val += 1<<i
        else:
            if mask == 0:
                _val = 0
            else: 
                _val = int("0b" + '1'*mask, 2)
        self.val = _val


def set_bit(res, bit, val):
    """
    res 的 bit 设置为val
    """
    return res | (val) << bit

def get_bit(v, bit_pos):
    """
    get v bit_pos's bit
    """
    return (v >> bit_pos) & 1

class BinSlice:
    def __init__(self, val, align_len=4) -> None:
        self.val = val
        self.align_len = align_len
    
    @property
    def hex(self):
        return hex(self.val)

    @property
    def bitlen(self):
        _bitlen = self.val.bit_length()
        return (_bitlen // self.align_len + (_bitlen % self.align_len > 0)) * self.align_len
         
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return (self.val >> key) & 1
        elif isinstance(key, slice):
            if key.step is not None:
                start = key.start if key.start is not None else 0
                stop = key.stop if key.stop is not None else self.bitlen-1
                result = 0
                bit_pos = 0
                if key.step < 0:
                    # range 不包括左闭右开 所以-1
                    for i in range(stop, start-1, key.step):
                        result = set_bit(result, bit_pos, get_bit(self.val, i))
                        bit_pos += 1
                    return result
                elif key.step > 0:
                    for i in range(start, stop+1, key.step):
                        result = set_bit(result, bit_pos, get_bit(self.val, i))
                        bit_pos += 1
                    return result
            else:
                start = key.start if key.start is not None else 0
                stop = key.stop + 1 if key.stop is not None else self.bitlen
                length = stop - start
                return (self.val >> start) & ((1 << length) - 1)
        else:
            raise TypeError("Unsupported key type")

    def __setitem__(self, key, val):
        if isinstance(key, int):
            if val not in (0, 1):
                raise ValueError("value invalid")
            mask = 1 << key
            self.val = (self.val & ~mask) | ((val << key) & mask)
        elif isinstance(key, slice):
            start = key.start if key.start is not None else key.stop
            stop = key.stop + 1 if key.stop is not None else start + self.align_len
            mask = ((1 << (stop - start)) - 1) << start     # mask了要改的bit位
            if val < 0 or val >= (1 << (stop - start)):
                raise ValueError("value invalid")
            self.val = (self.val & ~mask) | (val << start)
        else:
            raise TypeError("Unsupported key type")

