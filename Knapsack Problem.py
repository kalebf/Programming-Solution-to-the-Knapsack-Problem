import time
import random
import matplotlib.pyplot as plt
import numpy as np

def generate_test_case(n_items, max_weight=50, max_value=100): # Generate random weights and values
    weights = [random.randint(1, max_weight) for _ in range(n_items)]
    values = [random.randint(1, max_value) for _ in range(n_items)]
    capacity = random.randint(max_weight, max_weight * 3)
    return weights, values, capacity

def measure_time(func, *args): # Measure execution time of a function
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return result, end - start

def knapsack_01(weights, values, capacity):
    """
    Solves 0/1 Knapsack using dynamic programming.
    Returns max value and list of selected items.
    """
    n = len(weights) # number of items
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]   # DP table for 0/1 Knapsack

    # Fill DP table
    for i in range(1, n + 1):   # Iterate over items
        w = weights[i - 1] # weight of current item
        v = values[i - 1]  # value of current item  
        for c in range(capacity + 1): # Iterate over all capacities
            if w > c: # If item can't fit in current capacity
                dp[i][c] = dp[i - 1][c] # Exclude item
            else: # If item can fit
                dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + v) # Max of including or excluding item

    # Find max value
    max_value = dp[n][capacity]

    # Backtrack to find items
    selected = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            selected.append(i - 1)
            c -= weights[i - 1]

    return max_value, selected

def knapsack_unbounded(weights, values, capacity):
    """
    Solves Unbounded Knapsack using DP.
    Items can be reused.
    """
    dp = [0] * (capacity + 1) # DP array for Unbounded Knapsack
    item_trace = [-1] * (capacity + 1) # Traceback array for item selection

    for c in range(1, capacity + 1): # Iterate over all capacities
        for i in range(len(weights)): # Iterate over all items
            if weights[i] <= c: # If item can fit in current capacity

    
                if dp[c] < dp[c - weights[i]] + values[i]: # Check if including item i is better
                    dp[c] = dp[c - weights[i]] + values[i]  # Update DP value
                    item_trace[c] = i # Trace back the item used

    # Reconstruct items
    selected_counts = [0] * len(weights) # count of each item selected
    c = capacity
    while c > 0 and item_trace[c] != -1: # while there's an item to trace back
        idx = item_trace[c]
        selected_counts[idx] += 1
        c -= weights[idx]

    return dp[capacity], selected_counts

def run_comprehensive_tests():
    """Run tests with varying input sizes and collect timing data."""
    input_sizes = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    times_01 = []
    times_unbounded = []
    values_01 = []
    values_unbounded = []
    
    print("Running comprehensive tests...")
    print("-" * 50)
    
    for n in input_sizes:
        weights, values, capacity = generate_test_case(n, max_weight=30, max_value=50) # Smaller weights/values for larger n
        
        # Measure 0/1 Knapsack
        result_01, time_01 = measure_time(knapsack_01, weights, values, capacity) # Measure 0/1 Knapsack
        max_value_01, _ = result_01
        
        # Measure Unbounded Knapsack
        result_unb, time_unb = measure_time(knapsack_unbounded, weights, values, capacity) # Measure Unbounded Knapsack
        max_value_unb, _ = result_unb
        
        times_01.append(time_01)
        times_unbounded.append(time_unb)
        values_01.append(max_value_01)
        values_unbounded.append(max_value_unb)
        
        print(f"n={n:3d}: 0/1: {time_01:.6f}s, Unbounded: {time_unb:.6f}s")
    
    return input_sizes, times_01, times_unbounded, values_01, values_unbounded

def analyze_time_complexity(times_01, times_unbounded, input_sizes):
    """Analyze and print time complexity observations."""
    print("\n" + "=" * 60)
    print("TIME COMPLEXITY ANALYSIS")
    print("=" * 60)
    
    print("\n1. 0/1 Knapsack Complexity:")
    print("   - Theoretical: O(n * capacity)")
    print("   - Observations:")
    
    # Calculate ratios
    for i in range(1, len(input_sizes)): # start from second element
        n_ratio = input_sizes[i] / input_sizes[i-1] # ratio of input sizes
        time_ratio = times_01[i] / times_01[i-1] # ratio of times
        print(f"     n {input_sizes[i-1]}→{input_sizes[i]}: Time ratio = {time_ratio:.2f}x (n ratio = {n_ratio:.2f}x)")
    
    print("\n2. Unbounded Knapsack Complexity:")
    print("   - Theoretical: O(n * capacity)")
    print("   - Observations:")
    
    for i in range(1, len(input_sizes)): # start from second element
        n_ratio = input_sizes[i] / input_sizes[i-1] # ratio of input sizes
        time_ratio = times_unbounded[i] / times_unbounded[i-1] # ratio of times
        print(f"     n {input_sizes[i-1]}→{input_sizes[i]}: Time ratio = {time_ratio:.2f}x (n ratio = {n_ratio:.2f}x)")

def plot_results(input_sizes, times_01, times_unbounded):
    """Create visualizations of execution times."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Linear scale
    ax1.plot(input_sizes, times_01, 'b-o', label='0/1 Knapsack', linewidth=2)
    ax1.plot(input_sizes, times_unbounded, 'r-s', label='Unbounded Knapsack', linewidth=2)
    ax1.set_xlabel('Number of Items (n)')
    ax1.set_ylabel('Execution Time (seconds)')
    ax1.set_title('Execution Time vs Input Size')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Log-log scale to check polynomial behavior
    ax2.loglog(input_sizes, times_01, 'b-o', label='0/1 Knapsack', linewidth=2)
    ax2.loglog(input_sizes, times_unbounded, 'r-s', label='Unbounded Knapsack', linewidth=2)
    ax2.set_xlabel('Number of Items (n)')
    ax2.set_ylabel('Execution Time (seconds)')
    ax2.set_title('Log-Log Plot (Checking Polynomial Growth)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('knapsack_performance.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main function to run comprehensive analysis."""
    print("DYNAMIC PROGRAMMING: KNAPSACK PROBLEM ANALYSIS")
    print("=" * 50)
    
    # Run comprehensive tests
    input_sizes, times_01, times_unbounded, values_01, values_unbounded = run_comprehensive_tests()
    
    # Analyze time complexity
    analyze_time_complexity(times_01, times_unbounded, input_sizes)
    
    # Create visualizations
    plot_results(input_sizes, times_01, times_unbounded)
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"\nMaximum execution time for 0/1 Knapsack: {max(times_01):.6f}s")
    print(f"Maximum execution time for Unbounded Knapsack: {max(times_unbounded):.6f}s")
    print(f"\nAverage speedup (Unbounded/0/1): {np.mean(np.array(times_unbounded)/np.array(times_01)):.2f}x")
    
    return {
        'input_sizes': input_sizes,
        'times_01': times_01,
        'times_unbounded': times_unbounded,
        'values_01': values_01,
        'values_unbounded': values_unbounded
    }

if __name__ == "__main__":
    # Run your original test
    weights, values, capacity = generate_test_case(5)
    print("Weights:", weights)
    print("Values:", values)        
    print("Capacity:", capacity)
    
    max_value_01, selected_items_01 = knapsack_01(weights, values, capacity)
    print("\n0/1 Knapsack:")
    print("Max Value:", max_value_01)
    print("Selected Items:", selected_items_01)
    time_01 = measure_time(knapsack_01, weights, values, capacity)[1]
    print(f"Execution Time: {time_01:.6f} seconds")
    
    max_value_unbounded, selected_counts_unbounded = knapsack_unbounded(weights, values, capacity)
    print("\nUnbounded Knapsack:")
    print("Max Value:", max_value_unbounded)
    print("Selected Item Counts:", selected_counts_unbounded)
    time_unbounded = measure_time(knapsack_unbounded, weights, values, capacity)[1]
    print(f"Execution Time: {time_unbounded:.6f} seconds")
    
    # Run comprehensive analysis
    print("\n" + "=" * 60)
    print("COMPREHENSIVE ANALYSIS")
    print("=" * 60)
    results = main()