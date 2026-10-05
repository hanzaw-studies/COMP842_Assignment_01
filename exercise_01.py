import hashlib
import time
import pickle

def hash_data(data):
    # Generate a SHA-256 hash for a given string.
    return hashlib.sha256(data.encode()).hexdigest()

class Block:
    def __init__(self, height, transactions, previous_hash):
        self.height = height
        self.timestamp = int(time.time())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = self.compute_merkle_root(transactions)
        self.hash = self.compute_hash()

    def compute_merkle_root(self, transactions):
        # Computes the Merkle Root for the block's transactions 
        if len(transactions) == 0:
            return ""

        hashes = [hash_data(tx) for tx in transactions]

        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1]) # Duplicate the last hash if odd

            next_level = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i + 1]
                next_level.append(hash_data(combined))

            hashes = next_level
            
        return hashes[0]

    def compute_hash(self):
        # Generate the SHA-256 hash of the block's current state.
        block_data = {
            "height": self.height,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "transactions": self.transactions
        }

        # Convert dictionary to bytes before hashing
        block_bytes = pickle.dumps(block_data)
        return hashlib.sha256(block_bytes).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Initialises the blockchain with the genesis block.
        genesis_block = Block(1, ["Genesis Block - Initialisation"], "0" * 64)
        self.chain.append(genesis_block)

    def append_block(self, transactions):
        # Appends a new block to the chain using the previous block's hash.
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain) + 1, transactions, previous_block.hash)
        self.chain.append(new_block)

    def validate_chain(self):
        # Validate the integrity of the entire blockchain
        for i in range(0, len(self.chain)):
            current_block = self.chain[i]

            # 1. Validate Merkle Root
            recomputed_merkle = current_block.compute_merkle_root(
                current_block.transactions
            )
            if current_block.merkle_root != recomputed_merkle:
                print(
                    f"Validation Failed at Block {current_block.height}: Merkle Root "
                    f"is invalid (Transaction data was tampered with)."
                )
                return False

            # 2. Validate Current Block Hash
            if current_block.hash != current_block.compute_hash():
                print(
                    f"Validation Failed at Block {current_block.height}: Block hash "
                    f"is invalid."
                )
                return False

            # 3. Validate Hash Pointer Linkage (skip for the genesis block,
            # which has no previous block to link to)
            if i > 0:
                previous_block = self.chain[i - 1]
                if current_block.previous_hash != previous_block.hash:
                    print(
                        f"Validation Failed at Block {current_block.height}: Previous "
                        f"hash pointer is broken."
                    )
                    return False

        print("Validation Successful: The blockchain is valid and secure.")
        return True

    def display_chain(self):
        # Prints the entire blockchain in a readable format.
        for block in self.chain:
            print(f"Block {block.height}")
            print(f"  Transactions : {block.transactions}")
            print(f"  Merkle Root  : {block.merkle_root}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Current Hash : {block.hash}")
            print("-" * 65)
# --- Execution and Testing ---

# Create the blockchain and append blocks to reach a total of 10
my_blockchain = Blockchain()

# Block transaction data — Blocks 4 and 7 are given multiple transactions
block_transactions = [
    [f"Payment of $20 from User2 to User3"],                                  # Block 2
    [f"Payment of $30 from User3 to User4"],                                  # Block 3
    [f"Payment of $40 from User4 to User5", "Payment of $5 from User4 to User9"],  # Block 4
    [f"Payment of $50 from User5 to User6"],                                  # Block 5
    [f"Payment of $60 from User6 to User7"],                                  # Block 6
    [f"Payment of $70 from User7 to User8",
     "Payment of $15 from User7 to User2",
     "Payment of $8 from User7 to User10"],                                   # Block 7 (odd count)
    [f"Payment of $80 from User8 to User9"],                                  # Block 8
    [f"Payment of $90 from User9 to User10"],                                 # Block 9
    [f"Payment of $100 from User10 to User11"],                               # Block 10
]

for tx_data in block_transactions:
    my_blockchain.append_block(tx_data)

print("--- Step 1: Initial Blockchain Validation ---\n")
my_blockchain.display_chain()
my_blockchain.validate_chain()

print("\n--- Step 2: Simulating Tampering ---\n")
print("Modifying transaction data in Block 5...")
# Modifying the 5th block (Index 4) without recalculating its stored
# Merkle Root or Hash
my_blockchain.chain[4].transactions[0] = "Tampered Transaction: Hacker steals $1,000,000"

print("\n--- Step 3: Modified Blockchain and Validation Results ---\n")
my_blockchain.display_chain()
my_blockchain.validate_chain()
