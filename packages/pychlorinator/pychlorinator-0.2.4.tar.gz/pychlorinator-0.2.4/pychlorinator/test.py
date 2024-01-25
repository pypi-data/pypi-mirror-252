import pychlorinator.chlorinator

session_key = bytes.fromhex("442a9b2b895cff62fc5a7264cc2eba90")
#data = bytes.fromhex("c717f5621c9e7e35ed4a6e1ec7a8184eb7dde17b")

data = {
    bytes.fromhex("8200677d7e9a95740b474a0d9796ffdf76c36135"),
}

for packet in data:
    output = pychlorinator.chlorinator.decrypt_characteristic( packet, session_key )
    print(f"{output.hex()}")

#print(f"session key {session_key.hex()}")
#print(f"data {data.hex()}")
#print(f"output {output.hex()}")
