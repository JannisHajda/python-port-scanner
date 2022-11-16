#!/usr/bin/env python3
import socket
import sys
import errno
from concurrent.futures import ThreadPoolExecutor


def connect_scan(target_host, target_port):
    try:
        # create a new socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set a timeout to improve performance
        s.settimeout(0.5)
        # connect to the target host
        s.connect((target_host, target_port))

        # connection successful -> port is open
        print("Port %d: Open" % target_port)
        # close the socket
        s.close()
    except socket.timeout:
        # connection timed out -> port is filtered
        print("Port %d: Filtered" % target_port)
    except socket.error as e:
        if e.errno == errno.ECONNREFUSED:
            # connection refused -> port is closed
            print("Port %d: Closed" % target_port)


def parse_ports(ports):
    port_list = []
    for port in ports.split(","):
        # parse port range
        if "-" in port:
            start, end = port.split("-")
            port_list += range(int(start), int(end) + 1)
        # parse single port
        else:
            port_list.append(int(port))

    return port_list


if __name__ == "__main__":
    # check if the user provided ports
    if (len(sys.argv) != 3):
        print("Usage: %s <host> <port(s)>" % sys.argv[0])
        sys.exit(1)

    host = sys.argv[1]
    ports = parse_ports(sys.argv[2])

    # create a thread pool to speed up the scan
    with ThreadPoolExecutor(max_workers=len(ports)) as executor:
        for port in ports:
            # submit the job to the thread pool
            executor.submit(connect_scan, host, port)

        # shutdown the thread pool
        executor.shutdown(wait=True)
