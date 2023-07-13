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
        if not self.are_transactions_valid(transactions):
            print("Invalid transactions")
            return

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
                if transaction.from_address == 'System':
                    if transaction.to_address not in balances:
                        balances[transaction.to_address] = 0
                    balances[transaction.to_address] += transaction.amount
                else:
                    if transaction.from_address not in balances:
                        balances[transaction.from_address] = 0
                    if transaction.to_address not in balances:
                        balances[transaction.to_address] = 0
                    balances[transaction.from_address] -= transaction.amount
                    balances[transaction.to_address] += transaction.amount
        return balances

    def are_transactions_valid(self, transactions):
        """
        Since we're simulating an initial funding by a 'System' entity, the transactions from the 'System' should 
        not be considered invalid. We modify the are_transactions_valid method to allow the transactions from the 
        'System' regardless of the 'System' balance.
        This change should prevent the "Invalid transactions" messages and allow you to create the initial blockchain. 
        Remember that the number of blocks in the chain depends on how many blocks are successfully added, which in turn 
        depends on the validity of the transactions in those blocks. Therefore, if you have invalid transactions, you may 
        not have as many blocks in the blockchain as expected, resulting in the IndexError.
        """
        balances = self.calculate_balances(transactions)
        for transaction in transactions:
            if transaction.from_address == 'System':
                continue
            from_balance = balances.get(transaction.from_address, 0)
            if from_balance < transaction.amount:
                return False
        return True


"""
In this example, Alice sends 50 coins to Bob and Bob sends 25 to Charlie in the first block of transactions. In 
the second block, Charlie sends 10 coins back to Alice, and Alice sends 5 more coins to Bob. After these 
transactions, the balance of each person can be calculated.

consider a scenario where Alice, Bob, and Charlie already have some balance before starting the transactions. We can 
simulate this situation by creating a genesis block with transactions that credit each person with some coins.
In this code, we're simulating a 'System' entity that gives each participant 100 coins in the genesis block. Now, 
each subsequent transaction should be valid given the participants don't try to spend more coins than they have.
"""

# Create a new Blockchain
blockchain = Blockchain()

# Create a genesis block with initial balances
blockchain.add_block([Transaction("System", "Alice", 100), Transaction("System", "Bob", 100), Transaction("System", "Charlie", 100)])

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
