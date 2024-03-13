from typing import *

from dlms_cosem import a_xdr, dlms_data
from dlms_cosem.dlms_data import decode_variable_integer


def parse_as_dlms_data(data: bytes):
    data_decoder = a_xdr.AXdrDecoder(
        encoding_conf=a_xdr.EncodingConf(
            attributes=[a_xdr.Sequence(attribute_name="data")]
        )
    )
    return data_decoder.decode(data)["data"]


def parse_dlms_object(source_bytes: bytes) -> List[int]:
    """
    Some DLMS object attributes contain data structures. The items are not self
    descriptive and we cannot use the normal parser since we dont know what items to
    parse as the data tag is not included.

    But is seems they are always integers so we can parse them as a list of integers.
    """
    values = list()
    data = bytearray(source_bytes)
    tag = data.pop(0)
    allowed_dlms_object_tags = [dlms_data.DataArray.TAG, dlms_data.DataStructure.TAG]
    if tag not in allowed_dlms_object_tags:
        raise ValueError(
            f"You cannot use the dlms object parse "
            f"with {dlms_data.DlmsDataFactory.get_data_class(tag)}"
        )
    length, rest = decode_variable_integer(data)
    data = rest
    for i in range(0, length):
        values.append(data.pop(0))

    return values


def manufacturing_num_to_addr(man_num:int) -> tuple[int,int]:
	""" Convert NIK manufacturing number to logical and physical address 
	for HDLC transport protocol.
	Returns tuple (logical_addr, physical_addr)"""
	addr_hi = 0
	addr_lo = man_num & 0x3FFF

	if (man_num & 0x3FFF) < 16:
		addr_lo += 16
		addr_hi = addr_hi | (1<<12)
	else:
		addr_lo = man_num & 0x3FFF

	if ((man_num >> 14) & 0x3FFF) < 16:
		addr_hi += ((man_num >> 14) & 0x3FFF) + 16
		addr_hi |= (1 << 13)
	else:
		addr_hi |= (man_num >> 14) & 0x3FFF
	
	return (addr_hi, addr_lo)