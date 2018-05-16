# -*- coding: utf-8 -*-
import os
import sys
import socket
import struct
import time

import collections
from checksum import internet_checksum

assert 3 <= sys.version_info[0], 'Requires Python 3'

# For readability in time conversions
MILLISEC_PER_SEC = 1000.0

# Selects the right-most 16 bits
RIGHT_HEXTET = 0xffff

# Size in bits of buffer in which socket data is received
BUFFER_SIZE = 2 << 5

# A port number is required for socket.socket, even through port
# numbers are unused by ICMP. We use a legal (i.e. strictly positive)
# port number, just to be safe.
ICMP_PORT_PLACEHOLDER = 1
ICMP_HEADER_LENGTH = 28
ICMP_STRUCT_FIELDS = "BBHHH"  # for use with struct.pack/unpack


#
# TODO: Define ChecksumError class
#


# Note that TimeoutError already exists in the Standard Library
#class TimeoutError(PingError):
#    pass


# See IETF RFC 792: https://tools.ietf.org/html/rfc792
# NB: The order of the fields *is* significant
ICMPMessage = collections.namedtuple('ICMPMessage',
                                  ['type', 'code', 'checksum',
                                   'identifier', 'sequence_number'])
# For ICMP type field:
# See https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol
#     http://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
ICMPTypeCode = collections.namedtuple('ICMPTypeCode', ['type', 'code'])
ECHO_REQUEST = ICMPTypeCode(8, 0)
ECHO_REPLY = ICMPTypeCode(0, 0)


def this_instant():
	# TODO: Decide which of the following values to return here:
	# time.clock(), time.perf_counter(), time.process_time()
    return None


def ping(client_socket, dest_host, client_id, seq_no=0):
    """
   Sends echo request, receives response, and returns RTT.
    """

    def icmp_header(host_checksum):
        message = ICMPMessage(
                    type=None,  # TODO: Use appropriate argument here
                    code=None,  # TODO: Use appropriate argument here
                    checksum=host_checksum,
                    identifier=client_id,
                    sequence_number=seq_no)
        return struct.pack(ICMP_STRUCT_FIELDS, *message)

	# TODO: Please study these lines carefully,
	#       noting that "icmp_pack()" (defined above) is called *twice*
    icmp_payload = struct.pack('d', this_instant())  # double-precision float
    icmp_packet_without_checksum = icmp_header(0) + icmp_payload
    checksum = internet_checksum(icmp_packet_without_checksum)
    icmp_packet = icmp_header(checksum) + icmp_payload

    #
    # TODO: Please note that that "icmp_packet" is the
    #       payload that we'll send through for our INET raw socket
    #

    # Note: socket.gethostbyname() returns the host name
    # unchanged if it is already in IPv4 address format.
    dest_host = socket.gethostbyname(dest_host)

    #
	# TODO:
	# 1. Call sendto() on socket to send packet to destination host
    # 2. Call recvfrom() on socket to receive datagram
	#    (Note: A time-out exception might be raised here).
    # 2. Store this_instant() at which datagram was received
	# 3. Extract ICMP packet from datagram i.e. drop IP header (20 bytes)
	#     e.g. "icmp_packet = datagram[20:]"
	# 4. Compute checksum on ICMP response packet (header and payload);
	#     this will hopefully come to zero
	# 5. Raise exception if checksum is nonzero
	# 6. Extract ICMP response header from ICMP packet (8 bytes) and
	#     unpack binary response data to obtain ICMPMessage "response"
	#     that we'll return with the round-trip time (Step 9, below);
	#     notice that this namedstruct is printed in the sample
	#     command line output given in the assignment description.
	#     e.g. "Reply from 151.101.0.223 in 5ms: ICMPMessage(type=0, code=0, checksum=48791, identifier=33540, sequence_number=0)"
	# 7. Extract ICMP response payload (remaining bytes) and unpack
	#     binary data to recover "time sent"
	# 8. Compute round-trip time from "time sent"
	# 9. Return "(round-trip time in milliseconds, response)"
	#
    # If things go wrong
    # ==================
    # You might like to check ("assert") that:
    # 1. Type field of ICMP response header is ICMP echo reply type
    # 2. Code field of ICMP response header is ICMP echo reply code
    # 3. Identifier field of ICMP response header is client_id
    # 4. len() of ICMP response payload is struct.calcsize('d')
    #

def verbose_ping(host, timeout=2.0, count=4, log=print):
    """
    Send ping and print session details to command prompt.
    """
    try:
        host_ip = socket.gethostbyname(host)
    except OSError as error:
        log(error)
        log('Could not find host {}.'.format(host))
        log('Please check name and try again.')
        return

    #
	# TODO: Print suitable heading
	#       e.g. log("Contacting {} with {} bytes of data ".format(...))
    #

    round_trip_times = []

    for seq_no in range(count):
        try:
            #
			# TODO: Open socket using "with" statement
			#
			# TODO: set time-out duration (in seconds) on socket
			#

                # "The Identifier and Sequence Number can be used by the
                # client to match the reply with the request that caused the
                # reply. In practice, most Linux systems use a unique
                # identifier for every ping process, and sequence number is
                # an increasing number within that process. Windows uses a
                # fixed identifier, which varies between Windows versions,
                # and a sequence number that is only reset at boot time."
                # -- https://en.wikipedia.org/wiki/Ping_(networking_utility)
                client_id = os.getpid() & RIGHT_HEXTET

                delay, response = ping(client_socket,
                                   host,
                                   client_id=client_id,
                                   seq_no=seq_no)

            log("Reply from {:s} in {}ms: {}".format(host_ip, delay, response))

			#
            # TODO: Append "delay" to round_trip_times
			#

		# TODO:
        # catch time-out error:
        #     handle time-out error i.e. log(...)

		# TODO:
        # catch check-sum error
        #     handle checksum-error i.e. log(...)

        except OSError as error:
            log("OS error: {}. Please check name.".format(error.strerror))
            if isinstance(error, PermissionError):
                # Display the likely explanation for
                # TCP Socket Error Code "1 = Operation not permitted":
                log("NB: On some sytems, ICMP messages can"
                    " only be sent from processes running as root.")
            break

	#
	# TODO: Print packet statistics header
	# TODO: Compute & print packet statistics
	#       i.e. "how many packets received and lost?"
	#

	#
    # TODO: "if received more than 0 packets":
	#    TODO: Compute & print statistics on round-trip times
	#          i.e. Minimum, Maximum, Average
	#


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Test a host.')
    parser.add_argument('-w', '--timeout',
                        metavar=None,  # TODO: Specify this argument
                        type=int,
                        default=None,  # TODO: Specify this argument
                        help='Timeout to wait for each reply (milliseconds).')
    parser.add_argument('-c', '--count',
                        metavar='num',
                        type=None,  # TODO: Specify this argument
                        default=4,
                        help=None)  # TODO: Specify this argument
    parser.add_argument('hosts',
                        metavar='host',
                        type=str,
                        nargs='+',
                        help=None)  # TODO: Specify this argument
    args = parser.parse_args()

    for host in args.hosts:
        verbose_ping(host, timeout=args.timeout, count=args.count)
