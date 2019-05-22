#!/usr/bin/python
#

##### Authors #####
"""
Tommy McNeela (https://www.linkedin.com/in/thomas-mcneela)
Jeremy Tate (https://www.linkedin.com/in/jeremy-tate-83114b40)
Version 0.1 20190522
"""
##### End Authors #####

# import libraries
import argparse
import os
import requests

# print message to screen if verbose
def vlog(msg):
    if VERBOSE:
        print msg

# check if subdomain / endpoint is valid
def testsub(sub):
    URL = "%s://%s.%s" % (PROTO, sub, TLD)
    vlog("Testing %s" % URL)
    r = requests.get(url = URL, verify = SECURE)
    body = r.content
    r.close()
    if FLAG in body:
        # this is not a valid subdomain/endpoint
        print "%s.%s is not a valid subdomain." % (sub, TLD)
    else:
        # this is a valid subdomain/endpoint
        print "%s.%s is a valid subdomain." % (sub, TLD)

# default to HTTPS
PROTO = "https"
# default flag for OpenShift invalid requests
FLAG = "The application is currently not serving requests at this endpoint. It may not have been started or is still starting."

# build command line arguments
parser = argparse.ArgumentParser(description = "Test for valid subdomains / endpoints hosted by an OpenShift deployment.")
parser.add_argument("-t", "--tld", help = "specify top level domain")
parser.add_argument("-s", "--sub", help = "specify a single subdomain")
parser.add_argument("-f", "--file", help = "file containing a list of subdomains to check")
parser.add_argument("--flag", help = "string to check for in body of response indicating invalid subdomain / endpoint")
parser.add_argument("-i", "--insecure", help = "do not verify HTTPS certificate", action = "store_false")
parser.add_argument("--http", help = "use HTTP instead of default (HTTPS)", action = "store_true")
parser.add_argument("-v", "--verbose", help = "increase output verbosity", action = "store_true")

# parse command line arguments
args = parser.parse_args()

# gather command line arguments
TLD = args.tld
SUB = args.sub
INFILE = args.file
if args.flag:
    FLAG = args.flag
SECURE = args.insecure
if args.http:
    PROTO = "http"
VERBOSE = args.verbose

# ignore warning if we aren't verifying HTTPS certificate
if not SECURE:
    requests.packages.urllib3.disable_warnings()

# DO THE STUFF
if INFILE and os.path.isfile(INFILE):
    # loop through file
    f = open(INFILE, "r")
    for SUB in f.readlines():
        testsub(SUB.strip())
    f.close()
elif SUB:
    # test single specified subdomain
    testsub(SUB)
else:
    print "Error, no valid input file or single subdomain specified."
