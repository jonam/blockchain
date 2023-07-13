"""
Adding cryptographic proofs to our blockchain would add an additional layer of security and authenticity. Here's how we can introduce cryptographic hashing and proof of work:

Firstly, we'll need to import the hashlib module for our cryptographic needs. Each block will have a previous_hash attribute to store the hash of the previous block, and we'll create a hash method to calculate a block's hash based on its content. We'll also introduce a proof attribute and a method to calculate a proof of work.

Proof of work is a concept used in blockchains to prevent spam and abuse. It requires participants to do some work, typically solving a difficult puzzle, in order to add blocks. The most commonly used form is a hash puzzle, where the goal is to find a number that, when hashed together with the rest of the block, produces a hash with a certain number of leading zeroes. This is hard to calculate but easy to verify, providing a basic level of security for the blockchain.

In this version of the code, each block includes a proof of work, and the add_block function will not add a block until it has found a valid proof of work. The is_chain_valid function also checks whether each block's previous_hash matches the hash of the previous block, providing additional verification of the blockchain's integrity.

The difficulty level for the proof of work puzzle is set to 4, which means it requires finding a number that produces a hash with 4 leading zeroes. This might take a few seconds or more to calculate depending on your machine's capabilities.

This is still a simplified version of a blockchain. Real blockchains like Bitcoin use similar concepts, but with more complex and secure mechanisms for adding blocks, verifying transactions, handling multiple participants, and more.
"""

import hashlib
import json
from time import time

class Transaction:
    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount

    def to_dict(self):
        return {
            'from_address': self.from_address,
            'to_address': self.to_address,
            'amount': self.amount,
        }

class Block:
    def __init__(self, transactions, previous_hash):
        self.timestamp = time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = 0

    def hash(self):
        """
        Here's how the hash method works:

        1. It creates a copy of the block's dictionary (self.__dict__), which includes all its properties 
           (timestamp, transactions, previous hash, and proof).
        2. It replaces the list of Transaction objects with a list of dictionaries representing each 
           transaction. This is done with a list comprehension ([tx.to_dict() for tx in self.transactions]), 
           which calls to_dict on each transaction (tx) in the block's transactions (self.transactions).
        3. It converts the modified dictionary to a JSON string, sorts the keys to ensure consistency, and 
           encodes it to bytes.
        4. It hashes the bytes using SHA-256 and returns the hexadecimal representation of the hash.
        """
        block_dict = self.__dict__.copy()
        block_dict['transactions'] = [tx.to_dict() for tx in self.transactions]
        block_string = json.dumps(block_dict, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.blocks = [self.genesis_block()]

    def genesis_block(self):
        transactions = [Transaction("System", "Alice", 100), Transaction("System", "Bob", 100), Transaction("System", "Charlie", 100)]
        genesis_block = Block(transactions, "0")
        genesis_block.proof = self.proof_of_work(genesis_block)
        return genesis_block

    def add_block(self, transactions):
        if not self.are_transactions_valid(transactions):
            print("Invalid transactions")
            return
        previous_hash = self.blocks[-1].hash()
        new_block = Block(transactions, previous_hash)
        # new_block.proof = self.proof_of_work(new_block)
        start = time()  # Start timing
        new_block.proof = self.proof_of_work(new_block, difficulty=7)  # Increase difficulty
        end = time()  # End timing

        print(f"Proof of work solved in {end - start} seconds")
        self.blocks.append(new_block)

    def calculate_balances(self, pending_transactions=None):
        balances = {}
        for block in self.blocks:
            for transaction in block.transactions:
                if transaction.from_address not in balances:
                    balances[transaction.from_address] = 0
                if transaction.to_address not in balances:
                    balances[transaction.to_address] = 0
                balances[transaction.from_address] -= transaction.amount
                balances[transaction.to_address] += transaction.amount
        if pending_transactions:
            for transaction in pending_transactions:
                if transaction.from_address not in balances:
                    balances[transaction.from_address] = 0
                if transaction.to_address not in balances:
                    balances[transaction.to_address] = 0
                balances[transaction.from_address] -= transaction.amount
                balances[transaction.to_address] += transaction.amount
        return balances

    def are_transactions_valid(self, transactions):
        balances = self.calculate_balances(transactions)
        for transaction in transactions:
            if transaction.from_address == 'System':
                continue
            from_balance = balances.get(transaction.from_address, 0)
            if from_balance < transaction.amount:
                return False
        return True

    def proof_of_work(self, block, difficulty=4):
        block.proof = 0
        while not block.hash()[:difficulty] == "0" * difficulty:
            block.proof += 1
        return block.proof

    def is_chain_valid(self):
        for i in range(1, len(self.blocks)):
            current = self.blocks[i]
            previous = self.blocks[i-1]
            if current.hash() != current.hash():
                return False
            if current.previous_hash != previous.hash():
                return False
        return True

# Create a new Blockchain
blockchain = Blockchain()

# Add some blocks with transactions
blockchain.add_block([Transaction("Alice", "Bob", 50), Transaction("Bob", "Charlie", 25)])
blockchain.add_block([Transaction("Charlie", "Alice", 10), Transaction("Alice", "Bob", 5)])

# Verify the blockchain is valid
print(blockchain.is_chain_valid())  # Should return True

# Check the balances
print(blockchain.calculate_balances())

# Let's tamper with the second block (third, if you count the genesis block)
blockchain.blocks[2].transactions[0].amount = 1000

# Now the blockchain should be invalid
print(blockchain.is_chain_valid())  # Should return False
