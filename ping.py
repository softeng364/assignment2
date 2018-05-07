# -*- coding: utf-8 -*-
import checksum  # Use *our* checksum module

def ping(client_socket, dest_host, id, seq_no):
    """
    Sends echo request, receives response, and returns RTT
    """
	pass  # TODO: Compute and return RTT


def verbose_ping(host, timeout=1.0, count=4, log=print):
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

    for seq_no in range(count):
        try:		
			# TODO: Call ping()		
        except TimeoutError:
            # TODO: Handle exception

		# TODO: Handle other exceptions

	# TODO: Print number of successful echoes

	# TODO: Print round-trip time statistics

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Test a host.')

	# TODO: Define command line arguments
	
    args = parser.parse_args()

    for host in args.hosts:
        verbose_ping(host, timeout=args.timeout, count=args.count)
