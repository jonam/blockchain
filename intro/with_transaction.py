"""
Let's introduce the concept of transactions in this basic blockchain model. We'll create a Transaction class and modify the Block and Blockchain classes to handle transactions.

Note that, for simplicity, we are not verifying whether the from_address actually has enough balance for the transactions. In a real-world blockchain like Bitcoin or Ethereum, before adding a transaction to a block, you'd need to check whether the sender has a sufficient balance. You'd also need to implement a reward system for the miner who adds the new block. This example is meant to be as simple as possible while introducing the concept of transactions.
"""

import hashlib
import time

class Transaction:
    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.genesis_block = self.create_genesis_block()
        self.blocks = [self.genesis_block]

    @staticmethod
    def create_genesis_block():
        return Block(0, "0", int(time.time()), [], "")

    @staticmethod
    def calculate_hash(index, previous_hash, timestamp, transactions):
        transaction_data = "".join(str(transaction.__dict__) for transaction in transactions)
        value = str(index) + str(previous_hash) + str(timestamp) + transaction_data
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def add_block(self, transactions):
        index = len(self.blocks)
        previous_hash = self.blocks[index - 1].hash
        timestamp = int(time.time())
        hash = self.calculate_hash(index, previous_hash, timestamp, transactions)
        block = Block(index, previous_hash, timestamp, transactions, hash)
        self.blocks.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            previous_block = self.blocks[i - 1]
            if current_block.hash != self.calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.transactions):
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# Create a new Blockchain
blockchain = Blockchain()

# Add some blocks with transactions
blockchain.add_block([Transaction("Alice", "Bob", 50), Transaction("Bob", "Charlie", 25)])
blockchain.add_block([Transaction("Charlie", "Alice", 10), Transaction("Alice", "Bob", 5)])

# Verify the blockchain is valid
print(blockchain.is_chain_valid())  # Should return True

# Let's tamper with the second block
blockchain.blocks[1].transactions[0].amount = 1000

# Now the blockchain should be invalid
print(blockchain.is_chain_valid())  # Should return False
