import sys
import argparse
import pwinput

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help = "Username for your MergeTB account")
parser.add_argument("-p", "--password", help = "Password for your MergeTB account")
parser.add_argument("-S", "--server", help = "MergeTB portal GRPC address", default = "grpc.sphere-testbed.net")
parser.add_argument("-P", "--port", help = "MergeTB portal GRPC port", type = int, default = 443)
parser.add_argument("-X", "--disable-tls", help = "Disable TLS when communication with the MergeTB portal", action = 'store_true')
args = parser.parse_args()

###
# These 4 lines are only needed if you intend to communicate with a non-standard
# Merge portal. They are here as a reference
from mergetb.grpc_client import MergeGRPCConfig, set_grpc_config
set_grpc_config(MergeGRPCConfig(
    server=args.server, port=args.port, ssl=(not args.disable_tls),
))

def check_prompt_credentials():
    global args

    if not args.username:
        args.username = input("Enter your MergeTB username: ")
    if not args.password:
        args.password = pwinput.pwinput("Enter your MergeTB password: ", mask='*')

    return args.username, args.password 
