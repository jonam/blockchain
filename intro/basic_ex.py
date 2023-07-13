"""
This code does not have any dependencies beyond the Python standard library. You can run it using any Python 3 interpreter.

Please note, this is a simplified blockchain and lacks many features that a real-world blockchain would have, such as peer-to-peer networking, a consensus algorithm (like proof-of-work or proof-of-stake), transaction handling, encryption, or any form of reward system for adding new blocks. This is just a basic data structure with the property that each block contains the hash of the previous block, creating a chain of blocks that can't be modified without invalidating the rest of the chain.
"""

import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.genesis_block = self.create_genesis_block()
        self.blocks = [self.genesis_block]

    @staticmethod
    def create_genesis_block():
        return Block(0, "0", int(time.time()), "Genesis Block", "")

    @staticmethod
    def calculate_hash(index, previous_hash, timestamp, data):
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def add_block(self, data):
        index = len(self.blocks)
        previous_hash = self.blocks[index - 1].hash
        timestamp = int(time.time())
        hash = self.calculate_hash(index, previous_hash, timestamp, data)
        block = Block(index, previous_hash, timestamp, data, hash)
        self.blocks.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            previous_block = self.blocks[i - 1]
            if current_block.hash != self.calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True


# Create a new Blockchain
blockchain = Blockchain()

# Add some blocks
blockchain.add_block("Block 1")
blockchain.add_block("Block 2")
blockchain.add_block("Block 3")

# Verify the blockchain is valid
print(blockchain.is_chain_valid())  # Should return True

# Let's tamper with the second block
blockchain.blocks[1].data = "Fake Block"

# Now the blockchain should be invalid
print(blockchain.is_chain_valid())  # Should return False
