# Python Port Scanner

This script scans a give IP for open ports using the TCP Connect scan method. It's using multithreading to speed up the whole process.

## Usage

`python3 scanner.py <IP> <PORTS>`

## Parameters

**IP** - IPv4-address of the target to be scanned \
**PORTS** - comma seperated list of ports to be checked, also allows range of ports (eg. 1-433,1000)
