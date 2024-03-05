import logging
import os
import sys

# Добавление пути текущей папки в список путей поиска модулей для импорта
sys.path.append(os.path.dirname(__file__))
# Добавление пути в корень проекта в список путей поиска модулей для импорта
sys.path.append(os.path.split(os.path.dirname(__file__))[0])

from dlms_cosem import cosem, enumerations
from dlms_cosem.security import (
    NoSecurityAuthentication,
    LowLevelSecurityAuthentication,
    HighLevelSecurityGmacAuthentication,
)
from dlms_cosem.client import DlmsClient
from dlms_cosem.io import BlockingTcpIO, HdlcTransport


# стенд 1
#HOST = '10.48.0.2'
#PORT = 7772

# стенд 2
HOST = '10.48.0.111'
PORT = 7771

USER = 'Оператор'
PASSWORD = '1111111111111111'
#MANUFACTURING_NUM = 10056361 # стенд 1
MANUFACTURING_NUM = 10083641 # стенд 2
SERIAL_NUM = 2104100563612018


# set up logging so you get a bit nicer printout of what is happening.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s,%(msecs)d : %(levelname)s : %(message)s",
    datefmt="%H:%M:%S",
)


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


power_meter_addr = manufacturing_num_to_addr(MANUFACTURING_NUM)
public_hdlc_transport = HdlcTransport(
    client_logical_address=16,
    server_logical_address=power_meter_addr[0],#MANUFACTURING_NUM,#613,
    server_physical_address=power_meter_addr[1],#12969,
    extended_addressing=True,
    io=BlockingTcpIO(host=HOST, port=PORT),
)
authentication = LowLevelSecurityAuthentication(
        secret=bytes(PASSWORD, 'utf-8'),
        user_type='user'
    )
public_client = DlmsClient(
    transport=public_hdlc_transport, # type: ignore
    #authentication=NoSecurityAuthentication()
    authentication=authentication, # type: ignore
    #authentication=HighLevelSecurityGmacAuthentication()
)   


with public_client.session() as client:
	print('BEGIN READ METRICS')
	# Суммарная по фазам активная мощность A+ (Вт)
	response_data = client.get(
		cosem.CosemAttribute(
			interface=enumerations.CosemInterface.REGISTER,
			#instance=cosem.Obis(1, 0, 15, 7, 0, 0),
			instance=cosem.Obis(1, 0, 1, 7, 0, 0),
			attribute=2,
		)
	)
	print('Суммарная по фазам активная мощность A+ (Вт) = '
		f'{int.from_bytes(response_data[1:], byteorder='little', signed=False)/1000}')

	# Напряжение фазы (для 1 Ф счетчика) 
	response_data = client.get(
		cosem.CosemAttribute(
			interface=enumerations.CosemInterface.REGISTER,
			#instance=cosem.Obis(1, 0, 15, 7, 0, 0),
			instance=cosem.Obis(1, 0, 12, 7, 0, 0),
			attribute=2,
		)
	)
	print('Напряжение фазы (для 1 Ф счетчика) = '
		f'{int.from_bytes(response_data[1:], byteorder='little', signed=False)/1000}')
