"""I2C transport layer
"""
from logging import getLogger
from time import sleep
from pymdfu.transport import Transport, TransportError
from pymdfu.timeout import Timer
from pymdfu.mac.exceptions import MacError, MacI2cNackError

RESPONSE_READY = 0x01

class I2cTransport(Transport):
    """ Transport layer for I2C
    """
    def __init__(self, mac, timeout=5, polling_interval=0.001):
        """ Class initialization

        :param mac: MAC layer for i2c bus access
        :type mac: Classes that implement the MAC layer interface
        :param timeout: Communication timeout in seconds, defaults to 5
        :type timeout: int, optional
        :param polling_interval: Response size polling interval in seconds. The minimum and accuracy
        is dependent on the operating system and Python version (3.11 has an improved timer implementation)
        but typically it can be expected that accuracy is reasonable down to 0.001s.
        :type polling_interval: float
        """
        self.timeout = timeout
        self.polling_interval = polling_interval
        self.com = mac
        self.logger = getLogger(__name__)

    # Support 'with ... as ...' construct
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.com:
            self.com.close()

    @staticmethod
    def calculate_checksum(data):
        """Calculate checksum for transport frame

        The checksum is a two's complement addition (integer addition)
        of 16-bit values in little-endian byte oder.

        :param data: Input data for checksum calculation
        :type data: Bytes like object
        :return: 16bit checksum
        :rtype: int
        """
        checksum = 0
        for i in range(0, len(data), 2):
            checksum += (data[i + 1] << 8) | data[i]
        return (~checksum) & 0xffff

    def create_frame(self, packet):
        """Create a transport frame

        :param packet: MDFU packet
        :type packet: Bytes
        :return: Transport frame
        :rtype: Bytes
        """
        if len(packet) % 2:
            check_sequence = self.calculate_checksum(packet + bytes(1))
        else:
            check_sequence = self.calculate_checksum(packet)
        check_sequence = check_sequence.to_bytes(2, byteorder="little")
        frame = packet + check_sequence
        return frame

    def open(self):
        """Open transport
        """
        try:
            self.com.open()
        except MacError as exc:
            self.logger.error("Opening Mac failed: %s", exc)
            raise TransportError(exc) from exc

    def close(self):
        """Close transport
        """
        self.com.close()

    @property
    def mac(self):
        """MAC layer

        :return: MAC layer used in the transport layer
        :rtype: Mac
        """
        return self.com

    def write(self, data):
        """Send MDFU command packet to client

        :param data: MDFU packet
        :type data: bytes
        """
        frame = self.create_frame(data)
        self.logger.debug("Sending frame -> 0x%s", frame.hex())
        try:
            self.com.write(frame)
        except (MacError, MacI2cNackError) as exc:
            raise TransportError(exc) from exc

    def _poll_for_status(self, timeout):
        """Poll for client status

        :param timeout: Polling timeout in seconds.
        :type timeout: float
        :raises TransportError: When timeout expires during polling
        :raises TransportError: When a MAC error is raised
        """
        timer = Timer(timeout if timeout else self.timeout)

        # Poll for status
        while True:
            try:
                buf = self.com.read(1)
                if buf:
                    if 1 == len(buf):
                        self.logger.debug("Received status <- 0x%s", buf.hex())
                        status = int(buf[0])
                        if status & RESPONSE_READY:
                            break
            except MacI2cNackError:
                pass # Continue polling when client NACKs
            except MacError as exc:
                raise TransportError(exc) from exc

            if timer.expired():
                raise TransportError("Timeout while waiting for response from client.")
            sleep(self.polling_interval)

    def read(self, timeout=None):
        """Receive a MDFU status packet

        :param timeout: Timeout for the read operation in seconds
        timeout = 0 -> Non-blocking read
        timeout = None -> Use default timeout set during class initialization.
        timeout any other value -> The value is used as timeout
        :type timeout: Float
        :raises TransportError: For CRC checksum mismatch
        :raises TransportError: When MAC returns unexpected number of bytes
        :raises TransportError: When a MAC error was raised
        :return: MDFU status packet
        :rtype: bytes
        """
        self._poll_for_status(timeout)
        # Read response length
        try:
            buf = self.com.read(5)
            if buf is not None and 5 == len(buf):
                self.logger.debug("Received response frame size <- 0x%s", buf.hex())
                size = int.from_bytes(buf[1:3], byteorder="little")
                checksum = int.from_bytes(buf[3:5], byteorder="little")
                calculated_checksum = self.calculate_checksum(buf[1:3])
                if checksum != calculated_checksum:
                    raise TransportError("I2C transport checksum mismatch")
            else:
                raise TransportError(f"Unexpected number of bytes returned \
from client for response size, got {len(buf)} but expected 5")
        except MacError as exc:
            raise TransportError(exc) from exc

        # Read response
        try:
            frame = self.com.read(size + 1)
            self.logger.debug("Received response <- 0x%s", frame.hex())
            frame = frame[1:] # remove status byte
            frame_checksum = int.from_bytes(frame[-2:], byteorder="little")
            packet = frame[:-2]

            if len(packet) % 2:
                calculated_checksum = self.calculate_checksum(packet + bytes(1))
            else:
                calculated_checksum = self.calculate_checksum(packet)

            if frame_checksum != calculated_checksum:
                self.logger.error("I2C transport checksum mismatch")
                raise TransportError("I2C transport checksum mismatch")
        except MacError as exc:
            raise TransportError(exc) from exc
        return packet

class I2cTransportClient(Transport):
    """ Transport layer for I2C
    """
    def __init__(self, mac, timeout=5):
        """ Class initialization

        :param mac: MAC layer for i2c bus access
        :type mac: Classes that implement the MAC layer interface
        :param timeout: Communication timeout in seconds, defaults to 5
        :type timeout: int, optional
        """
        self.timeout = timeout
        self.com = mac
        self.logger = getLogger(__name__)

    def __del__(self):
        if self.com:
            self.com.close()

    # Support 'with ... as ...' construct
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.com:
            self.com.close()

    @staticmethod
    def calculate_checksum(data):
        """Calculate checksum for transport frame

        The checksum is a two's complement addition (integer addition)
        of 16-bit values in little-endian byte oder.

        :param data: Input data for checksum calculation
        :type data: Bytes like object
        :return: 16bit checksum
        :rtype: int
        """
        checksum = 0
        for i in range(0, len(data), 2):
            checksum += (data[i + 1] << 8) | data[i]
        return (~checksum) & 0xffff

    def create_frame(self, packet):
        """Create a transport frame

        The frame created here consists of
        - MDFU packet size (2 bytes)
        - MDFU packet size checksum (2 bytes)
        - MDFU packet (MDFU packet size bytes)
        - MDFU packet checksum (2 bytes)

        :param packet: MDFU packet
        :type packet: Bytes
        :return: Transport frame
        :rtype: Bytes
        """
        if len(packet) % 2:
            check_sequence = self.calculate_checksum(packet + bytes(1))
        else:
            check_sequence = self.calculate_checksum(packet)
        packet_check_sequence = check_sequence.to_bytes(2, byteorder="little")
        size = len(packet).to_bytes(2, byteorder="little")
        check_sequence = self.calculate_checksum(size)
        size_check_sequence = check_sequence.to_bytes(2, byteorder="little")
        frame = size + size_check_sequence + packet + packet_check_sequence
        return frame

    def open(self):
        """Open transport
        """
        try:
            self.com.open()
        except MacError as exc:
            self.logger.error("Opening Mac failed: %s", exc)
            raise TransportError(exc) from exc

    def close(self):
        """Close transport
        """
        self.com.close()

    @property
    def mac(self):
        """MAC layer

        :return: MAC layer used in the transport layer
        :rtype: Mac
        """
        return self.com

    def write(self, data):
        """Send MDFU command packet to host

        :param data: MDFU packet
        :type data: bytes
        """
        frame = self.create_frame(data)
        # We have three I2C transactions for a response
        # 1) Return status byte with repsonse ready
        # 2) Response size + size checksum
        # 3) MDFU response packet + packet checksum
        # so we issue three writes here
        status = bytes([RESPONSE_READY])
        self.logger.debug("Sending status -> 0x%s", status.hex())
        self.com.write(status)
        self.logger.debug("Sending response length -> 0x%s", frame[:4].hex())
        self.com.write(status + frame[:4])
        self.logger.debug("Sending response -> 0x%s", frame[4:].hex())
        self.com.write(status + frame[4:])

    def read(self, timeout=None):
        """Receive a MDFU packet

        :param timeout: Timeout for the read operation in seconds.
        timeout = 0 -> Non-blocking read
        timeout = None -> Use default timeout set during class initialization.
        timeout any other value -> The value is used as timeout
        :type timeout: Float
        :raises ValueError: Upon checksum error
        :return: MDFU status packet
        :rtype: bytes
        """
        packet = None
        timer = Timer(timeout if timeout else self.timeout)

        while True:
            try:
                frame = self.com.read()
                if frame:
                    packet = frame[:-2]
                    checksum = int.from_bytes(frame[-2:], byteorder="little")

                    if len(packet) % 2:
                        calc_checksum = self.calculate_checksum(packet + bytes(1))
                    else:
                        calc_checksum = self.calculate_checksum(packet)

                    if checksum != calc_checksum:
                        raise TransportError("Frame checksum error detected")
                    break
            except MacError as exc:
                raise TransportError(exc) from exc

            if timer.expired():
                raise TransportError("Timeout while waiting for response from client.")
        return packet
