import argparse
import asyncio
from enum import Enum
from hashlib import md5
import logging
import os
import secrets
import socket

PORT = 9715

logger = logging.getLogger(__name__)


class PowerStatus(Enum):
    Off = 0x0000
    On = 0x0100
    CoolDown = 0x0200


class InputSource(Enum):
    ComputerIn1 = 0x0000
    ComputerIn2 = 0x0400
    HDMI = 0x0300
    Component = 0x0500
    SVideo = 0x0200
    Video = 0x0100
    USBTypeA = 0x0600
    LAN = 0x0B00
    USBTypeB = 0x0C00


class EcoModeStatus(Enum):
    Normal = 0x0000
    Eco = 0x0100


class AutoEcoModeStatus(Enum):
    Off = 0x0000
    On = 0x0100


class BlankStatus(Enum):
    Off = 0x0000
    On = 0x0100


class ErrorStatus(Enum):
    Normal = 0x0000
    Cover = 0x0100
    Fan = 0x0200
    Lamp = 0x0300
    Temp = 0x0400
    AirFlow = 0x0500
    Cold = 0x0700
    Filter = 0x0800


class Command(Enum):
    AutoEcoModeOn = "auto_eco_mode_on"
    AutoEcoModeOff = "auto_eco_mode_off"
    AutoEcoModeGet = "auto_eco_mode_get"
    BlankOn = "blank_on"
    BlankOff = "blank_off"
    BlankGet = "blank_get"
    EcoModeEco = "eco_mode_eco"
    EcoModeNormal = "eco_mode_normal"
    EcoModeGet = "eco_mode_get"
    ErrorStatusGet = "error_status_get"
    PowerTurnOn = "power_turn_on"
    PowerTurnOff = "power_turn_off"
    PowerGet = "power_get"
    GammaGet = "gamma_get"
    InputSourceGet = "input_source_get"
    InputSourceComputerIn1 = "input_source_computer_in_1"
    InputSourceComputerIn2 = "input_source_computer_in_2"
    InputSourceHDMI = "input_source_hdmi"
    InputSourceComponent = "input_source_component"
    InputSourceSVideo = "input_source_svideo"
    InputSourceVideo = "input_source_video"
    InputSourceUSBTypeA = "input_source_usb_type_a"
    InputSourceLAN = "input_source_lan"
    InputSourceUSBTypeB = "input_source_usb_type_b"
    FilterTimeGet = "filter_time_get"
    LampTimeGet = "lamp_time_get"


commands = {
    Command.AutoEcoModeOff: bytes.fromhex("BE EF 03 06 00 FB 27 01 00 10 33 00 00"),
    Command.AutoEcoModeOn: bytes.fromhex("BE EF 03 06 00 6B 26 01 00 10 33 01 00"),
    Command.AutoEcoModeGet: bytes.fromhex("BE EF 03 06 00 C8 27 02 00 10 33 00 00"),
    Command.BlankOff: bytes.fromhex("BE EF 03 06 00 FB D8 01 00 20 30 00 00"),
    Command.BlankOn: bytes.fromhex("BE EF 03 06 00 6B D9 01 00 20 30 01 00"),
    Command.BlankGet: bytes.fromhex("BE EF 03 06 00 C8 D8 02 00 20 30 00 00"),
    Command.EcoModeEco: bytes.fromhex("BE EF 03 06 00 AB 22 01 00 00 33 01 00"),
    Command.EcoModeNormal: bytes.fromhex("BE EF 03 06 00 3B 23 01 00 00 33 00 00"),
    Command.EcoModeGet: bytes.fromhex("BE EF 03 06 00 08 23 02 00 00 33 00 00"),
    Command.ErrorStatusGet: bytes.fromhex("BE EF 03 06 00 D9 D8 02 00 20 60 00 00"),
    Command.PowerTurnOff: bytes.fromhex("BE EF 03 06 00 2A D3 01 00 00 60 00 00"),
    Command.PowerTurnOn: bytes.fromhex("BE EF 03 06 00 BA D2 01 00 00 60 01 00"),
    Command.PowerGet: bytes.fromhex("BE EF 03 06 00 19 D3 02 00 00 60 00 00"),
    Command.GammaGet: bytes.fromhex("BE EF 03 06 00 F4 F0 02 00 A1 30 00 00"),
    Command.InputSourceGet: bytes.fromhex("BE EF 03 06 00 CD D2 02 00 00 20 00 00"),
    Command.InputSourceComputerIn1: bytes.fromhex(
        "BE EF 03 06 00 FE D2 01 00 00 20 00 00"
    ),
    Command.InputSourceComputerIn2: bytes.fromhex(
        "BE EF 03 06 00 3E D0 01 00 00 20 04 00"
    ),
    Command.InputSourceHDMI: bytes.fromhex("BE EF 03 06 00 0E D2 01 00 00 20 03 00"),
    Command.InputSourceComponent: bytes.fromhex(
        "BE EF 03 06 00 AE D1 01 00 00 20 05 00"
    ),
    Command.InputSourceSVideo: bytes.fromhex("BE EF 03 06 00 9E D3 01 00 00 20 02 00"),
    Command.InputSourceVideo: bytes.fromhex("BE EF 03 06 00 6E D3 01 00 00 20 01 00"),
    Command.InputSourceUSBTypeA: bytes.fromhex(
        "BE EF 03 06 00 5E D1 01 00 00 20 06 00"
    ),
    Command.InputSourceLAN: bytes.fromhex("BE EF 03 06 00 CE D5 01 00 00 20 0B 00"),
    Command.InputSourceUSBTypeB: bytes.fromhex(
        "BE EF 03 06 00 FE D7 01 00 00 20 0C 00"
    ),
    Command.FilterTimeGet: bytes.fromhex("BE EF 03 06 00 C2 F0 02 00 A0 10 00 00"),
    Command.LampTimeGet: bytes.fromhex("BE EF 03 06 00 C2 FF 02 00 90 10 00 00"),
}


class ReplyType(Enum):
    ACK = 0x06
    NACK = 0x15
    ERROR = 0x1C
    DATA = 0x1D
    BUSY = 0x1F
    AUTH = 0xFF  # virtual, this is actually 0x1F too


def make_packet(cmd, digest=None):
    HEADER = 0x02
    DATA_LENGTH = 0x0D

    packet = bytearray()
    if digest:
        packet.extend(digest)
    packet.extend([HEADER, DATA_LENGTH])
    packet.extend(cmd)

    checksum = (255 - ((packet[0] + packet[1] + packet[-1]) & 0xFF)).to_bytes(1)
    packet.extend(checksum)

    connection_id = secrets.randbelow(256)
    packet.append(connection_id)

    logger.debug(
        f"checksum={checksum},connection_id={connection_id},packet={packet.hex()}"
    )
    return (packet, connection_id)


def parse_reply(reply_type, reply):
    match reply_type:
        case ReplyType.ACK:
            logger.debug("Command ACKed")
            return (ReplyType.ACK, None)

        case ReplyType.NACK:
            logger.debug("Command NACKed")
            return (ReplyType.NACK, None)

        case ReplyType.ERROR:
            error_code = reply[1:3]
            logger.debug(f"Command errored: {error_code.hex()}")
            return (ReplyType.ERROR, error_code)

        case ReplyType.DATA:
            data = reply[1:3]
            logger.debug(f"Command response: {data.hex()}")
            return (ReplyType.DATA, data)

        case ReplyType.BUSY:
            status = reply[1:3]
            if status == bytes([0x04, 0x00]):
                logger.debug("Command invalid auth")
                return (ReplyType.AUTH, None)

            logger.debug(f"Command busy: {status.hex()}")
            return (ReplyType.BUSY, status)

        case _:
            logger.debug("Command invalid auth")
            return (ReplyType.AUTH, None)


def build_auth_digest(nonce, password):
    content = bytearray()
    content.extend(nonce)
    content.extend(bytes(password, "utf-8"))

    hash_context = md5()
    hash_context.update(content)
    return bytes(hash_context.hexdigest(), "utf-8")


class HitachiProjectorConnection:
    def __init__(self, host, password):
        self.host = host
        self.password = password

    async def async_send_cmd(self, cmd):
        logger.debug("async connecting")
        packet, connection_id = make_packet(cmd)
        reader, writer = await asyncio.open_connection(self.host, PORT)

        logger.debug("sending")
        writer.write(packet)
        await writer.drain()

        logger.debug("reading")
        reply = await reader.read(256)
        logger.debug(f"data={reply.hex()}")

        # Check if auth required
        if len(reply) == 8:
            logger.debug("reading expected auth failure")
            expected_auth_failure_reply = await reader.read(256)
            logger.debug(f"data={expected_auth_failure_reply.hex()}")
            if expected_auth_failure_reply != bytes([0x1F, 0x04, 0x00, connection_id]):
                raise RuntimeError("Unexpected auth failure response")

            if self.password is None:
                raise RuntimeError("Auth required but missing password")

            digest = build_auth_digest(reply, self.password)
            logger.debug(f"reply: {reply.hex()}, digest: {digest}")

            packet, connection_id = make_packet(cmd, digest)

            logger.debug("sending with digest")
            writer.write(packet)
            await writer.drain()

            logger.debug("reading")
            reply = await reader.read(256)
            logger.debug(f"data={reply.hex()}")

        writer.close()
        await writer.wait_closed()

        reply_type = ReplyType(reply[0])

        this_connection = connection_id == reply[-1]
        if not this_connection:
            logger.debug(
                f"Received reply for other connection: {connection_id} != {reply[-1]}"
            )
            return (False, None)

        return parse_reply(reply_type, reply)

    async def get_power_status(self):
        return await self.__build_get_status(Command.PowerGet, PowerStatus)

    async def get_input_source(self):
        return await self.__build_get_status(Command.InputSourceGet, InputSource)

    async def get_eco_mode_status(self):
        return await self.__build_get_status(Command.EcoModeGet, EcoModeStatus)

    async def get_auto_eco_mode_status(self):
        return await self.__build_get_status(Command.AutoEcoModeGet, AutoEcoModeStatus)

    async def get_blank_status(self):
        return await self.__build_get_status(Command.BlankGet, BlankStatus)

    async def get_error_status(self):
        return await self.__build_get_status(Command.ErrorStatusGet, ErrorStatus)

    async def get_filter_time(self):
        return await self.__build_get_value(Command.FilterTimeGet)

    async def get_lamp_time(self):
        return await self.__build_get_value(Command.LampTimeGet)

    async def __build_get_value(self, command):
        reply_type, data = await self.async_send_cmd(commands[command])
        if reply_type != ReplyType.DATA or data is None:
            return reply_type, data

        value = int.from_bytes(data, byteorder="little")
        return (reply_type, value)

    async def __build_get_status(self, command, enum):
        reply_type, data = await self.async_send_cmd(commands[command])
        if reply_type != ReplyType.DATA or data is None:
            return reply_type, data

        status = enum(int.from_bytes(data, byteorder="big"))
        return (reply_type, status)


async def main():
    logging.basicConfig(level=os.environ.get("LOG", logging.INFO))

    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument(
        "command", choices=list(map(lambda key: key.value, commands.keys()))
    )
    parser.add_argument("-p", "--password")
    args = parser.parse_args()
    command = Command(args.command)

    con = HitachiProjectorConnection(host=args.host, password=args.password)

    print(f"Sending cmd: {command}")

    reply_type, data = await con.async_send_cmd(commands[command])
    match reply_type:
        case ReplyType.ACK:
            pass

        case ReplyType.DATA:
            assert data is not None
            match command:
                case Command.PowerGet:
                    status = PowerStatus(int.from_bytes(data, byteorder="big"))
                    print(f"Power status: {status}")

                case Command.InputSourceGet:
                    status = InputSource(int.from_bytes(data, byteorder="big"))
                    print(f"Input source: {status}")

                case _:
                    print(f"Command reply: {data.hex()}")

        case _:
            print(f"bad response: {reply_type}, {data}")
            raise RuntimeError("bad response")

    print("Done")


if __name__ == "__main__":
    asyncio.run(main())
