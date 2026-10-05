import hashlib
import time
import statistics

def mine_block(block_data, difficulty):
    """Mines a block by incrementing a nonce until the hash meets the difficulty."""
    prefix = '0' * difficulty
    nonce = 0
    start_time = time.time()
    
    while True:
        # Concatenate block data and nonce
        text = block_data + str(nonce)
        hash_result = hashlib.sha256(text.encode()).hexdigest()
        
        # Increment nonce for the next attempt if it fails
        nonce += 1
        
        # Check if the hash satisfies the difficulty
        if hash_result.startswith(prefix):
            end_time = time.time()
            mining_time = end_time - start_time
            return mining_time, hash_result, nonce

def run_experiment():
    difficulties = [2, 3, 4, 5]
    num_blocks = 30
    
    print("Starting Proof of Work Experiment...")
    print("-" * 60)
    
    for diff in difficulties:
        mining_times = []
        hash_attempts = []
        
        print(f"\nMining 30 blocks at Difficulty {diff} (Leading Zeros)...")
        
        for i in range(num_blocks):
            # Using unique data for each block to ensure unique hashes
            data = f"COMP842 Block {i} at Diff {diff}"
            m_time, valid_hash, attempts = mine_block(data, diff)
            
            mining_times.append(m_time)
            hash_attempts.append(attempts)
            
            # Print the first block's result as a sample for the console output
            if i == 0:
                print(f"  [Sample Block 1] Hash: {valid_hash} | Attempts: {attempts} | Time: {m_time:.4f}s")
                
        # Calculate Metrics
        avg_time = statistics.mean(mining_times)
        min_time = min(mining_times)
        max_time = max(mining_times)
        std_dev = statistics.stdev(mining_times)
        
        total_time = sum(mining_times)
        total_hashes = sum(hash_attempts)
        throughput = total_hashes / total_time if total_time > 0 else 0
        
        theoretical_attempts = 16 ** diff
        measured_avg_attempts = statistics.mean(hash_attempts)
        
        print(f"\n--- Metrics for Difficulty {diff} ---")
        print(f"Average Mining Time   : {avg_time:.5f} seconds")
        print(f"Minimum Mining Time   : {min_time:.5f} seconds")
        print(f"Maximum Mining Time   : {max_time:.5f} seconds")
        print(f"Standard Deviation    : {std_dev:.5f} seconds")
        print(f"Mining Throughput     : {throughput:,.2f} hashes/sec")
        print(f"Measured Avg Attempts : {measured_avg_attempts:,.2f}")
        print(f"Theoretical Attempts  : {theoretical_attempts:,}")
        print("-" * 60)

if __name__ == "__main__":
    run_experiment()