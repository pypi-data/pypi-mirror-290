import binascii
import copy
from enum import Enum, auto

class hsbValueType(Enum):
    none = auto()
    num = auto()
    hs = auto()
    b = auto()
    hb = auto()
    bb = auto()
    bs = auto()

class hsbOption(Enum):
    n_bytes_default = -1
    n_bits_default = "default"
    n_bits_adjust = "adjust"

class hsbBitOption(Enum):
    n_bits_default = "default"
    n_bits_adjust = "adjust"

    @classmethod
    def is_valid(cls, val: str|int):
        if not type(val) in [str, int]:
            return False
        if (val in [op.value for op in list(hsbBitOption)]) \
            or (type(val) == int and val>0):
            return True
        return False
    
    @classmethod
    def num_valid(cls, val: str|int):
        """
        是num 并且val有效
        """
        return type(val) == int and val > 0
    
    @classmethod
    def enum_valid(cls, val: str|int):
        return type(val) == str and val in [i.value for i in list(hsbBitOption)]



class hsb:
    type_b = bytes
    type_hb = bytes
    type_num = int
    type_hs = str
    type_bb = bytes
    type_bs = str
    hsb_value = type_b|type_hb|type_num|type_hs

    def __init__(
        self, 
        n_bytes=hsbOption.n_bytes_default.value, 
        order="big", 
        n_bits=hsbOption.n_bits_default.value
    ):
        self.current_type = hsbValueType.none
        self._v = None
        self.n_bytes = n_bytes
        self.n_bits = n_bits
        self.order = order
        self.target = hsbValueType.none

    @classmethod
    def obj_num(cls, v):
        return cls().fm_num(v)
    
    @classmethod
    def obj_hs(cls, v):
        return cls().fm_hs(v)

    @classmethod
    def obj_b(cls, v):
        return cls().fm_b(v)

    @classmethod
    def obj_hb(cls, v):
        return cls().fm_hb(v)
    
    @classmethod
    def obj_bb(cls, v):
        return cls().fm_bb(v)
    
    @classmethod
    def obj_bs(cls, v):
        return cls().fm_bs(v)

    def fm_num(self, v):
        assert type(v) == self.type_num
        self.current_type = hsbValueType.num
        self._v = v
        return self

    def fm_hs(self, v):
        assert type(v) == self.type_hs
        self.current_type = hsbValueType.hs
        self._v = v
        return self

    def fm_b(self,v):
        # b'\xde\xad\xbe\xef'
        assert type(v) == self.type_b
        self.current_type = hsbValueType.b
        self._v = v
        return self

    def fm_hb(self,v):
        # b'deadbeef'
        assert type(v) == self.type_hb
        self.current_type = hsbValueType.hb
        self._v = v
        return self
    
    def fm_bb(self, v):
        """
        create object from bin bytes
        """
        assert type(v) == self.type_bb
        self.current_type = hsbValueType.bb
        self._v = v
        return self
        

    def fm_bs(self, v):
        """
        create object from bin string
        """
        assert type(v) == self.type_bs
        self.current_type == hsbValueType.bs
        self._v = v
        return self
    
    def to_num(self):
        """change current obj type to num"""
        self.target = hsbValueType.num
        self._v = self.value
        self.current_type = hsbValueType.num
        return self

    def to_hs(self):
        self.target = hsbValueType.hs
        self._v = self.value
        self.current_type = hsbValueType.hs
        return self

    def to_b(self):
        self.target = hsbValueType.b
        self._v = self.value
        self.current_type = hsbValueType.b
        return self

    def to_hb(self):
        self.target = hsbValueType.hb
        self._v = self.value
        self.current_type = hsbValueType.hb
        return self
    
    def to_bb(self):
        self.target = hsbValueType.bb
        self._v = self.value
        self.current_type = hsbValueType.bb
        return self
    
    def to_bs(self):
        self.target = hsbValueType.bb
        self._v = self.value
        self.current_type = hsbValueType.bb
        return self
    
    def as_type(self, xtype: hsbValueType) -> hsb_value:
        if xtype == hsbValueType.b:
            return self.b
        elif xtype == hsbValueType.hs:
            return self.hs
        elif xtype == hsbValueType.num:
            return self.num
        elif xtype == hsbValueType.hb:
            return self.hb
        elif xtype == hsbValueType.bb:
            return self.bb
        elif xtype == hsbValueType.bs:
            return self.bs
        else:
            raise Exception("unknown hsb type!")

    def set_nBytes(self, n):
        """
        target value format
        """
        self.n_bytes = n
        return self
    
    def set_nbits(self, n:str|int='default'):
        """
        bin string value format
        """
        if not hsbBitOption.is_valid(n):
            raise Exception("n must be auto or positive integer")
        self.n_bits = n
        return self
        
    
    def set_order(self, od):
        """
        target value format
        """
        self.order = od
        return self

    @property
    def b(self):
        """bytes"""
        self.target = hsbValueType.b
        return self.value

    @property
    def hb(self):
        """hex bytes"""
        self.target = hsbValueType.hb
        return self.value

    @property
    def num(self):
        """number"""
        self.target = hsbValueType.num
        return self.value

    @property
    def hs(self):
        """hex string"""
        self.target = hsbValueType.hs
        return self.value

    @property
    def bb(self):
        """bin bytes"""
        self.target = hsbValueType.bb
        return self.value

    @property
    def bs(self):
        """bin string"""
        self.target = hsbValueType.bs
        return self.value

    @classmethod
    def rev4B():
        pass

    def trans2b(self):
        """把当前对象中的值 转换成bytes格式 方便向其他格式转换"""
        # 输入必须为 大端序
        # 由不同格式转换成 大端序的bytes
        if self.current_type == hsbValueType.num:
            val: int = self._v
            # 自动计算 bytes
            bytes_len = int(val.bit_length() % 8 >0) + val.bit_length()//8
            res = val.to_bytes(bytes_len, byteorder='big')
        elif self.current_type == hsbValueType.hb:
            if len(self._v) % 2 == 1:
                # odd length
                _val = b'0' + self._v
            else:
                _val = self._v
            res = binascii.a2b_hex(_val)
        elif self.current_type == hsbValueType.b:
            res = self._v
        elif self.current_type == hsbValueType.hs:
            if len(self._v) % 2 == 1:
                # odd length
                _val = '0' + self._v
            else:
                _val = self._v
            res = binascii.a2b_hex(_val)
        elif self.current_type in [hsbValueType.bb, hsbValueType.bs]:
            # first, get res
            res = int(self._v, 2)

        # 补齐长度
        if self.n_bytes != hsbOption.n_bytes_default.value:
            # 不等于默认值表示设置了n_bytes
            if self.n_bytes > len(res):
                # 补\x00
                res = res.rjust(self.n_bytes, b"\x00")
            elif self.n_bytes < len(res):
                # 截取, 适用于前面有\x00的情况
                res = res[-self.n_bytes:]
            else:   # equal
                pass
        

        return res
    
    def trans2target(self, bytes_val: bytes, target: hsbValueType):
        
        """根据target_type 把bytes_val转换成目标格式"""
        # 转换成目标端序 因为当前是字节 所以直接翻转
        if self.order == 'little':
            bytes_val = bytes_val[::-1]
            # if target == hsbValueType.num:
            #     raise ValueError    # 大端序输入转小端序数字?

        if target == hsbValueType.num:
            res = int.from_bytes(bytes_val, byteorder='big')
        elif target == hsbValueType.hb:
            res = binascii.b2a_hex(bytes_val)
        elif target == hsbValueType.b:
            res = bytes_val
        elif target == hsbValueType.hs:
            res = binascii.b2a_hex(bytes_val).decode()
        elif target in [hsbValueType.bb, hsbValueType.bs]:
            # get target res
            num_val = self.num
            res = bin(num_val)[2:]
            if target == hsbValueType.bb:
                res = res.encode()
            # apply n_bits flag
            fill_char = '0' if type(res) == str else b'0'
            if self.n_bits == hsbBitOption.n_bits_default.value:
                pass
            else:
                # set target_len
                target_len = None
                if self.n_bits == hsbBitOption.n_bits_adjust.value:
                    target_len = self.bytelen * 8
                elif hsbBitOption.num_valid(self.n_bits):
                    target_len = self.n_bits
                else:
                    raise Exception("branch error")
                # fill or cut
                if target_len > len(res):  # zero fill
                    res = res.rjust(target_len, fill_char)
                else:
                    res = res[-target_len:]
                
        return res

    @property
    def value(self):
        """do transfer accroding to cur_type and target_type"""
        res_a = self.trans2b()
        res_b = self.trans2target(res_a, self.target)
        return res_b
    
    @property
    def bytelen(self):
        return len(self.b)
    
    @property
    def bitlen_8n(self):
        """8*self.bytelen"""
        return 8*self.bytelen
    
    @property
    def bitlen(self):
        return self.num.bit_length()

class hsb2b(hsb):
    """初始化之后 对象转换为并且存放bytes类型, 向其他类型转换效率高"""
    def fm_num(self, v):
        self.current_type = hsbValueType.num
        self._v = v
        return self.to_b()

    def fm_hs(self, v):
        self.current_type = hsbValueType.hs
        self._v = v
        return self.to_b()

    def fm_b(self,v):
        # b'\xde\xad\xbe\xef'
        self.current_type = hsbValueType.b
        self._v = v
        return self.to_b()

    def fm_hb(self,v):
        # b'deadbeef'
        self.current_type = hsbValueType.hb
        self._v = v
        return self.to_b()

if __name__ == "__main__":
    res = hsb().fm_num(12345678).b
    print(res)