import subprocess
from bitcoinrpc.authproxy import AuthServiceProxy
from key import user, pw

PASSWORD = pw
USERNAME = user
IPADDRESS = "0.0.0.0"
PORT = "8555"

# rpc_connection = AuthServiceProxy(
#     f"http://{USERNAME}:{PASSWORD}@{IPADDRESS}:{PORT}")

# print(rpc_connection.uptime())

subprocess.run(
    ['/home/jesjehle//projects/defichain/defichain-cli/defichain-2.3.1/bin/defi-cli', '-rpcuser=ts', '-stdinrpcpass', 'getbalance'])
