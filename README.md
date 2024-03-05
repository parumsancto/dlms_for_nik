
# A Python library DLMS/COSEM for NIK power meters.
* forked from [u9n/dlms-cosem](https://github.com/u9n/dlms-cosem)
# About
`dlms-cosem` is designed to be a tool with a simple API for working with DLMS/COSEM
enabled energy meters. It provides the lowest level function, as protocol state
management, APDU encoding/decoding, APDU encryption/decryption.

The library aims to provide a [sans-io](https://sans-io.readthedocs.io/) implementation
of the DLMS/COSEM protocol so that the protocol code can be reused with several
io-paradigms. As of now we provide a simple client implementation based on
blocking I/O. This can be used over either a serial interface with HDLC or over TCP.

We have not implemented full support to be able to build a server (meter) emulator. If
this is a use-case you need, consider sponsoring the development and contact us.
# Supported features
* AssociationRequest  and AssociationRelease
* GET
# Example use:
Look /examples folder
# Supported meters
* NIK2401
# License
Open Source License



