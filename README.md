# Complete Guide to Data Structure & Algorithm Patterns

*A comprehensive collection of all essential algorithmic patterns with Python implementations*



## Table of Contents

**Part I: Array & String Patterns**
1. Two Pointers Pattern
2. Sliding Window Pattern
3. Fast & Slow Pointers Pattern
4. Cyclic Sort Pattern

**Part II: Search & Sort Patterns** 
5. Binary Search Pattern
6. Quick Select Pattern
7. Merge Intervals Pattern

**Part III: Tree & Graph Patterns**
8. Depth-First Search (DFS)
9. Breadth-First Search (BFS) 
10. Tree Traversal Patterns
11. Topological Sort Pattern
12. Union-Find Pattern

**Part IV: Dynamic Programming & Optimization**
13. Dynamic Programming Pattern
14. Kadane's Algorithm Pattern
15. Divide & Conquer Pattern

**Part V: Backtracking & Enumeration**
16. Backtracking Pattern
17. Subsets & Combinations Pattern

**Part VI: Greedy & Selection**
18. Greedy Algorithm Pattern
19. Top K Elements Pattern
20. K-way Merge Pattern

**Part VII: Advanced Data Structure Patterns**
21. Trie (Prefix Tree) Pattern
22. Monotonic Stack Pattern
23. Heap Patterns
24. Two Heaps Pattern

**Part VIII: Mathematical & Bitwise Patterns**
25. Bitwise XOR Pattern
26. Mathematical Patterns



# Part I: Array & String Patterns

## 1. Two Pointers Pattern

**When to use:** Finding pairs, triplets, or comparing elements from different positions in sorted arrays or strings. This pattern is your first choice when you see problems asking about pairs or when you need to compare elements from both ends.

**Key insight:** Instead of using nested loops which give us O(n²) time complexity, we can use two pointers moving toward each other or in the same direction to achieve O(n) time complexity. Think of it as having two fingers on a book - one at the beginning and one at the end, moving them based on what you find.

**Problem types:** Pair with target sum, removing duplicates, palindrome verification, container problems.

```python
def two_sum_sorted(nums, target):
    """
    Find two numbers in sorted array that add up to target.
    
    The beauty of this approach is that we eliminate half the remaining 
    possibilities with each comparison, similar to binary search logic.
    
    Time: O(n), Space: O(1)
    """
    left = 0                    # Start from smallest number
    right = len(nums) - 1       # Start from largest number
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum == target:
            return [left, right]    # Perfect! Found our pair
        elif current_sum < target:
            left += 1               # Need bigger sum, move left pointer right
        else:
            right -= 1              # Need smaller sum, move right pointer left
    
    return []  # No valid pair exists

def three_sum(nums):
    """
    Find all unique triplets that sum to zero.
    
    This extends two-pointer by fixing one number and finding pairs
    for the remaining target. Notice how we handle duplicates.
    
    Time: O(n²), Space: O(1) excluding output
    """
    nums.sort()  # Sorting enables two-pointer approach
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicate values for first number
        if i > 0 and nums[i] == nums[i-1]:
            continue
            
        left, right = i + 1, len(nums) - 1
        target = -nums[i]  # We want nums[left] + nums[right] = target
        
        while left < right:
            current_sum = nums[left] + nums[right]
            
            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for second and third numbers
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result

# Example usage and testing
nums = [1, 2, 3, 4, 6]
target = 6
result = two_sum_sorted(nums, target)
print(f"Two sum indices: {result}")  # [1, 3] -> nums[1] + nums[3] = 2 + 4 = 6

triplet_nums = [-1, 0, 1, 2, -1, -4]
triplets = three_sum(triplet_nums)
print(f"Three sum triplets: {triplets}")  # [[-1, -1, 2], [-1, 0, 1]]
```



## 2. Sliding Window Pattern

**When to use:** Problems involving subarrays or substrings of specific sizes, or finding optimal subarrays based on certain conditions. This pattern is perfect when you need to examine contiguous sequences within arrays or strings.

**Key insight:** Instead of recalculating everything for each possible window position, we slide the window by removing the leftmost element and adding the rightmost element. This transforms O(n×k) brute force solutions into O(n) elegant solutions.

**Problem types:** Maximum/minimum subarray sum, longest substring problems, anagram problems.

```python
def max_sum_subarray(nums, k):
    """
    Find maximum sum of any contiguous subarray of size k.
    
    The sliding technique: imagine a window frame sliding across
    the array. Instead of recalculating the sum for each position,
    we subtract what leaves and add what enters.
    
    Time: O(n), Space: O(1)
    """
    if len(nums) < k:
        return None
    
    # Calculate sum of first window
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    # Slide the window: remove leftmost, add rightmost
    for i in range(k, len(nums)):
        # This is the key insight: update incrementally
        window_sum = window_sum - nums[i - k] + nums[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum

def longest_substring_without_repeating(s):
    """
    Find length of longest substring without repeating characters.
    
    This uses a variable-sized sliding window. We expand the window
    by moving the right pointer and shrink it when we find duplicates.
    
    Time: O(n), Space: O(min(m,n)) where m is charset size
    """
    char_index = {}  # Maps character to its most recent index
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        current_char = s[right]
        
        # If character is repeated and within current window
        if current_char in char_index and char_index[current_char] >= left:
            # Move left pointer past the previous occurrence
            left = char_index[current_char] + 1
        
        # Update character's most recent index
        char_index[current_char] = right
        
        # Update maximum length found so far
        max_length = max(max_length, right - left + 1)
    
    return max_length

def min_window_substring(s, t):
    """
    Find minimum window in s that contains all characters of t.
    
    This demonstrates the expand-contract pattern: expand until
    valid, then contract while maintaining validity.
    
    Time: O(s + t), Space: O(s + t)
    """
    if len(s) < len(t):
        return ""
    
    # Count characters needed
    char_count = {}
    for char in t:
        char_count[char] = char_count.get(char, 0) + 1
    
    required_chars = len(char_count)  # Number of unique chars in t
    formed_chars = 0  # Number of unique chars in current window with desired frequency
    
    window_counts = {}  # Character frequencies in current window
    
    left = 0
    min_len = float('inf')
    min_left = 0
    
    for right in range(len(s)):
        # Expand window by including right character
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        # Check if current character's frequency matches required frequency
        if char in char_count and window_counts[char] == char_count[char]:
            formed_chars += 1
        
        # Contract window while it's valid
        while left <= right and formed_chars == required_chars:
            # Update minimum window if current is smaller
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            # Remove left character from window
            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in char_count and window_counts[left_char] < char_count[left_char]:
                formed_chars -= 1
            
            left += 1
    
    return "" if min_len == float('inf') else s[min_left:min_left + min_len]

# Example usage
nums = [2, 1, 5, 1, 3, 2]
k = 3
result = max_sum_subarray(nums, k)
print(f"Maximum sum of subarray size {k}: {result}")  # 9 (5+1+3)

s = "abcabcbb"
result = longest_substring_without_repeating(s)
print(f"Longest substring length: {result}")  # 3 ("abc")

s, t = "ADOBECODEBANC", "ABC"
result = min_window_substring(s, t)
print(f"Minimum window: '{result}'")  # "BANC"
```



## 3. Fast & Slow Pointers Pattern

**When to use:** Detecting cycles in linked lists, finding middle elements, or problems where you need to move at different speeds through a data structure. This pattern is particularly elegant for linked list problems.

**Key insight:** Use two pointers moving at different speeds. The fast pointer moves two steps while the slow pointer moves one step. If there's a cycle, they'll eventually meet. Think of it like two runners on a circular track - the faster runner will lap the slower one.

**Problem types:** Cycle detection, finding middle of linked list, palindrome linked lists.

```python
class ListNode:
    """Definition for singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle(head):
    """
    Detect if linked list has a cycle using Floyd's algorithm.
    
    The mathematical insight: if there's a cycle, the fast pointer
    will eventually catch up to the slow pointer from behind.
    
    Time: O(n), Space: O(1)
    """
    if not head or not head.next:
        return False
    
    slow = head          # Moves one step at a time
    fast = head.next     # Moves two steps at a time
    
    while fast and fast.next:
        if slow == fast:
            return True  # Cycle detected!
        
        slow = slow.next      # One step
        fast = fast.next.next # Two steps
    
    return False  # Reached end, no cycle

def find_cycle_start(head):
    """
    Find the starting node of cycle in linked list.
    
    Beautiful mathematical property: after detecting cycle,
    if you start one pointer from head and keep other at meeting point,
    they'll meet exactly at cycle start.
    
    Time: O(n), Space: O(1)
    """
    if not head or not head.next:
        return None
    
    # Phase 1: Detect if cycle exists
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle found
    
    # Phase 2: Find cycle start
    # Mathematical proof: distance from head to cycle start equals
    # distance from meeting point to cycle start
    start = head
    while start != slow:
        start = start.next
        slow = slow.next
    
    return start

def find_middle_node(head):
    """
    Find middle node of linked list.
    
    When fast pointer reaches end, slow pointer is at middle.
    For even length, this returns the second middle node.
    
    Time: O(n), Space: O(1)
    """
    if not head:
        return None
    
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next      # One step
        fast = fast.next.next # Two steps
    
    return slow  # Slow is now at middle

def is_palindrome_linkedlist(head):
    """
    Check if linked list is palindrome.
    
    Strategy: Find middle, reverse second half, compare both halves.
    This showcases how fast-slow pointers enable complex operations.
    
    Time: O(n), Space: O(1)
    """
    if not head or not head.next:
        return True
    
    # Find middle using fast-slow pointers
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    def reverse_list(node):
        prev = None
        while node:
            next_temp = node.next
            node.next = prev
            prev = node
            node = next_temp
        return prev
    
    second_half = reverse_list(slow)
    
    # Compare both halves
    first_half = head
    while second_half:  # Second half might be shorter
        if first_half.val != second_half.val:
            return False
        first_half = first_half.next
        second_half = second_half.next
    
    return True

# Example usage with linked list creation helper
def create_linked_list(values):
    """Helper to create linked list from array."""
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    
    return head

# Test palindrome detection
head = create_linked_list([1, 2, 3, 2, 1])
print(f"Is palindrome: {is_palindrome_linkedlist(head)}")  # True

head = create_linked_list([1, 2, 3, 4, 5])
middle = find_middle_node(head)
print(f"Middle node value: {middle.val}")  # 3
```



## 4. Cyclic Sort Pattern

**When to use:** Problems involving arrays containing numbers in a given range, typically 1 to n. This pattern is perfect when you need to place elements at their correct positions.

**Key insight:** If we have n numbers ranging from 1 to n, each number should ideally be at index (number - 1). We can achieve sorting in O(n) time by placing each number at its correct position through swaps.

**Problem types:** Finding missing numbers, duplicates, or corrupt data in arrays with specific ranges.

```python
def cyclic_sort(nums):
    """
    Sort array containing numbers from 1 to n using cyclic sort.
    
    The key insight: number 'i' should be at index 'i-1'.
    We keep swapping until each number reaches its correct position.
    
    Time: O(n), Space: O(1)
    """
    i = 0
    while i < len(nums):
        # Calculate where current number should be placed
        correct_index = nums[i] - 1
        
        # If current number is not at its correct position
        if nums[i] != nums[correct_index]:
            # Swap current number to its correct position
            nums[i], nums[correct_index] = nums[correct_index], nums[i]
        else:
            # Current number is at correct position, move to next
            i += 1
    
    return nums

def find_missing_number(nums):
    """
    Find missing number in array containing n distinct numbers from 0 to n.
    
    We place each number at its correct position, then find the position
    that doesn't contain the expected number.
    
    Time: O(n), Space: O(1)
    """
    n = len(nums)
    i = 0
    
    # Place each number at its correct position
    while i < n:
        # For range 0 to n, number should be at its own index
        correct_index = nums[i]
        
        # Only swap if number is in valid range and not at correct position
        if nums[i] < n and nums[i] != nums[correct_index]:
            nums[i], nums[correct_index] = nums[correct_index], nums[i]
        else:
            i += 1
    
    # Find the first position where number doesn't match index
    for i in range(n):
        if nums[i] != i:
            return i
    
    # If all positions 0 to n-1 are correct, missing number is n
    return n

def find_all_duplicates(nums):
    """
    Find all duplicates in array where elements are in range [1, n].
    
    We use the fact that each number should appear at index (number - 1).
    After sorting, duplicates will be at wrong positions.
    
    Time: O(n), Space: O(1) excluding output array
    """
    i = 0
    
    # Place numbers at their correct positions
    while i < len(nums):
        correct_index = nums[i] - 1
        
        if nums[i] != nums[correct_index]:
            nums[i], nums[correct_index] = nums[correct_index], nums[i]
        else:
            i += 1
    
    # Find all numbers that are not at their correct positions
    duplicates = []
    for i in range(len(nums)):
        if nums[i] != i + 1:
            duplicates.append(nums[i])
    
    return duplicates

def find_corrupt_pair(nums):
    """
    Find the corrupt pair in array where one number is duplicated
    and one number is missing from range [1, n].
    
    Returns [duplicate, missing]
    
    Time: O(n), Space: O(1)
    """
    i = 0
    
    # Sort using cyclic sort
    while i < len(nums):
        correct_index = nums[i] - 1
        
        if nums[i] != nums[correct_index]:
            nums[i], nums[correct_index] = nums[correct_index], nums[i]
        else:
            i += 1
    
    # After sorting, find the position with wrong number
    for i in range(len(nums)):
        if nums[i] != i + 1:
            return [nums[i], i + 1]  # [duplicate, missing]
    
    return []

# Example usage and demonstrations
print("=== Cyclic Sort Examples ===")

# Basic cyclic sort
nums = [3, 1, 5, 4, 2]
sorted_nums = cyclic_sort(nums.copy())
print(f"Original: {[3, 1, 5, 4, 2]}")
print(f"Sorted: {sorted_nums}")  # [1, 2, 3, 4, 5]

# Find missing number
nums = [4, 0, 3, 1]
missing = find_missing_number(nums.copy())
print(f"Missing number in {[4, 0, 3, 1]}: {missing}")  # 2

# Find duplicates
nums = [4, 3, 2, 7, 8, 2, 3, 1]
duplicates = find_all_duplicates(nums.copy())
print(f"Duplicates in {[4, 3, 2, 7, 8, 2, 3, 1]}: {duplicates}")  # [2, 3]

# Find corrupt pair
nums = [3, 1, 2, 5, 2]
corrupt = find_corrupt_pair(nums.copy())
print(f"Corrupt pair in {[3, 1, 2, 5, 2]}: {corrupt}")  # [2, 4] (2 is duplicate, 4 is missing)
```



# Part II: Search & Sort Patterns

## 5. Binary Search Pattern

**When to use:** Searching in sorted data, or when you can eliminate half the search space in each step. This pattern extends beyond simple searching to many optimization problems.

**Key insight:** The power of binary search lies in the ability to eliminate half of the remaining possibilities with each comparison. This works whenever you can define a condition that divides the search space into two parts.

**Problem types:** Finding elements, first/last occurrence, peak elements, square roots, search in rotated arrays.

```python
def binary_search_basic(nums, target):
    """
    Basic binary search implementation.
    
    The template that forms the foundation for all binary search variations.
    Always use 'left + (right - left) // 2' to prevent integer overflow.
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Prevent overflow
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1    # Target must be in right half
        else:
            right = mid - 1   # Target must be in left half
    
    return -1  # Target not found

def find_first_occurrence(nums, target):
    """
    Find the first occurrence of target in sorted array with duplicates.
    
    Key insight: Even after finding target, continue searching in left half
    to ensure we find the first occurrence.
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            result = mid      # Found target, but keep searching left
            right = mid - 1   # Continue searching in left half for first occurrence
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result

def find_last_occurrence(nums, target):
    """
    Find the last occurrence of target in sorted array with duplicates.
    
    Similar to first occurrence, but continue searching in right half.
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            result = mid      # Found target, but keep searching right
            left = mid + 1    # Continue searching in right half for last occurrence
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result

def search_in_rotated_array(nums, target):
    """
    Search in rotated sorted array.
    
    Key insight: At least one half of the array is always sorted.
    We determine which half is sorted and check if target lies in that half.
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        
        # Determine which half is sorted
        if nums[left] <= nums[mid]:  # Left half is sorted
            # Check if target is in sorted left half
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half is sorted
            # Check if target is in sorted right half
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1

def find_peak_element(nums):
    """
    Find a peak element (element greater than its neighbors).
    
    Key insight: We can always move toward the side with larger neighbor,
    guaranteeing we'll find a peak.
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        # Compare with right neighbor to decide direction
        if nums[mid] < nums[mid + 1]:
            # Peak is on the right side
            left = mid + 1
        else:
            # Peak is on the left side or mid itself
            right = mid
    
    return left  # left == right at this point

def sqrt_binary_search(x):
    """
    Find integer square root using binary search.
    
    This demonstrates binary search on answer space rather than array indices.
    We search for the largest number whose square is <= x.
    
    Time: O(log x), Space: O(1)
    """
    if x < 2:
        return x
    
    left, right = 2, x // 2
    
    while left <= right:
        mid = left + (right - left) // 2
        square = mid * mid
        
        if square == x:
            return mid
        elif square < x:
            left = mid + 1
        else:
            right = mid - 1
    
    return right  # right is the largest number whose square <= x

def find_minimum_in_rotated_array(nums):
    """
    Find minimum element in rotated sorted array.
    
    Key insight: Minimum element is the only element smaller than its previous element.
    We use binary search to efficiently locate this pivot point.
    
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    # If array is not rotated
    if nums[left] <= nums[right]:
        return nums[left]
    
    while left < right:
        mid = left + (right - left) // 2
        
        # If mid element is greater than rightmost element,
        # minimum must be in right half
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            # Minimum is in left half or mid itself
            right = mid
    
    return nums[left]

# Example usage and testing
print("=== Binary Search Examples ===")

nums = [1, 2, 4, 4, 4, 6, 7]
target = 4

basic_result = binary_search_basic(nums, target)
first_occurrence = find_first_occurrence(nums, target)
last_occurrence = find_last_occurrence(nums, target)

print(f"Array: {nums}, Target: {target}")
print(f"Basic search result: {basic_result}")
print(f"First occurrence: {first_occurrence}")
print(f"Last occurrence: {last_occurrence}")

rotated = [4, 5, 6, 7, 0, 1, 2]
target = 0
rotated_result = search_in_rotated_array(rotated, target)
print(f"Rotated array {rotated}, target {target}: index {rotated_result}")

nums = [1, 2, 3, 1]
peak = find_peak_element(nums)
print(f"Peak element in {nums} at index: {peak} (value: {nums[peak]})")

x = 8
sqrt_result = sqrt_binary_search(x)
print(f"Integer square root of {x}: {sqrt_result}")
```



## 6. Quick Select Pattern

**When to use:** Finding the kth smallest or largest element without fully sorting the array. This pattern is essential for selection problems where you don't need complete ordering.

**Key insight:** Use the partitioning logic from quicksort, but only recurse on the side containing the target element. This reduces average time complexity from O(n log n) to O(n).

**Problem types:** Kth largest element, median finding, top K problems.

```python
import random

def quick_select(nums, k):
    """
    Find kth smallest element (1-indexed) using Quick Select.
    
    The brilliance of Quick Select: we only need to sort one side
    of the partition, unlike quicksort which sorts both sides.
    
    Average Time: O(n), Worst Time: O(n²), Space: O(1)
    """
    def partition(left, right, pivot_index):
        """
        Partition array around pivot, returning pivot's final position.
        
        After partitioning:
        - All elements left of pivot are <= pivot
        - All elements right of pivot are >= pivot
        """
        pivot_value = nums[pivot_index]
        
        # Move pivot to end
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
        
        # Partition around pivot
        store_index = left
        for i in range(left, right):
            if nums[i] < pivot_value:
                nums[store_index], nums[i] = nums[i], nums[store_index]
                store_index += 1
        
        # Place pivot in its final position
        nums[right], nums[store_index] = nums[store_index], nums[right]
        return store_index
    
    def select(left, right, k_smallest):
        """
        Recursively find kth smallest element in subarray.
        """
        if left == right:
            return nums[left]
        
        # Choose random pivot to ensure good average performance
        pivot_index = random.randint(left, right)
        
        # Partition and get pivot's final position
        pivot_index = partition(left, right, pivot_index)
        
        # The pivot is now at its correct sorted position
        if k_smallest == pivot_index:
            return nums[k_smallest]
        elif k_smallest < pivot_index:
            # Target is in left partition
            return select(left, pivot_index - 1, k_smallest)
        else:
            # Target is in right partition
            return select(pivot_index + 1, right, k_smallest)
    
    return select(0, len(nums) - 1, k - 1)  # Convert to 0-indexed

def find_kth_largest(nums, k):
    """
    Find kth largest element in array.
    
    We can either find (n-k+1)th smallest element,
    or modify our comparison to find kth largest directly.
    
    Time: O(n) average, Space: O(1)
    """
    return quick_select(nums.copy(), len(nums) - k + 1)

def median_of_array(nums):
    """
    Find median using Quick Select.
    
    Median is middle element for odd length,
    or average of two middle elements for even length.
    
    Time: O(n) average, Space: O(1)
    """
    n = len(nums)
    nums_copy = nums.copy()  # Don't modify original array
    
    if n % 2 == 1:
        # Odd length: median is middle element
        return quick_select(nums_copy, n // 2 + 1)
    else:
        # Even length: median is average of two middle elements
        left_mid = quick_select(nums_copy.copy(), n // 2)
        right_mid = quick_select(nums_copy.copy(), n // 2 + 1)
        return (left_mid + right_mid) / 2.0

def top_k_frequent_elements(nums, k):
    """
    Find k most frequent elements using Quick Select on frequencies.
    
    This showcases Quick Select on derived data (frequencies)
    rather than original array elements.
    
    Time: O(n) average, Space: O(n)
    """
    from collections import Counter
    
    # Count frequencies
    count = Counter(nums)
    unique_elements = list(count.keys())
    
    def partition_by_frequency(left, right, pivot_index):
        """Partition based on frequency rather than value."""
        pivot_freq = count[unique_elements[pivot_index]]
        
        # Move pivot to end
        unique_elements[pivot_index], unique_elements[right] = \
            unique_elements[right], unique_elements[pivot_index]
        
        store_index = left
        for i in range(left, right):
            # Note: we want higher frequencies first, so reverse comparison
            if count[unique_elements[i]] > pivot_freq:
                unique_elements[store_index], unique_elements[i] = \
                    unique_elements[i], unique_elements[store_index]
                store_index += 1
        
        unique_elements[right], unique_elements[store_index] = \
            unique_elements[store_index], unique_elements[right]
        return store_index
    
    def select_by_frequency(left, right, k):
        """Select k most frequent elements."""
        if left == right:
            return
        
        pivot_index = random.randint(left, right)
        pivot_index = partition_by_frequency(left, right, pivot_index)
        
        if k == pivot_index:
            return
        elif k < pivot_index:
            select_by_frequency(left, pivot_index - 1, k)
        else:
            select_by_frequency(pivot_index + 1, right, k)
    
    select_by_frequency(0, len(unique_elements) - 1, k - 1)
    return unique_elements[:k]

# Example usage and testing
print("=== Quick Select Examples ===")

nums = [3, 2, 1, 5, 6, 4]
k = 2

kth_smallest = quick_select(nums.copy(), k)
kth_largest = find_kth_largest(nums.copy(), k)
median = median_of_array(nums)

print(f"Array: {nums}")
print(f"{k}th smallest: {kth_smallest}")  # 2
print(f"{k}th largest: {kth_largest}")    # 5
print(f"Median: {median}")                # 3.5

# Test with frequencies
nums = [1, 1, 1, 2, 2, 3]
k = 2
top_k = top_k_frequent_elements(nums, k)
print(f"Top {k} frequent in {nums}: {top_k}")  # [1, 2]
```



## 7. Merge Intervals Pattern

**When to use:** Problems involving overlapping intervals, scheduling conflicts, or merging time ranges. This pattern is crucial for calendar applications and resource allocation problems.

**Key insight:** Sort intervals by start time, then iterate through them, merging overlapping ones. Two intervals overlap if the start of one is less than or equal to the end of the other.

**Problem types:** Merging overlapping intervals, inserting intervals, finding free time slots.

```python
def merge_intervals(intervals):
    """
    Merge overlapping intervals.
    
    The key insight: after sorting by start time, we only need to check
    if current interval overlaps with the last merged interval.
    
    Time: O(n log n), Space: O(1) excluding output
    """
    if not intervals:
        return []
    
    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]  # Start with first interval
    
    for current in intervals[1:]:
        last_merged = merged[-1]
        
        # Check if current interval overlaps with last merged interval
        if current[0] <= last_merged[1]:
            # Overlapping: merge by extending end time
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # Non-overlapping: add current interval to result
            merged.append(current)
    
    return merged

def insert_interval(intervals, new_interval):
    """
    Insert new interval and merge if necessary.
    
    Three phases:
    1. Add all intervals that end before new interval starts
    2. Merge all intervals that overlap with new interval
    3. Add all intervals that start after new interval ends
    
    Time: O(n), Space: O(n)
    """
    result = []
    i = 0
    start, end = new_interval
    
    # Phase 1: Add intervals that end before new interval starts
    while i < len(intervals) and intervals[i][1] < start:
        result.append(intervals[i])
        i += 1
    
    # Phase 2: Merge overlapping intervals
    while i < len(intervals) and intervals[i][0] <= end:
        # Extend the new interval to include current interval
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    
    # Add the merged interval
    result.append([start, end])
    
    # Phase 3: Add remaining intervals
    while i < len(intervals):
        result.append(intervals[i])
        i += 1
    
    return result

def interval_intersections(first_list, second_list):
    """
    Find intersection of two lists of intervals.
    
    Two intervals intersect if max(start1, start2) <= min(end1, end2).
    We use two pointers to efficiently find all intersections.
    
    Time: O(m + n), Space: O(1) excluding output
    """
    result = []
    i = j = 0
    
    while i < len(first_list) and j < len(second_list):
        # Get current intervals from both lists
        start1, end1 = first_list[i]
        start2, end2 = second_list[j]
        
        # Check if intervals intersect
        intersection_start = max(start1, start2)
        intersection_end = min(end1, end2)
        
        if intersection_start <= intersection_end:
            result.append([intersection_start, intersection_end])
        
        # Move pointer for interval that ends first
        if end1 < end2:
            i += 1
        else:
            j += 1
    
    return result

def can_attend_all_meetings(intervals):
    """
    Check if person can attend all meetings (no overlaps).
    
    After sorting, we only need to check adjacent intervals.
    
    Time: O(n log n), Space: O(1)
    """
    if not intervals:
        return True
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Check each adjacent pair for overlap
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False  # Overlap found
    
    return True

def min_meeting_rooms(intervals):
    """
    Find minimum number of meeting rooms required.
    
    Key insight: Use separate arrays for start and end times.
    When we encounter a start time, we need a room.
    When we encounter an end time, we free a room.
    
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return 0
    
    # Separate start and end times
    starts = [interval[0] for interval in intervals]
    ends = [interval[1] for interval in intervals]
    
    # Sort both arrays
    starts.sort()
    ends.sort()
    
    rooms_needed = 0
    max_rooms = 0
    start_ptr = end_ptr = 0
    
    # Process events in chronological order
    while start_ptr < len(starts):
        # If meeting starts before or when another ends
        if starts[start_ptr] < ends[end_ptr]:
            rooms_needed += 1  # Need one more room
            max_rooms = max(max_rooms, rooms_needed)
            start_ptr += 1
        else:
            rooms_needed -= 1  # Free up a room
            end_ptr += 1
    
    return max_rooms

def employee_free_time(schedules):
    """
    Find free time intervals common to all employees.
    
    Strategy: Merge all working intervals, then find gaps.
    
    Time: O(n log n), Space: O(n)
    """
    # Flatten all intervals from all employees
    all_intervals = []
    for schedule in schedules:
        all_intervals.extend(schedule)
    
    # Merge all working intervals
    merged_work = merge_intervals(all_intervals)
    
    # Find gaps between merged intervals
    free_time = []
    for i in range(1, len(merged_work)):
        # Gap exists between end of previous and start of current
        if merged_work[i-1][1] < merged_work[i][0]:
            free_time.append([merged_work[i-1][1], merged_work[i][0]])
    
    return free_time

# Example usage and comprehensive testing
print("=== Merge Intervals Examples ===")

# Test merge intervals
intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
merged = merge_intervals(intervals)
print(f"Original: {intervals}")
print(f"Merged: {merged}")  # [[1, 6], [8, 10], [15, 18]]

# Test insert interval
intervals = [[1, 3], [6, 9]]
new_interval = [2, 5]
inserted = insert_interval(intervals, new_interval)
print(f"Insert {new_interval} into {intervals}: {inserted}")  # [[1, 5], [6, 9]]

# Test meeting rooms
meetings = [[0, 30], [5, 10], [15, 20]]
can_attend = can_attend_all_meetings(meetings.copy())
min_rooms = min_meeting_rooms(meetings.copy())
print(f"Meetings: {meetings}")
print(f"Can attend all: {can_attend}")  # False
print(f"Min rooms needed: {min_rooms}")  # 2

# Test interval intersections
first = [[0, 2], [5, 10], [13, 23], [24, 25]]
second = [[1, 5], [8, 12], [15, 24], [25, 26]]
intersections = interval_intersections(first, second)
print(f"Intersections: {intersections}")  # [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
```



# Part III: Tree & Graph Patterns

## 8. Depth-First Search (DFS)

**When to use:** Exploring all paths, finding connected components, solving problems recursively on trees and graphs, or when you need to go as deep as possible before exploring other branches.

**Key insight:** DFS explores as far as possible along each branch before backtracking. Think of it as exploring a maze by always taking the first unexplored path you encounter, marking dead ends, and backtracking when stuck.

**Problem types:** Tree traversal, pathfinding, cycle detection, topological sorting.

```python
class TreeNode:
    """Definition for binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth_recursive(root):
    """
    Find maximum depth of binary tree using recursive DFS.
    
    The recursive beauty: depth of tree = 1 + max depth of subtrees.
    Base case: empty tree has depth 0.
    
    Time: O(n), Space: O(h) where h is height
    """
    if not root:
        return 0
    
    # Recursively find depth of left and right subtrees
    left_depth = max_depth_recursive(root.left)
    right_depth = max_depth_recursive(root.right)
    
    # Current node adds 1 to maximum of subtree depths
    return 1 + max(left_depth, right_depth)

def max_depth_iterative(root):
    """
    Find maximum depth using iterative DFS with stack.
    
    We simulate recursion using explicit stack containing (node, depth) pairs.
    This approach uses O(h) space but avoids recursion stack overflow.
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return 0
    
    stack = [(root, 1)]  # (node, current_depth)
    max_depth = 0
    
    while stack:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)
        
        # Add children with incremented depth
        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))
    
    return max_depth

def has_path_sum(root, target_sum):
    """
    Check if tree has root-to-leaf path with given sum.
    
    DFS naturally explores all root-to-leaf paths.
    We subtract current node's value from target as we go deeper.
    
    Time: O(n), Space: O(h)
    """
    def dfs(node, remaining_sum):
        if not node:
            return False
        
        remaining_sum -= node.val
        
        # Check if we're at leaf and sum matches
        if not node.left and not node.right:
            return remaining_sum == 0
        
        # Recursively check both subtrees
        return (dfs(node.left, remaining_sum) or 
                dfs(node.right, remaining_sum))
    
    return dfs(root, target_sum)

def find_all_paths_with_sum(root, target_sum):
    """
    Find all root-to-leaf paths with given sum.
    
    We maintain current path and add it to results when we find
    a valid path. Backtracking removes nodes when we return.
    
    Time: O(n²) worst case, Space: O(n²)
    """
    def dfs(node, remaining_sum, current_path, all_paths):
        if not node:
            return
        
        # Add current node to path
        current_path.append(node.val)
        remaining_sum -= node.val
        
        # If leaf and sum matches, save path
        if not node.left and not node.right and remaining_sum == 0:
            all_paths.append(current_path[:])  # Make a copy
        else:
            # Continue DFS on children
            dfs(node.left, remaining_sum, current_path, all_paths)
            dfs(node.right, remaining_sum, current_path, all_paths)
        
        # Backtrack: remove current node from path
        current_path.pop()
    
    all_paths = []
    dfs(root, target_sum, [], all_paths)
    return all_paths

def diameter_of_binary_tree(root):
    """
    Find diameter of binary tree (longest path between any two nodes).
    
    Key insight: For each node, diameter passing through it equals
    left_height + right_height. We update global maximum during DFS.
    
    Time: O(n), Space: O(h)
    """
    max_diameter = 0
    
    def height(node):
        """Calculate height and update diameter simultaneously."""
        nonlocal max_diameter
        
        if not node:
            return 0
        
        left_height = height(node.left)
        right_height = height(node.right)
        
        # Diameter through current node
        current_diameter = left_height + right_height
        max_diameter = max(max_diameter, current_diameter)
        
        # Return height of current subtree
        return 1 + max(left_height, right_height)
    
    height(root)
    return max_diameter

def validate_binary_search_tree(root):
    """
    Validate if binary tree is valid BST.
    
    For each node, we maintain valid range [min_val, max_val].
    Left children must be < node.val, right children must be > node.val.
    
    Time: O(n), Space: O(h)
    """
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        # Check if current node violates BST property
        if node.val <= min_val or node.val >= max_val:
            return False
        
        # Recursively validate subtrees with updated bounds
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))

def graph_dfs_all_paths(graph, start, end, path=[]):
    """
    Find all paths from start to end in graph using DFS.
    
    This demonstrates DFS on graphs. We maintain visited path
    to avoid cycles and explore all possible routes.
    
    Time: O(V + E) per path, Space: O(V)
    """
    path = path + [start]  # Add current node to path
    
    if start == end:
        return [path]      # Found complete path
    
    paths = []
    for neighbor in graph.get(start, []):
        if neighbor not in path:  # Avoid cycles
            # Recursively explore from neighbor
            new_paths = graph_dfs_all_paths(graph, neighbor, end, path)
            paths.extend(new_paths)
    
    return paths

def count_connected_components(n, edges):
    """
    Count connected components in undirected graph.
    
    We build adjacency list and use DFS to mark all nodes
    reachable from each unvisited node.
    
    Time: O(V + E), Space: O(V + E)
    """
    # Build adjacency list
    graph = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = set()
    components = 0
    
    def dfs(node):
        """Mark all nodes in current component as visited."""
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
    
    # Start DFS from each unvisited node
    for i in range(n):
        if i not in visited:
            dfs(i)
            components += 1
    
    return components

# Example usage and comprehensive testing
print("=== DFS Examples ===")

# Create sample binary tree:     3
#                               / \
#                              9   20
#                                 / \
#                                15  7
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

print(f"Max depth (recursive): {max_depth_recursive(root)}")  # 3
print(f"Max depth (iterative): {max_depth_iterative(root)}")  # 3
print(f"Has path sum 22: {has_path_sum(root, 22)}")  # True (3->9->10, but 10 doesn't exist, so False actually)
print(f"Diameter: {diameter_of_binary_tree(root)}")  # 3
print(f"Is valid BST: {validate_binary_search_tree(root)}")  # False

# Graph DFS example
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
all_paths = graph_dfs_all_paths(graph, 'A', 'F')
print(f"All paths from A to F: {all_paths}")

# Connected components
edges = [[0, 1], [1, 2], [3, 4]]
components = count_connected_components(5, edges)
print(f"Connected components: {components}")  # 2
```



## 9. Breadth-First Search (BFS)

**When to use:** Finding shortest paths in unweighted graphs, level-by-level tree processing, minimum number of steps to reach a target, or when you need to explore all possibilities at the current level before moving deeper.

**Key insight:** BFS explores all nodes at distance k before exploring nodes at distance k+1. This guarantees that the first time we reach a node, we've found the shortest path to it.

**Problem types:** Shortest path, level order traversal, minimum steps problems, flood fill.

```python
from collections import deque

def level_order_traversal(root):
    """
    Traverse binary tree level by level using BFS.
    
    We use a queue to process nodes level by level.
    The key insight: process all nodes at current level
    before adding their children for next level.
    
    Time: O(n), Space: O(w) where w is maximum width
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])  # Use deque for efficient operations
    
    while queue:
        level_size = len(queue)  # Number of nodes at current level
        current_level = []
        
        # Process all nodes at current level
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            # Add children for next level
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result

def zigzag_level_order(root):
    """
    Traverse tree in zigzag pattern (alternating left-to-right, right-to-left).
    
    We perform normal level order traversal but reverse every other level.
    This showcases how to modify BFS for specific requirements.
    
    Time: O(n), Space: O(w)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    left_to_right = True  # Direction flag
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        # Reverse level if going right-to-left
        if not left_to_right:
            current_level.reverse()
        
        result.append(current_level)
        left_to_right = not left_to_right  # Toggle direction
    
    return result

def min_depth_of_tree(root):
    """
    Find minimum depth of binary tree (shortest path to leaf).
    
    BFS naturally finds minimum depth because it explores
    level by level. First leaf we encounter gives minimum depth.
    
    Time: O(n), Space: O(w)
    """
    if not root:
        return 0
    
    queue = deque([(root, 1)])  # (node, depth)
    
    while queue:
        node, depth = queue.popleft()
        
        # First leaf node we encounter has minimum depth
        if not node.left and not node.right:
            return depth
        
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    
    return 0

def shortest_path_in_graph(graph, start, end):
    """
    Find shortest path between two nodes using BFS.
    
    BFS guarantees shortest path in unweighted graphs.
    We track both distance and actual path.
    
    Time: O(V + E), Space: O(V)
    """
    if start == end:
        return [start]
    
    queue = deque([(start, [start])])  # (current_node, path_to_current)
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        for neighbor in graph.get(current, []):
            if neighbor == end:
                return path + [neighbor]  # Found shortest path
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return []  # No path found

def word_ladder_length(begin_word, end_word, word_list):
    """
    Find minimum transformations to change begin_word to end_word.
    Each transformation changes exactly one letter.
    
    This is a shortest path problem in disguise. Each word is a node,
    and edges connect words differing by one letter.
    
    Time: O(M²×N) where M is word length, N is word list size
    Space: O(M×N)
    """
    if end_word not in word_list:
        return 0
    
    def get_neighbors(word):
        """Generate all words differing by exactly one letter."""
        neighbors = []
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != word[i]:
                    new_word = word[:i] + c + word[i+1:]
                    if new_word in word_set:
                        neighbors.append(new_word)
        return neighbors
    
    word_set = set(word_list)  # O(1) lookup
    queue = deque([(begin_word, 1)])  # (word, transformations)
    visited = {begin_word}
    
    while queue:
        current_word, transformations = queue.popleft()
        
        if current_word == end_word:
            return transformations
        
        for neighbor in get_neighbors(current_word):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, transformations + 1))
    
    return 0  # No transformation sequence found

def flood_fill(image, sr, sc, new_color):
    """
    Flood fill algorithm (like paint bucket tool).
    
    We use BFS to visit all connected pixels of same color
    and change them to new color.
    
    Time: O(n) where n is number of pixels, Space: O(n)
    """
    if not image or sr < 0 or sr >= len(image) or sc < 0 or sc >= len(image[0]):
        return image
    
    original_color = image[sr][sc]
    if original_color == new_color:
        return image  # No change needed
    
    queue = deque([(sr, sc)])
    image[sr][sc] = new_color
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # 4-directional
    
    while queue:
        row, col = queue.popleft()
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check bounds and color match
            if (0 <= new_row < len(image) and 
                0 <= new_col < len(image[0]) and 
                image[new_row][new_col] == original_color):
                
                image[new_row][new_col] = new_color
                queue.append((new_row, new_col))
    
    return image

def rotting_oranges(grid):
    """
    Find minimum time for all oranges to rot.
    Initially rotten oranges rot adjacent fresh oranges each minute.
    
    Multi-source BFS: we start from all initially rotten oranges
    simultaneously and process them level by level.
    
    Time: O(m×n), Space: O(m×n)
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0
    
    # Find all initially rotten oranges and count fresh ones
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:  # Rotten
                queue.append((r, c, 0))  # (row, col, time)
            elif grid[r][c] == 1:  # Fresh
                fresh_count += 1
    
    if fresh_count == 0:
        return 0  # No fresh oranges
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    max_time = 0
    
    while queue:
        row, col, time = queue.popleft()
        max_time = max(max_time, time)
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check bounds and if orange is fresh
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                grid[new_row][new_col] == 1):
                
                grid[new_row][new_col] = 2  # Make it rotten
                fresh_count -= 1
                queue.append((new_row, new_col, time + 1))
    
    return max_time if fresh_count == 0 else -1

def course_schedule_bfs(num_courses, prerequisites):
    """
    Check if all courses can be finished (detect cycle using BFS).
    
    This is topological sorting using Kahn's algorithm.
    If we can process all nodes, there's no cycle.
    
    Time: O(V + E), Space: O(V + E)
    """
    # Build adjacency list and in-degree count
    graph = {i: [] for i in range(num_courses)}
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Start with courses having no prerequisites
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    processed = 0
    
    while queue:
        current = queue.popleft()
        processed += 1
        
        # Process all courses that depend on current course
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return processed == num_courses  # True if no cycle

# Example usage and comprehensive testing
print("=== BFS Examples ===")

# Create sample binary tree
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

levels = level_order_traversal(root)
print(f"Level order: {levels}")  # [[3], [9, 20], [15, 7]]

zigzag = zigzag_level_order(root)
print(f"Zigzag order: {zigzag}")  # [[3], [20, 9], [15, 7]]

min_depth = min_depth_of_tree(root)
print(f"Minimum depth: {min_depth}")  # 2

# Graph shortest path
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': ['G'],
    'E': ['G'],
    'F': ['G'],
    'G': []
}
shortest_path = shortest_path_in_graph(graph, 'A', 'G')
print(f"Shortest path A to G: {shortest_path}")  # ['A', 'B', 'D', 'G'] or similar

# Word ladder
begin = "hit"
end = "cog"
words = ["hot","dot","dog","lot","log","cog"]
ladder_length = word_ladder_length(begin, end, words)
print(f"Word ladder length: {ladder_length}")  # 5

# Flood fill
image = [[1,1,1],[1,1,0],[1,0,1]]
filled = flood_fill([row[:] for row in image], 1, 1, 2)  # Copy to avoid modifying original
print(f"Flood fill result: {filled}")  # [[2,2,2],[2,2,0],[2,0,1]]
```



## 10. Tree Traversal Patterns

**When to use:** Processing tree nodes in specific orders, expression evaluation, serialization/deserialization, or when the order of processing matters for your algorithm.

**Key insight:** Different traversal orders give us different perspectives on the tree structure. Preorder gives us prefix notation, inorder gives us sorted order for BST, and postorder allows bottom-up processing.

**Problem types:** Expression trees, tree serialization, finding ancestors, tree reconstruction.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def preorder_recursive(root):
    """
    Preorder traversal: Root -> Left -> Right
    
    Use case: Copying the tree, prefix expressions, tree serialization.
    We process root first, which is useful when we need parent info
    before processing children.
    
    Time: O(n), Space: O(h) where h is height
    """
    def traverse(node, result):
        if node:
            result.append(node.val)      # Process root
            traverse(node.left, result)  # Process left subtree
            traverse(node.right, result) # Process right subtree
    
    result = []
    traverse(root, result)
    return result

def preorder_iterative(root):
    """
    Preorder traversal using explicit stack.
    
    The iterative version helps understand the underlying mechanism
    and avoids recursion depth issues for very deep trees.
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)  # Process current node
        
        # Push right first, then left (since stack is LIFO)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result

def inorder_recursive(root):
    """
    Inorder traversal: Left -> Root -> Right
    
    Use case: For BST, gives sorted order. Also useful for
    expression evaluation where we need left operand first.
    
    Time: O(n), Space: O(h)
    """
    def traverse(node, result):
        if node:
            traverse(node.left, result)  # Process left subtree
            result.append(node.val)      # Process root
            traverse(node.right, result) # Process right subtree
    
    result = []
    traverse(root, result)
    return result

def inorder_iterative(root):
    """
    Inorder traversal using stack.
    
    More complex than preorder because we need to visit node twice:
    once to go left, once to process after returning from left.
    
    Time: O(n), Space: O(h)
    """
    result = []
    stack = []
    current = root
    
    while stack or current:
        # Go to leftmost node
        while current:
            stack.append(current)
            current = current.left
        
        # Process current node
        current = stack.pop()
        result.append(current.val)
        
        # Move to right subtree
        current = current.right
    
    return result

def postorder_recursive(root):
    """
    Postorder traversal: Left -> Right -> Root
    
    Use case: Deleting tree, calculating directory sizes, postfix expressions.
    We process children before parent, enabling bottom-up computations.
    
    Time: O(n), Space: O(h)
    """
    def traverse(node, result):
        if node:
            traverse(node.left, result)  # Process left subtree
            traverse(node.right, result) # Process right subtree
            result.append(node.val)      # Process root
    
    result = []
    traverse(root, result)
    return result

def postorder_iterative(root):
    """
    Postorder traversal using two stacks.
    
    Trick: Reverse preorder (Root->Right->Left) gives postorder!
    We use two stacks to achieve this reversal efficiently.
    
    Time: O(n), Space: O(h)
    """
    if not root:
        return []
    
    stack1 = [root]
    stack2 = []
    
    # Modified preorder: Root -> Right -> Left
    while stack1:
        node = stack1.pop()
        stack2.append(node)
        
        # Push left first, then right (opposite of preorder)
        if node.left:
            stack1.append(node.left)
        if node.right:
            stack1.append(node.right)
    
    # Pop from stack2 to get postorder
    result = []
    while stack2:
        result.append(stack2.pop().val)
    
    return result

def morris_inorder(root):
    """
    Morris inorder traversal using O(1) space.
    
    Brilliant technique: temporarily modify tree structure to create
    threads, then restore. Achieves inorder without recursion or stack.
    
    Time: O(n), Space: O(1)
    """
    result = []
    current = root
    
    while current:
        if not current.left:
            # No left subtree, process current and go right
            result.append(current.val)
            current = current.right
        else:
            # Find inorder predecessor (rightmost node in left subtree)
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right
            
            if not predecessor.right:
                # Create thread and go left
                predecessor.right = current
                current = current.left
            else:
                # Thread exists, remove it and process current
                predecessor.right = None
                result.append(current.val)
                current = current.right
    
    return result

def build_tree_from_preorder_inorder(preorder, inorder):
    """
    Reconstruct binary tree from preorder and inorder traversals.
    
    Key insight: First element in preorder is always root.
    Find root in inorder to determine left and right subtrees.
    
    Time: O(n), Space: O(n)
    """
    if not preorder or not inorder:
        return None
    
    # Build index map for O(1) lookup in inorder
    inorder_map = {val: i for i, val in enumerate(inorder)}
    
    def build(pre_start, pre_end, in_start, in_end):
        if pre_start > pre_end:
            return None
        
        # Root is first element in preorder range
        root_val = preorder[pre_start]
        root = TreeNode(root_val)
        
        # Find root position in inorder
        root_index = inorder_map[root_val]
        
        # Calculate left subtree size
        left_size = root_index - in_start
        
        # Recursively build left and right subtrees
        root.left = build(pre_start + 1, pre_start + left_size,
                         in_start, root_index - 1)
        root.right = build(pre_start + left_size + 1, pre_end,
                          root_index + 1, in_end)
        
        return root
    
    return build(0, len(preorder) - 1, 0, len(inorder) - 1)

def serialize_tree(root):
    """
    Serialize binary tree to string using preorder traversal.
    
    We use preorder because it allows efficient reconstruction:
    first element is always root, making recursive rebuilding natural.
    
    Time: O(n), Space: O(n)
    """
    def preorder_serialize(node):
        if not node:
            values.append("null")
            return
        
        values.append(str(node.val))
        preorder_serialize(node.left)
        preorder_serialize(node.right)
    
    values = []
    preorder_serialize(root)
    return ",".join(values)

def deserialize_tree(data):
    """
    Deserialize string to binary tree.
    
    We use an iterator to consume preorder values one by one,
    recursively building left and right subtrees.
    
    Time: O(n), Space: O(n)
    """
    def preorder_deserialize():
        val = next(values)
        if val == "null":
            return None
        
        node = TreeNode(int(val))
        node.left = preorder_deserialize()
        node.right = preorder_deserialize()
        return node
    
    values = iter(data.split(","))
    return preorder_deserialize()

def find_path_to_node(root, target):
    """
    Find path from root to target node using preorder traversal.
    
    We maintain current path and use backtracking to remove
    nodes when they don't lead to target.
    
    Time: O(n), Space: O(h)
    """
    def find_path(node, path):
        if not node:
            return False
        
        # Add current node to path
        path.append(node.val)
        
        # Check if we found target
        if node.val == target:
            return True
        
        # Recursively search in subtrees
        if (find_path(node.left, path) or 
            find_path(node.right, path)):
            return True
        
        # Backtrack: remove current node if it doesn't lead to target
        path.pop()
        return False
    
    path = []
    if find_path(root, path):
        return path
    return []

# Example usage and comprehensive testing
print("=== Tree Traversal Examples ===")

# Create sample tree:      1
#                         / \
#                        2   3
#                       / \
#                      4   5
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

print(f"Preorder recursive: {preorder_recursive(root)}")    # [1, 2, 4, 5, 3]
print(f"Preorder iterative: {preorder_iterative(root)}")    # [1, 2, 4, 5, 3]

print(f"Inorder recursive: {inorder_recursive(root)}")      # [4, 2, 5, 1, 3]
print(f"Inorder iterative: {inorder_iterative(root)}")      # [4, 2, 5, 1, 3]
print(f"Morris inorder: {morris_inorder(root)}")            # [4, 2, 5, 1, 3]

print(f"Postorder recursive: {postorder_recursive(root)}")  # [4, 5, 2, 3, 1]
print(f"Postorder iterative: {postorder_iterative(root)}")  # [4, 5, 2, 3, 1]

# Test serialization
serialized = serialize_tree(root)
print(f"Serialized: {serialized}")
deserialized = deserialize_tree(serialized)
print(f"Deserialized preorder: {preorder_recursive(deserialized)}")

# Find path to node
path_to_5 = find_path_to_node(root, 5)
print(f"Path to node 5: {path_to_5}")  # [1, 2, 5]

# Tree reconstruction
preorder = [1, 2, 4, 5, 3]
inorder = [4, 2, 5, 1, 3]
reconstructed = build_tree_from_preorder_inorder(preorder, inorder)
print(f"Reconstructed tree preorder: {preorder_recursive(reconstructed)}")  # [1, 2, 4, 5, 3]
```



## 11. Topological Sort Pattern

**When to use:** Scheduling tasks with dependencies, course prerequisites, build systems, or any directed acyclic graph (DAG) where you need to find a valid ordering.

**Key insight:** Topological sort finds a linear ordering of vertices such that for every directed edge (u, v), vertex u comes before v in the ordering. This is only possible in DAGs (no cycles).

**Problem types:** Course scheduling, task dependencies, compilation order, detecting cycles in directed graphs.

```python
from collections import deque, defaultdict

def topological_sort_dfs(graph, num_vertices):
    """
    Topological sort using DFS (Depth-First Search).
    
    Algorithm: Perform DFS and add nodes to result in reverse post-order.
    The key insight: in a DAG, if we finish processing node u before node v,
    then u should come after v in topological ordering.
    
    Time: O(V + E), Space: O(V)
    """
    visited = set()
    result_stack = []
    
    def dfs(vertex):
        visited.add(vertex)
        
        # Visit all neighbors first
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs(neighbor)
        
        # Add current vertex after visiting all its dependencies
        result_stack.append(vertex)
    
    # Start DFS from all unvisited vertices
    for vertex in range(num_vertices):
        if vertex not in visited:
            dfs(vertex)
    
    # Reverse the stack to get correct topological order
    return result_stack[::-1]

def topological_sort_bfs(graph, num_vertices):
    """
    Topological sort using BFS (Kahn's Algorithm).
    
    Algorithm: Start with nodes having no dependencies (in-degree 0),
    remove them and update in-degrees of their neighbors.
    
    This approach is more intuitive: we process nodes as soon as
    all their dependencies are satisfied.
    
    Time: O(V + E), Space: O(V)
    """
    # Calculate in-degree for each vertex
    in_degree = [0] * num_vertices
    for vertex in graph:
        for neighbor in graph[vertex]:
            in_degree[neighbor] += 1
    
    # Start with vertices having no dependencies
    queue = deque([i for i in range(num_vertices) if in_degree[i] == 0])
    result = []
    
    while queue:
        current = queue.popleft()
        result.append(current)
        
        # Remove current vertex and update in-degrees
        for neighbor in graph.get(current, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If we couldn't process all vertices, there's a cycle
    if len(result) != num_vertices:
        return []  # Cycle detected
    
    return result

def course_schedule_with_order(num_courses, prerequisites):
    """
    Find valid course order given prerequisites.
    
    Returns course order if possible, empty list if impossible (cycle exists).
    This is a direct application of topological sort.
    
    Time: O(V + E), Space: O(V + E)
    """
    # Build adjacency list
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Find courses with no prerequisites
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    course_order = []
    
    while queue:
        current_course = queue.popleft()
        course_order.append(current_course)
        
        # Remove current course and update prerequisites count
        for next_course in graph[current_course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # Return order if all courses can be taken, empty list otherwise
    return course_order if len(course_order) == num_courses else []

def alien_dictionary_order(words):
    """
    Find lexicographical order of alien dictionary characters.
    
    Build dependency graph from word comparisons, then topologically sort.
    If word[i] < word[j], then first differing character creates dependency.
    
    Time: O(C) where C is total content of all words, Space: O(1) since at most 26 chars
    """
    # Build graph of character dependencies
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Initialize all characters with 0 in-degree
    for word in words:
        for char in word:
            in_degree[char] = 0
    
    # Build dependencies by comparing adjacent words
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        min_len = min(len(word1), len(word2))
        
        # Invalid case: longer word is prefix of shorter word
        if len(word1) > len(word2) and word1[:min_len] == word2[:min_len]:
            return ""
        
        # Find first different character
        for j in range(min_len):
            if word1[j] != word2[j]:
                # word1[j] comes before word2[j] in alien alphabet
                if word2[j] not in graph[word1[j]]:  # Avoid duplicate edges
                    graph[word1[j]].append(word2[j])
                    in_degree[word2[j]] += 1
                break
    
    # Topological sort using BFS
    queue = deque([char for char in in_degree if in_degree[char] == 0])
    result = []
    
    while queue:
        current = queue.popleft()
        result.append(current)
        
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all characters are processed (no cycle)
    if len(result) == len(in_degree):
        return "".join(result)
    else:
        return ""  # Cycle detected

def minimum_height_trees(n, edges):
    """
    Find roots that give minimum height trees.
    
    Key insight: Remove leaf nodes layer by layer until 1-2 nodes remain.
    These remaining nodes are the centroids that minimize tree height.
    
    Time: O(V + E), Space: O(V + E)
    """
    if n == 1:
        return [0]
    
    # Build adjacency list
    graph = defaultdict(list)
    degree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        degree[u] += 1
        degree[v] += 1
    
    # Start with leaf nodes (degree 1)
    queue = deque([i for i in range(n) if degree[i] == 1])
    remaining = n
    
    # Remove leaves layer by layer
    while remaining > 2:
        leaves_count = len(queue)
        remaining -= leaves_count
        
        for _ in range(leaves_count):
            leaf = queue.popleft()
            
            # Remove leaf and update neighbors
            for neighbor in graph[leaf]:
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    queue.append(neighbor)
    
    return list(queue)  # 1 or 2 remaining nodes are the answer

def detect_cycle_directed_graph(graph, num_vertices):
    """
    Detect cycle in directed graph using topological sort.
    
    If topological sort can't process all vertices,
    then there must be a cycle.
    
    Time: O(V + E), Space: O(V)
    """
    in_degree = [0] * num_vertices
    
    # Calculate in-degrees
    for vertex in graph:
        for neighbor in graph[vertex]:
            in_degree[neighbor] += 1
    
    # BFS from nodes with no incoming edges
    queue = deque([i for i in range(num_vertices) if in_degree[i] == 0])
    processed = 0
    
    while queue:
        current = queue.popleft()
        processed += 1
        
        for neighbor in graph.get(current, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return processed != num_vertices  # Cycle exists if not all vertices processed

def task_scheduling_with_dependencies(tasks, dependencies):
    """
    Schedule tasks with dependencies, minimizing total time.
    
    This extends basic topological sort by considering task priorities
    or execution times when multiple tasks are ready.
    
    Time: O(V + E), Space: O(V + E)
    """
    # Build dependency graph
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Initialize all tasks
    for task in tasks:
        in_degree[task] = 0
    
    # Add dependencies
    for before, after in dependencies:
        graph[before].append(after)
        in_degree[after] += 1
    
    # Priority queue for tasks ready to execute (can use different priority)
    import heapq
    ready_tasks = [task for task in tasks if in_degree[task] == 0]
    heapq.heapify(ready_tasks)
    
    execution_order = []
    
    while ready_tasks:
        # Execute highest priority ready task
        current_task = heapq.heappop(ready_tasks)
        execution_order.append(current_task)
        
        # Update dependencies
        for next_task in graph[current_task]:
            in_degree[next_task] -= 1
            if in_degree[next_task] == 0:
                heapq.heappush(ready_tasks, next_task)
    
    return execution_order if len(execution_order) == len(tasks) else []

# Example usage and comprehensive testing
print("=== Topological Sort Examples ===")

# Course scheduling example
num_courses = 4
prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
course_order = course_schedule_with_order(num_courses, prerequisites)
print(f"Course order: {course_order}")  # Possible: [0, 1, 2, 3] or [0, 2, 1, 3]

# Build basic graph for testing
graph = {
    0: [1, 2],
    1: [3],
    2: [3],
    3: []
}

topo_dfs = topological_sort_dfs(graph, 4)
topo_bfs = topological_sort_bfs(graph, 4)
print(f"Topological sort (DFS): {topo_dfs}")  # [0, 1, 2, 3] or [0, 2, 1, 3]
print(f"Topological sort (BFS): {topo_bfs}")  # [0, 1, 2, 3] or [0, 2, 1, 3]

# Alien dictionary
words = ["wrt", "wrf", "er", "ett", "rftt"]
alien_order = alien_dictionary_order(words)
print(f"Alien dictionary order: {alien_order}")  # "wertf"

# Minimum height trees
edges = [[0, 1], [1, 2], [1, 3], [2, 4], [3, 5]]
mht_roots = minimum_height_trees(6, edges)
print(f"Minimum height tree roots: {mht_roots}")  # [1, 2]

# Cycle detection
cyclic_graph = {0: [1], 1: [2], 2: [0]}  # Has cycle: 0->1->2->0
has_cycle = detect_cycle_directed_graph(cyclic_graph, 3)
print(f"Graph has cycle: {has_cycle}")  # True

# Task scheduling
tasks = ['A', 'B', 'C', 'D']
dependencies = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
task_order = task_scheduling_with_dependencies(tasks, dependencies)
print(f"Task execution order: {task_order}")  # ['A', 'B', 'C', 'D'] or ['A', 'C', 'B', 'D']
```



## 12. Union-Find Pattern

**When to use:** Dynamic connectivity problems, detecting cycles in undirected graphs, grouping elements into disjoint sets, or when you need to efficiently merge sets and check connectivity.

**Key insight:** Union-Find (Disjoint Set Union) maintains disjoint sets with two main operations: find (which set does element belong to) and union (merge two sets). Path compression and union by rank make operations nearly O(1).

**Problem types:** Connected components, cycle detection, Kruskal's MST algorithm, percolation problems.

```python
class UnionFind:
    """
    Union-Find data structure with path compression and union by rank.
    
    This implementation achieves nearly O(1) amortized time per operation
    through two optimizations:
    1. Path Compression: Make every node point directly to root during find
    2. Union by Rank: Always attach smaller tree under root of larger tree
    
    Time: O(α(n)) per operation, where α is inverse Ackermann function
    Space: O(n)
    """
    
    def __init__(self, n):
        """Initialize n disjoint sets."""
        self.parent = list(range(n))  # Each node is its own parent initially
        self.rank = [0] * n           # Height of each tree (for union by rank)
        self.components = n           # Number of disjoint components
    
    def find(self, x):
        """
        Find root of set containing x with path compression.
        
        Path compression: make every node in path point directly to root.
        This flattens the tree and speeds up future operations.
        """
        if self.parent[x] != x:
            # Recursively find root and compress path
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """
        Union two sets containing x and y using union by rank.
        
        Union by rank: attach tree with smaller rank under tree with larger rank.
        This keeps trees balanced and maintains good performance.
        
        Returns True if union performed, False if already connected.
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same set
        
        # Union by rank: attach smaller tree under larger tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            # Same rank: make one root and increase its rank
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        self.components -= 1  # One fewer component after union
        return True
    
    def connected(self, x, y):
        """Check if x and y are in the same set."""
        return self.find(x) == self.find(y)
    
    def get_components(self):
        """Get number of disjoint components."""
        return self.components
    
    def get_component_size(self, x):
        """Get size of component containing x."""
        root = self.find(x)
        return sum(1 for i in range(len(self.parent)) if self.find(i) == root)

def count_connected_components_uf(n, edges):
    """
    Count connected components in undirected graph using Union-Find.
    
    Start with n components, decrease count each time we union two components.
    Union-Find naturally handles the merging of components.
    
    Time: O(E×α(n)), Space: O(n)
    """
    uf = UnionFind(n)
    
    for u, v in edges:
        uf.union(u, v)
    
    return uf.get_components()

def detect_cycle_undirected_uf(n, edges):
    """
    Detect cycle in undirected graph using Union-Find.
    
    Key insight: If we try to union two nodes that are already connected,
    then adding this edge creates a cycle.
    
    Time: O(E×α(n)), Space: O(n)
    """
    uf = UnionFind(n)
    
    for u, v in edges:
        if uf.connected(u, v):
            return True  # Adding edge between connected nodes creates cycle
        uf.union(u, v)
    
    return False

def accounts_merge(accounts):
    """
    Merge accounts that belong to the same person.
    
    If two accounts share an email, they belong to same person.
    Use Union-Find to group accounts, then merge emails.
    
    Time: O(N×M×α(N×M)) where N=accounts, M=emails per account
    Space: O(N×M)
    """
    # Create email to index mapping
    email_to_index = {}
    email_to_name = {}
    index = 0
    
    # Assign unique index to each unique email
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in email_to_index:
                email_to_index[email] = index
                email_to_name[email] = name
                index += 1
    
    # Union emails that belong to same account
    uf = UnionFind(index)
    for account in accounts:
        first_email = account[1]
        first_index = email_to_index[first_email]
        
        for email in account[2:]:
            email_index = email_to_index[email]
            uf.union(first_index, email_index)
    
    # Group emails by their root parent
    from collections import defaultdict
    groups = defaultdict(list)
    for email, email_index in email_to_index.items():
        root = uf.find(email_index)
        groups[root].append(email)
    
    # Build result with sorted emails
    result = []
    for emails in groups.values():
        emails.sort()
        name = email_to_name[emails[0]]
        result.append([name] + emails)
    
    return result

def number_of_islands_uf(grid):
    """
    Count number of islands using Union-Find.
    
    Convert 2D grid to 1D indices and union adjacent land cells.
    Number of components with land cells gives island count.
    
    Time: O(M×N×α(M×N)), Space: O(M×N)
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    uf = UnionFind(rows * cols)
    
    def get_index(r, c):
        return r * cols + c
    
    # Union adjacent land cells
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':  # Land cell
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols and 
                        grid[nr][nc] == '1'):
                        uf.union(get_index(r, c), get_index(nr, nc))
    
    # Count unique components that contain land cells
    land_roots = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                land_roots.add(uf.find(get_index(r, c)))
    
    return len(land_roots)

def kruskal_minimum_spanning_tree(n, edges):
    """
    Find Minimum Spanning Tree using Kruskal's algorithm with Union-Find.
    
    Algorithm: Sort edges by weight, add edge to MST if it doesn't create cycle.
    Union-Find efficiently checks for cycles.
    
    Time: O(E log E), Space: O(V)
    """
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])  # (u, v, weight)
    
    uf = UnionFind(n)
    mst_edges = []
    mst_weight = 0
    
    for u, v, weight in edges:
        if not uf.connected(u, v):  # No cycle created
            uf.union(u, v)
            mst_edges.append((u, v, weight))
            mst_weight += weight
            
            # MST has exactly n-1 edges
            if len(mst_edges) == n - 1:
                break
    
    return mst_edges, mst_weight

def redundant_connection(edges):
    """
    Find the redundant edge that creates a cycle in tree.
    
    In a tree with n nodes, there are exactly n-1 edges.
    The extra edge creates exactly one cycle.
    
    Time: O(n×α(n)), Space: O(n)
    """
    n = len(edges)
    uf = UnionFind(n + 1)  # Nodes are 1-indexed
    
    for u, v in edges:
        if uf.connected(u, v):
            return [u, v]  # This edge creates a cycle
        uf.union(u, v)
    
    return []

# Example usage and comprehensive testing
print("=== Union-Find Examples ===")

# Basic Union-Find operations
uf = UnionFind(10)
print(f"Initial components: {uf.get_components()}")  # 10

# Connect some nodes
uf.union(1, 2)
uf.union(2, 3)
uf.union(4, 5)
print(f"After unions: {uf.get_components()}")  # 7
print(f"1 and 3 connected: {uf.connected(1, 3)}")  # True
print(f"1 and 4 connected: {uf.connected(1, 4)}")  # False

# Count connected components
edges = [[0, 1], [1, 2], [3, 4]]
components = count_connected_components_uf(5, edges)
print(f"Connected components: {components}")  # 2

# Cycle detection
cycle_edges = [[0, 1], [1, 2], [2, 0]]
has_cycle = detect_cycle_undirected_uf(3, cycle_edges)
print(f"Graph has cycle: {has_cycle}")  # True

# Account merging
accounts = [
    ["John", "johnsmith@mail.com", "john00@mail.com"],
    ["John", "johnnybravo@mail.com"],
    ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
    ["Mary", "mary@mail.com"]
]
merged = accounts_merge(accounts)
print(f"Merged accounts: {merged}")

# Number of islands
grid = [
    ["1","1","1","1","0"],
    ["1","1","0","1","0"],
    ["1","1","0","0","0"],
    ["0","0","0","0","0"]
]
islands = number_of_islands_uf(grid)
print(f"Number of islands: {islands}")  # 1

# Kruskal's MST
edges = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4)]
mst_edges, mst_weight = kruskal_minimum_spanning_tree(4, edges)
print(f"MST edges: {mst_edges}, Total weight: {mst_weight}")



# Part IV: Dynamic Programming & Optimization

## 13. Dynamic Programming Pattern

**When to use:** Problems with overlapping subproblems and optimal substructure. When you can break a complex problem into simpler subproblems and the optimal solution contains optimal solutions to subproblems.

**Key insight:** Store solutions to subproblems to avoid recalculating them. This transforms exponential recursive solutions into polynomial iterative solutions. Think of it as "smart recursion with memory."

**Problem types:** Optimization problems, counting problems, sequence problems, knapsack variants.

```python
def fibonacci_dp_variants(n):
    """
    Multiple approaches to fibonacci: shows evolution from naive to optimal.
    
    This demonstrates the thinking process:
    1. Naive recursion: clear but exponential
    2. Memoization: add memory to recursion  
    3. Tabulation: bottom-up iterative
    4. Space optimization: keep only needed values
    """
    
    # Approach 1: Naive recursion - O(2^n) time, O(n) space
    def fib_naive(n):
        if n <= 1:
            return n
        return fib_naive(n-1) + fib_naive(n-2)
    
    # Approach 2: Memoization (top-down DP) - O(n) time, O(n) space
    def fib_memo(n, memo={}):
        if n in memo:
            return memo[n]
        if n <= 1:
            return n
        memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
        return memo[n]
    
    # Approach 3: Tabulation (bottom-up DP) - O(n) time, O(n) space
    def fib_tab(n):
        if n <= 1:
            return n
        dp = [0] * (n + 1)
        dp[1] = 1
        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[n]
    
    # Approach 4: Space optimized - O(n) time, O(1) space
    def fib_optimized(n):
        if n <= 1:
            return n
        prev2, prev1 = 0, 1
        for i in range(2, n + 1):
            current = prev1 + prev2
            prev2, prev1 = prev1, current
        return prev1
    
    return fib_optimized(n)  # Return the most efficient version

def longest_increasing_subsequence(nums):
    """
    Find length of longest increasing subsequence.
    
    DP State: dp[i] = length of LIS ending at index i
    Transition: dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]
    
    Time: O(n²), Space: O(n)
    """
    if not nums:
        return 0
    
    n = len(nums)
    # dp[i] represents length of LIS ending at index i
    dp = [1] * n  # Each element forms LIS of length 1
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                # Can extend LIS ending at j
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

def longest_common_subsequence(text1, text2):
    """
    Find length of longest common subsequence between two strings.
    
    DP State: dp[i][j] = LCS length of text1[0:i] and text2[0:j]
    Transition: 
    - If text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
    - Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    Time: O(m×n), Space: O(m×n)
    """
    m, n = len(text1), len(text2)
    
    # dp[i][j] = LCS length of text1[0:i] and text2[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                # Characters match, extend LCS
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                # Take maximum from excluding one character
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

def knapsack_0_1(weights, values, capacity):
    """
    0/1 Knapsack: maximize value within weight capacity.
    Each item can be taken at most once.
    
    DP State: dp[i][w] = max value using first i items with capacity w
    Transition:
    - Don't take item i: dp[i][w] = dp[i-1][w]  
    - Take item i: dp[i][w] = dp[i-1][w-weight[i]] + value[i]
    - Choose maximum of both options
    
    Time: O(n×W), Space: O(n×W)
    """
    n = len(weights)
    # dp[i][w] = max value using first i items with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Option 1: Don't take current item
            dp[i][w] = dp[i-1][w]
            
            # Option 2: Take current item if it fits
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                               dp[i-1][w - weights[i-1]] + values[i-1])
    
    return dp[n][capacity]

def coin_change_min_coins(coins, amount):
    """
    Find minimum coins needed to make amount.
    
    DP State: dp[i] = minimum coins needed to make amount i
    Transition: dp[i] = min(dp[i-coin] + 1) for all valid coins
    
    Time: O(amount × coins), Space: O(amount)
    """
    # dp[i] = minimum coins needed to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # 0 coins needed to make amount 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                # Use this coin and check if it gives better result
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

def coin_change_count_ways(coins, amount):
    """
    Count number of ways to make amount using given coins.
    
    DP State: dp[i] = number of ways to make amount i
    Transition: dp[i] += dp[i-coin] for all valid coins
    
    Time: O(amount × coins), Space: O(amount)
    """
    # dp[i] = number of ways to make amount i
    dp = [0] * (amount + 1)
    dp[0] = 1  # One way to make amount 0: use no coins
    
    # Process each coin type
    for coin in coins:
        # Update all amounts that can use this coin
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    
    return dp[amount]

def edit_distance(word1, word2):
    """
    Find minimum edit distance (insert/delete/replace) between two words.
    
    DP State: dp[i][j] = min operations to convert word1[0:i] to word2[0:j]
    Transition:
    - If chars match: dp[i][j] = dp[i-1][j-1]
    - Else: dp[i][j] = 1 + min(insert, delete, replace)
    
    Time: O(m×n), Space: O(m×n)
    """
    m, n = len(word1), len(word2)
    
    # dp[i][j] = min operations to convert word1[0:i] to word2[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases: converting empty string
    for i in range(m + 1):
        dp[i][0] = i  # Delete all i characters
    for j in range(n + 1):
        dp[0][j] = j  # Insert all j characters
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                # Characters match, no operation needed
                dp[i][j] = dp[i-1][j-1]
            else:
                # Choose minimum of three operations
                dp[i][j] = 1 + min(
                    dp[i-1][j],     # Delete from word1
                    dp[i][j-1],     # Insert to word1  
                    dp[i-1][j-1]    # Replace in word1
                )
    
    return dp[m][n]

def house_robber_variants(nums):
    """
    House robber problems: maximize money robbed without adjacent houses.
    
    Shows different constraints and how DP adapts:
    1. Linear houses
    2. Circular houses  
    3. Binary tree houses
    """
    
    def rob_linear(houses):
        """
        Linear arrangement: can't rob adjacent houses.
        
        DP State: dp[i] = max money robbed from first i houses
        Transition: dp[i] = max(rob house i + dp[i-2], don't rob house i + dp[i-1])
        
        Time: O(n), Space: O(1)
        """
        if not houses:
            return 0
        if len(houses) == 1:
            return houses[0]
        
        # Only need previous two values
        prev2 = houses[0]  # dp[i-2]
        prev1 = max(houses[0], houses[1])  # dp[i-1]
        
        for i in range(2, len(houses)):
            current = max(prev1, prev2 + houses[i])
            prev2, prev1 = prev1, current
        
        return prev1
    
    def rob_circular(houses):
        """
        Circular arrangement: first and last houses are adjacent.
        
        Key insight: Either rob first house (can't rob last) or don't rob first house.
        Run linear algorithm twice with different constraints.
        
        Time: O(n), Space: O(1)
        """
        if not houses:
            return 0
        if len(houses) == 1:
            return houses[0]
        
        # Case 1: Rob first house, can't rob last
        case1 = rob_linear(houses[:-1])
        
        # Case 2: Don't rob first house, can rob last
        case2 = rob_linear(houses[1:])
        
        return max(case1, case2)
    
    return rob_linear(nums)

def palindrome_partitioning_min_cuts(s):
    """
    Find minimum cuts to partition string into palindromes.
    
    DP State: dp[i] = min cuts needed for s[0:i+1]
    Transition: For each ending position, try all possible last palindromes
    
    Time: O(n²), Space: O(n²)
    """
    n = len(s)
    
    # Precompute palindrome information
    is_palindrome = [[False] * n for _ in range(n)]
    
    # Every single character is palindrome
    for i in range(n):
        is_palindrome[i][i] = True
    
    # Check for palindromes of length 2
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            is_palindrome[i][i + 1] = True
    
    # Check for palindromes of length 3 and more
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and is_palindrome[i + 1][j - 1]:
                is_palindrome[i][j] = True
    
    # DP for minimum cuts
    dp = [float('inf')] * n
    
    for i in range(n):
        if is_palindrome[0][i]:
            dp[i] = 0  # Entire prefix is palindrome
        else:
            # Try all possible last palindromes
            for j in range(i):
                if is_palindrome[j + 1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)
    
    return dp[n - 1]

# Example usage and comprehensive testing
print("=== Dynamic Programming Examples ===")

# Fibonacci
n = 10
fib_result = fibonacci_dp_variants(n)
print(f"Fibonacci({n}): {fib_result}")  # 55

# Longest Increasing Subsequence
nums = [10, 9, 2, 5, 3, 7, 101, 18]
lis_length = longest_increasing_subsequence(nums)
print(f"LIS length in {nums}: {lis_length}")  # 4

# Longest Common Subsequence  
text1, text2 = "abcde", "ace"
lcs_length = longest_common_subsequence(text1, text2)
print(f"LCS length of '{text1}' and '{text2}': {lcs_length}")  # 3

# 0/1 Knapsack
weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
max_value = knapsack_0_1(weights, values, capacity)
print(f"Knapsack max value: {max_value}")  # 220

# Coin Change
coins = [1, 3, 4]
amount = 6
min_coins = coin_change_min_coins(coins, amount)
count_ways = coin_change_count_ways(coins, amount)
print(f"Min coins for amount {amount}: {min_coins}")  # 2
print(f"Ways to make amount {amount}: {count_ways}")  # 3

# Edit Distance
word1, word2 = "horse", "ros"
edit_dist = edit_distance(word1, word2)
print(f"Edit distance between '{word1}' and '{word2}': {edit_dist}")  # 3

# House Robber
houses = [2, 7, 9, 3, 1]
max_robbed = house_robber_variants(houses)
print(f"Max money robbed: {max_robbed}")  # 12

# Palindrome Partitioning
s = "aab"
min_cuts = palindrome_partitioning_min_cuts(s)
print(f"Min cuts for palindrome partitioning '{s}': {min_cuts}")  # 1



## 14. Kadane's Algorithm Pattern

**When to use:** Finding maximum sum of contiguous subarray, or variants involving maximum/minimum products, circular arrays, or multiple subarrays.

**Key insight:** At each position, we decide whether to extend the existing subarray or start a new one. We keep track of the maximum sum ending at current position and update global maximum.

**Problem types:** Maximum subarray sum, maximum product subarray, maximum sum circular subarray.

```python
def kadane_basic(nums):
    """
    Find maximum sum of contiguous subarray (classic Kadane's algorithm).
    
    The brilliant insight: at each position, we have two choices:
    1. Extend the previous subarray by including current element
    2. Start a new subarray from current element
    
    We choose the option that gives larger sum.
    
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    
    max_ending_here = nums[0]  # Max sum ending at current position
    max_so_far = nums[0]       # Global maximum sum found so far
    
    for i in range(1, len(nums)):
        # Either extend previous subarray or start new one
        max_ending_here = max(nums[i], max_ending_here + nums[i])
        
        # Update global maximum
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far

def kadane_with_indices(nums):
    """
    Kadane's algorithm that also returns the indices of maximum subarray.
    
    We track start and end indices of the current subarray and
    update them when we find a new maximum.
    
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0, 0, 0
    
    max_sum = nums[0]
    current_sum = nums[0]
    
    start = 0          # Start of maximum subarray
    end = 0            # End of maximum subarray
    temp_start = 0     # Temporary start when we begin new subarray
    
    for i in range(1, len(nums)):
        if current_sum < 0:
            # Start new subarray from current position
            current_sum = nums[i]
            temp_start = i
        else:
            # Extend current subarray
            current_sum += nums[i]
        
        # Update maximum if we found better sum
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, start, end

def maximum_product_subarray(nums):
    """
    Find maximum product of contiguous subarray.
    
    Challenge: Negative numbers can make small products large.
    Solution: Track both maximum and minimum products ending at each position.
    
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    
    # Track both max and min products ending at current position
    max_product = nums[0]
    min_product = nums[0]
    result = nums[0]
    
    for i in range(1, len(nums)):
        current = nums[i]
        
        # If current number is negative, swap max and min
        if current < 0:
            max_product, min_product = min_product, max_product
        
        # Update max and min products ending at current position
        max_product = max(current, max_product * current)
        min_product = min(current, min_product * current)
        
        # Update global maximum
        result = max(result, max_product)
    
    return result

def maximum_sum_circular_subarray(nums):
    """
    Find maximum sum of subarray in circular array.
    
    Key insight: Maximum circular sum = Total sum - Minimum subarray sum
    We need to consider two cases:
    1. Maximum subarray is non-circular (use regular Kadane's)
    2. Maximum subarray is circular (use total - minimum subarray)
    
    Time: O(n), Space: O(1)
    """
    def kadane_max(arr):
        """Standard Kadane's for maximum subarray."""
        max_ending = arr[0]
        max_so_far = arr[0]
        
        for i in range(1, len(arr)):
            max_ending = max(arr[i], max_ending + arr[i])
            max_so_far = max(max_so_far, max_ending)
        
        return max_so_far
    
    def kadane_min(arr):
        """Modified Kadane's for minimum subarray."""
        min_ending = arr[0]
        min_so_far = arr[0]
        
        for i in range(1, len(arr)):
            min_ending = min(arr[i], min_ending + arr[i])
            min_so_far = min(min_so_far, min_ending)
        
        return min_so_far
    
    # Case 1: Maximum subarray is non-circular
    max_kadane = kadane_max(nums)
    
    # Case 2: Maximum subarray is circular
    total_sum = sum(nums)
    min_kadane = kadane_min(nums)
    max_circular = total_sum - min_kadane
    
    # Handle edge case: all elements are negative
    if max_circular == 0:
        return max_kadane
    
    return max(max_kadane, max_circular)

def maximum_sum_k_subarrays(nums, k):
    """
    Find maximum sum of k non-overlapping subarrays.
    
    We use DP with Kadane's insight:
    dp[i][j] = max sum using j subarrays from first i elements
    
    Time: O(n²×k), Space: O(n×k)
    """
    n = len(nums)
    if k > n:
        return 0
    
    # dp[i][j] = max sum using exactly j subarrays from first i elements
    dp = [[-float('inf')] * (k + 1) for _ in range(n + 1)]
    
    # Base case: 0 subarrays gives sum 0
    for i in range(n + 1):
        dp[i][0] = 0
    
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            # Option 1: Don't include nums[i-1] in any subarray
            dp[i][j] = dp[i-1][j]
            
            # Option 2: Include nums[i-1] as end of some subarray
            current_sum = 0
            for start in range(i - 1, -1, -1):
                current_sum += nums[start]
                if j == 1:
                    # First subarray
                    dp[i][j] = max(dp[i][j], current_sum)
                else:
                    # Extend from previous subarrays
                    dp[i][j] = max(dp[i][j], dp[start][j-1] + current_sum)
    
    return dp[n][k]

def maximum_subarray_sum_with_deletion(nums):
    """
    Find maximum subarray sum with at most one deletion allowed.
    
    We maintain two states:
    - no_delete[i]: max sum ending at i with no deletions
    - one_delete[i]: max sum ending at i with exactly one deletion
    
    Time: O(n), Space: O(1)
    """
    if not nums:
        return 0
    
    n = len(nums)
    
    # no_delete[i]: max sum ending at i without any deletion
    # one_delete[i]: max sum ending at i with exactly one deletion
    no_delete = nums[0]
    one_delete = 0  # Can't delete from single element to get valid subarray
    result = nums[0]
    
    for i in range(1, n):
        # Update one_delete: either delete current element or extend previous deletion
        one_delete = max(no_delete, one_delete + nums[i])
        
        # Update no_delete: standard Kadane's algorithm
        no_delete = max(nums[i], no_delete + nums[i])
        
        # Update result
        result = max(result, max(no_delete, one_delete))
    
    return result

def maximum_alternating_sum(nums):
    """
    Find maximum alternating sum of subsequence.
    Alternating sum: a1 - a2 + a3 - a4 + ...
    
    We track two states:
    - even: max sum ending at current position with even number of elements
    - odd: max sum ending at current position with odd number of elements
    
    Time: O(n), Space: O(1)
    """
    # even: max alternating sum with even number of elements (last is subtracted)
    # odd: max alternating sum with odd number of elements (last is added)
    even = 0  # Empty subsequence
    odd = 0
    
    for num in nums:
        # Update in correct order to avoid using updated values
        new_odd = max(odd, even + num)   # Add current number
        new_even = max(even, odd - num)  # Subtract current number
        
        odd = new_odd
        even = new_even
    
    return odd  # We want odd number of elements for maximum alternating sum

# Example usage and comprehensive testing
print("=== Kadane's Algorithm Examples ===")

# Basic maximum subarray
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
max_sum = kadane_basic(nums)
max_sum_with_idx, start, end = kadane_with_indices(nums.copy())
print(f"Maximum subarray sum: {max_sum}")  # 6
print(f"Maximum subarray: indices {start} to {end}, sum {max_sum_with_idx}")

# Maximum product subarray
nums = [2, 3, -2, 4]
max_product = maximum_product_subarray(nums)
print(f"Maximum product subarray: {max_product}")  # 6

# Maximum sum circular subarray
nums = [1, -2, 3, -2]
max_circular_sum = maximum_sum_circular_subarray(nums)
print(f"Maximum circular subarray sum: {max_circular_sum}")  # 3

nums = [5, -3, 5]
max_circular_sum = maximum_sum_circular_subarray(nums)
print(f"Maximum circular subarray sum: {max_circular_sum}")  # 10

# Maximum sum with deletion
nums = [1, -2, 0, 3]
max_sum_delete = maximum_subarray_sum_with_deletion(nums)
print(f"Maximum sum with deletion: {max_sum_delete}")  # 4

# Maximum alternating sum
nums = [4, 2, 5, 3]
max_alt_sum = maximum_alternating_sum(nums)
print(f"Maximum alternating sum: {max_alt_sum}")  # 7 (5-2+4)
```



## 15. Divide & Conquer Pattern

**When to use:** Problems that can be broken into smaller subproblems of the same type, where solutions can be combined to solve the original problem. This pattern shines when subproblems are independent.

**Key insight:** Break problem into smaller pieces, solve each piece recursively, then combine solutions. The classic "divide, conquer, and combine" approach often leads to efficient algorithms.

**Problem types:** Sorting, searching, tree problems, mathematical computations, closest pair problems.

```python
def merge_sort(nums):
    """
    Sort array using merge sort (classic divide & conquer).
    
    Divide: Split array into two halves
    Conquer: Recursively sort both halves  
    Combine: Merge sorted halves
    
    Time: O(n log n), Space: O(n)
    """
    if len(nums) <= 1:
        return nums
    
    # Divide: split into two halves
    mid = len(nums) // 2
    left_half = merge_sort(nums[:mid])
    right_half = merge_sort(nums[mid:])
    
    # Combine: merge sorted halves
    return merge_two_sorted_arrays(left_half, right_half)

def merge_two_sorted_arrays(left, right):
    """Helper function to merge two sorted arrays."""
    result = []
    i = j = 0
    
    # Merge elements in sorted order
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def quick_sort(nums):
    """
    Sort array using quicksort (divide & conquer with in-place partitioning).
    
    Divide: Partition around pivot
    Conquer: Recursively sort partitions
    Combine: No explicit combining needed (in-place)
    
    Average Time: O(n log n), Worst Time: O(n²), Space: O(log n)
    """
    def partition(arr, low, high):
        """Partition array around pivot, return pivot's final position."""
        # Choose rightmost element as pivot
        pivot = arr[high]
        
        # Index of smaller element
        i = low - 1
        
        for j in range(low, high):
            # If current element <= pivot
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        # Place pivot in correct position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def quick_sort_helper(arr, low, high):
        if low < high:
            # Partition and get pivot position
            pivot_pos = partition(arr, low, high)
            
            # Recursively sort elements before and after partition
            quick_sort_helper(arr, low, pivot_pos - 1)
            quick_sort_helper(arr, pivot_pos + 1, high)
    
    nums_copy = nums.copy()  # Don't modify original
    quick_sort_helper(nums_copy, 0, len(nums_copy) - 1)
    return nums_copy

def maximum_subarray_divide_conquer(nums):
    """
    Find maximum subarray sum using divide & conquer.
    
    Divide: Split array into left and right halves
    Conquer: Find max subarray in left half, right half, and crossing middle
    Combine: Return maximum of the three
    
    Time: O(n log n), Space: O(log n)
    """
    def max_crossing_sum(arr, left, mid, right):
        """Find maximum sum of subarray crossing the middle."""
        # Find max sum for left half ending at mid
        left_sum = float('-inf')
        current_sum = 0
        for i in range(mid, left - 1, -1):
            current_sum += arr[i]
            left_sum = max(left_sum, current_sum)
        
        # Find max sum for right half starting at mid+1
        right_sum = float('-inf')
        current_sum = 0
        for i in range(mid + 1, right + 1):
            current_sum += arr[i]
            right_sum = max(right_sum, current_sum)
        
        return left_sum + right_sum
    
    def max_subarray_helper(arr, left, right):
        # Base case: single element
        if left == right:
            return arr[left]
        
        # Divide
        mid = (left + right) // 2
        
        # Conquer: find max in left half, right half, and crossing
        left_max = max_subarray_helper(arr, left, mid)
        right_max = max_subarray_helper(arr, mid + 1, right)
        cross_max = max_crossing_sum(arr, left, mid, right)
        
        # Combine: return maximum of three possibilities
        return max(left_max, right_max, cross_max)
    
    if not nums:
        return 0
    
    return max_subarray_helper(nums, 0, len(nums) - 1)

def closest_pair_of_points(points):
    """
    Find closest pair of points in 2D plane.
    
    Divide: Split points by x-coordinate
    Conquer: Find closest pairs in left and right halves
    Combine: Check pairs crossing the dividing line
    
    Time: O(n log n), Space: O(n)
    """
    import math
    
    def distance(p1, p2):
        """Calculate Euclidean distance between two points."""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def brute_force_closest(pts):
        """Brute force for small arrays."""
        min_dist = float('inf')
        n = len(pts)
        closest_pair = None
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = distance(pts[i], pts[j])
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (pts[i], pts[j])
        
        return min_dist, closest_pair
    
    def closest_in_strip(strip, d):
        """Find closest points in vertical strip."""
        min_dist = d
        strip.sort(key=lambda p: p[1])  # Sort by y-coordinate
        closest_pair = None
        
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j][1] - strip[i][1]) < min_dist:
                dist = distance(strip[i], strip[j])
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (strip[i], strip[j])
                j += 1
        
        return min_dist, closest_pair
    
    def closest_pair_rec(px, py):
        """Recursive function for closest pair."""
        n = len(px)
        
        # Base case: use brute force for small arrays
        if n <= 3:
            return brute_force_closest(px)
        
        # Divide
        mid = n // 2
        midpoint = px[mid]
        
        pyl = [point for point in py if point[0] <= midpoint[0]]
        pyr = [point for point in py if point[0] > midpoint[0]]
        
        # Conquer
        dl, pair_l = closest_pair_rec(px[:mid], pyl)
        dr, pair_r = closest_pair_rec(px[mid:], pyr)
        
        # Find minimum of the two halves
        d = min(dl, dr)
        closest_pair = pair_l if dl <= dr else pair_r
        
        # Combine: check strip crossing the dividing line
        strip = [point for point in py if abs(point[0] - midpoint[0]) < d]
        strip_dist, strip_pair = closest_in_strip(strip, d)
        
        if strip_dist < d:
            return strip_dist, strip_pair
        else:
            return d, closest_pair
    
    # Sort points by x and y coordinates
    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])
    
    return closest_pair_rec(px, py)

def power_function(base, exponent):
    """
    Calculate base^exponent using divide & conquer (fast exponentiation).
    
    Key insight: base^n = (base^(n/2))^2 if n is even
                base^n = base * (base^(n/2))^2 if n is odd
    
    Time: O(log n), Space: O(log n)
    """
    def power_helper(base, exp):
        # Base cases
        if exp == 0:
            return 1
        if exp == 1:
            return base
        
        # Divide: calculate base^(exp//2)
        half_power = power_helper(base, exp // 2)
        
        # Combine
        if exp % 2 == 0:
            # Even exponent
            return half_power * half_power
        else:
            # Odd exponent
            return base * half_power * half_power
    
    if exponent < 0:
        return 1.0 / power_helper(base, -exponent)
    else:
        return power_helper(base, exponent)

def matrix_multiplication_strassen(A, B):
    """
    Multiply two matrices using Strassen's algorithm.
    
    Standard multiplication: O(n³)
    Strassen's algorithm: O(n^2.807)
    
    Divide each matrix into 4 quadrants, use 7 multiplications instead of 8.
    
    Time: O(n^2.807), Space: O(n²)
    """
    def add_matrices(X, Y):
        """Add two matrices."""
        n = len(X)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                result[i][j] = X[i][j] + Y[i][j]
        return result
    
    def subtract_matrices(X, Y):
        """Subtract two matrices."""
        n = len(X)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                result[i][j] = X[i][j] - Y[i][j]
        return result
    
    def strassen_multiply(X, Y):
        """Recursive Strassen multiplication."""
        n = len(X)
        
        # Base case: 1x1 matrix
        if n == 1:
            return [[X[0][0] * Y[0][0]]]
        
        # Divide matrices into quadrants
        mid = n // 2
        
        # A = [[A11, A12], [A21, A22]]
        A11 = [[X[i][j] for j in range(mid)] for i in range(mid)]
        A12 = [[X[i][j] for j in range(mid, n)] for i in range(mid)]
        A21 = [[X[i][j] for j in range(mid)] for i in range(mid, n)]
        A22 = [[X[i][j] for j in range(mid, n)] for i in range(mid, n)]
        
        # B = [[B11, B12], [B21, B22]]  
        B11 = [[Y[i][j] for j in range(mid)] for i in range(mid)]
        B12 = [[Y[i][j] for j in range(mid, n)] for i in range(mid)]
        B21 = [[Y[i][j] for j in range(mid)] for i in range(mid, n)]
        B22 = [[Y[i][j] for j in range(mid, n)] for i in range(mid, n)]
        
        # Calculate 7 products (Strassen's formulas)
        P1 = strassen_multiply(A11, subtract_matrices(B12, B22))
        P2 = strassen_multiply(add_matrices(A11, A12), B22)
        P3 = strassen_multiply(add_matrices(A21, A22), B11)
        P4 = strassen_multiply(A22, subtract_matrices(B21, B11))
        P5 = strassen_multiply(add_matrices(A11, A22), add_matrices(B11, B22))
        P6 = strassen_multiply(subtract_matrices(A12, A22), add_matrices(B21, B22))
        P7 = strassen_multiply(subtract_matrices(A11, A21), add_matrices(B11, B12))
        
        # Calculate result quadrants
        C11 = subtract_matrices(add_matrices(add_matrices(P5, P4), P6), P2)
        C12 = add_matrices(P1, P2)
        C21 = add_matrices(P3, P4)
        C22 = subtract_matrices(subtract_matrices(add_matrices(P5, P1), P3), P7)
        
        # Combine quadrants
        result = [[0] * n for _ in range(n)]
        for i in range(mid):
            for j in range(mid):
                result[i][j] = C11[i][j]
                result[i][j + mid] = C12[i][j]
                result[i + mid][j] = C21[i][j]
                result[i + mid][j + mid] = C22[i][j]
        
        return result
    
    return strassen_multiply(A, B)

def count_inversions(nums):
    """
    Count number of inversions in array using divide & conquer.
    An inversion is a pair (i, j) where i < j but nums[i] > nums[j].
    
    We modify merge sort to count inversions during merge step.
    
    Time: O(n log n), Space: O(n)
    """
    def merge_and_count(left, right):
        """Merge two sorted arrays and count inversions."""
        result = []
        i = j = inversions = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                # All remaining elements in left are greater than right[j]
                inversions += len(left) - i
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result, inversions
    
    def count_inversions_helper(arr):
        if len(arr) <= 1:
            return arr, 0
        
        mid = len(arr) // 2
        left_sorted, left_inv = count_inversions_helper(arr[:mid])
        right_sorted, right_inv = count_inversions_helper(arr[mid:])
        
        merged, split_inv = merge_and_count(left_sorted, right_sorted)
        
        total_inversions = left_inv + right_inv + split_inv
        return merged, total_inversions
    
    _, inversions = count_inversions_helper(nums)
    return inversions

# Example usage and comprehensive testing
print("=== Divide & Conquer Examples ===")

# Merge Sort
nums = [64, 34, 25, 12, 22, 11, 90]
sorted_nums = merge_sort(nums)
print(f"Original: {nums}")
print(f"Merge sorted: {sorted_nums}")

# Quick Sort
quick_sorted = quick_sort(nums)
print(f"Quick sorted: {quick_sorted}")

# Maximum subarray (divide & conquer vs Kadane's)
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
max_sum_dc = maximum_subarray_divide_conquer(nums)
print(f"Max subarray sum (D&C): {max_sum_dc}")

# Fast exponentiation
base, exp = 3, 10
result = power_function(base, exp)
print(f"{base}^{exp} = {result}")

# Closest pair of points
points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
min_dist, pair = closest_pair_of_points(points)
print(f"Closest pair: {pair}, distance: {min_dist:.2f}")

# Count inversions
nums = [8, 4, 2, 1]
inversions = count_inversions(nums)
print(f"Inversions in {nums}: {inversions}")  # 6



# Part V: Backtracking & Enumeration

## 16. Backtracking Pattern

**When to use:** Finding all solutions to a problem by exploring possibilities systematically, undoing choices that don't lead to solutions. Perfect for constraint satisfaction problems.

**Key insight:** Make a choice, explore its consequences, and if it doesn't work out, undo the choice (backtrack) and try the next option. Think of it as exploring a decision tree with the ability to "undo" bad decisions.

**Problem types:** Permutations, combinations, N-Queens, Sudoku, maze solving, word search.

```python
def generate_permutations(nums):
    """
    Generate all permutations of given numbers using backtracking.
    
    At each position, we try all available numbers, recurse,
    then backtrack by removing our choice.
    
    Time: O(n! × n), Space: O(n) for recursion stack
    """
    result = []
    
    def backtrack(current_permutation):
        # Base case: permutation is complete
        if len(current_permutation) == len(nums):
            result.append(current_permutation[:])  # Make a copy
            return
        
        for num in nums:
            if num not in current_permutation:
                # Make choice
                current_permutation.append(num)
                # Explore consequences
                backtrack(current_permutation)
                # Undo choice (backtrack)
                current_permutation.pop()
    
    backtrack([])
    return result

def generate_combinations(nums, k):
    """
    Generate all combinations of k elements from nums.
    
    We use index to avoid duplicates and ensure combinations
    (not permutations). Each element is either included or not.
    
    Time: O(C(n,k) × k), Space: O(k)
    """
    result = []
    
    def backtrack(start_index, current_combination):
        # Base case: combination is complete
        if len(current_combination) == k:
            result.append(current_combination[:])
            return
        
        # Try adding each remaining number
        for i in range(start_index, len(nums)):
            # Make choice
            current_combination.append(nums[i])
            # Explore with next available numbers
            backtrack(i + 1, current_combination)
            # Undo choice
            current_combination.pop()
    
    backtrack(0, [])
    return result

def solve_n_queens(n):
    """
    Solve N-Queens problem: place N queens on N×N chessboard
    such that no two queens attack each other.
    
    A queen attacks horizontally, vertically, and diagonally.
    We place queens row by row and check constraints.
    
    Time: O(N!), Space: O(N)
    """
    result = []
    board = ['.' * n for _ in range(n)]
    
    def is_safe(row, col):
        """Check if placing queen at (row, col) is safe."""
        # Check column
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        
        # Check diagonal (top-left to bottom-right)
        for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
            if board[i][j] == 'Q':
                return False
        
        # Check diagonal (top-right to bottom-left)
        for i, j in zip(range(row-1, -1, -1), range(col+1, n)):
            if board[i][j] == 'Q':
                return False
        
        return True
    
    def backtrack(row):
        # Base case: all queens placed successfully
        if row == n:
            result.append(board[:])  # Make a copy
            return
        
        # Try placing queen in each column of current row
        for col in range(n):
            if is_safe(row, col):
                # Make choice: place queen
                board[row] = board[row][:col] + 'Q' + board[row][col+1:]
                # Recurse to next row
                backtrack(row + 1)
                # Undo choice: remove queen
                board[row] = board[row][:col] + '.' + board[row][col+1:]
    
    backtrack(0)
    return result

def solve_sudoku(board):
    """
    Solve 9x9 Sudoku puzzle using backtracking.
    
    We find empty cells and try digits 1-9, checking constraints
    (row, column, 3x3 box). If digit works, recurse; otherwise backtrack.
    
    Time: O(9^(empty_cells)), Space: O(empty_cells)
    """
    def is_valid(board, row, col, num):
        """Check if placing num at (row, col) is valid."""
        # Check row
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def find_empty_cell(board):
        """Find next empty cell (marked with '.')."""
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    return i, j
        return None, None
    
    def solve():
        """Recursive backtracking solver."""
        row, col = find_empty_cell(board)
        
        # Base case: no empty cells, puzzle solved
        if row is None:
            return True
        
        # Try digits 1-9
        for num in '123456789':
            if is_valid(board, row, col, num):
                # Make choice
                board[row][col] = num
                
                # Recurse
                if solve():
                    return True
                
                # Undo choice (backtrack)
                board[row][col] = '.'
        
        return False  # No solution found
    
    solve()
    return board

def word_search(board, word):
    """
    Find if word exists in 2D character board.
    
    We can move horizontally or vertically. Each cell can be used
    at most once per word. Use backtracking to explore all paths.
    
    Time: O(N × 4^L) where N=cells, L=word length, Space: O(L)
    """
    if not board or not board[0] or not word:
        return False
    
    rows, cols = len(board), len(board[0])
    
    def backtrack(row, col, word_index):
        # Base case: found complete word
        if word_index == len(word):
            return True
        
        # Check bounds and character match
        if (row < 0 or row >= rows or col < 0 or col >= cols or
            board[row][col] != word[word_index] or 
            board[row][col] == '#'):  # Already visited
            return False
        
        # Mark cell as visited
        temp = board[row][col]
        board[row][col] = '#'
        
        # Explore all 4 directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        found = False
        
        for dr, dc in directions:
            if backtrack(row + dr, col + dc, word_index + 1):
                found = True
                break
        
        # Restore cell (backtrack)
        board[row][col] = temp
        
        return found
    
    # Try starting from each cell
    for i in range(rows):
        for j in range(cols):
            if backtrack(i, j, 0):
                return True
    
    return False

def generate_parentheses(n):
    """
    Generate all valid combinations of n pairs of parentheses.
    
    We build string character by character, ensuring we never
    have more closing than opening brackets.
    
    Time: O(4^n / √n), Space: O(4^n / √n)
    """
    result = []
    
    def backtrack(current_string, open_count, close_count):
        # Base case: string is complete
        if len(current_string) == 2 * n:
            result.append(current_string)
            return
        
        # Add opening bracket if we haven't used all
        if open_count < n:
            backtrack(current_string + '(', open_count + 1, close_count)
        
        # Add closing bracket if it doesn't exceed opening brackets
        if close_count < open_count:
            backtrack(current_string + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result

def palindrome_partitioning(s):
    """
    Partition string into all possible palindrome substrings.
    
    At each position, we try all possible palindromic prefixes,
    then recursively partition the remaining suffix.
    
    Time: O(N × 2^N), Space: O(N)
    """
    def is_palindrome(string, start, end):
        """Check if substring is palindrome."""
        while start < end:
            if string[start] != string[end]:
                return False
            start += 1
            end -= 1
        return True
    
    result = []
    
    def backtrack(start_index, current_partition):
        # Base case: processed entire string
        if start_index == len(s):
            result.append(current_partition[:])
            return
        
        # Try all possible endings for next palindrome
        for end_index in range(start_index, len(s)):
            if is_palindrome(s, start_index, end_index):
                # Make choice: add palindromic substring
                current_partition.append(s[start_index:end_index + 1])
                # Recurse on remaining string
                backtrack(end_index + 1, current_partition)
                # Undo choice
                current_partition.pop()
    
    backtrack(0, [])
    return result

def restore_ip_addresses(s):
    """
    Restore all possible valid IP addresses from string of digits.
    
    An IP address has 4 parts, each between 0-255.
    No leading zeros except for "0" itself.
    
    Time: O(1) since fixed number of possibilities, Space: O(1)
    """
    def is_valid_part(part):
        """Check if string is valid IP address part."""
        if not part or len(part) > 3:
            return False
        
        # No leading zeros except for "0"
        if len(part) > 1 and part[0] == '0':
            return False
        
        # Must be between 0-255
        return 0 <= int(part) <= 255
    
    result = []
    
    def backtrack(start_index, parts_count, current_ip):
        # Base case: 4 parts formed
        if parts_count == 4:
            if start_index == len(s):
                result.append(current_ip[:-1])  # Remove trailing dot
            return
        
        # Try all possible lengths for next part
        for length in range(1, 4):  # Parts can be 1-3 digits
            if start_index + length <= len(s):
                part = s[start_index:start_index + length]
                if is_valid_part(part):
                    backtrack(start_index + length, parts_count + 1, 
                             current_ip + part + '.')
    
    backtrack(0, 0, '')
    return result

# Example usage and comprehensive testing
print("=== Backtracking Examples ===")

# Permutations
nums = [1, 2, 3]
perms = generate_permutations(nums)
print(f"Permutations of {nums}: {perms}")

# Combinations
combs = generate_combinations([1, 2, 3, 4], 2)
print(f"Combinations of 2 from [1,2,3,4]: {combs}")

# N-Queens (show first solution)
n_queens = solve_n_queens(4)
print(f"N-Queens solutions for 4x4 board: {len(n_queens)} solutions")
print("First solution:")
for row in n_queens[0]:
    print(row)

# Generate parentheses
parens = generate_parentheses(3)
print(f"Valid parentheses for n=3: {parens}")

# Palindrome partitioning
s = "aab"
palindromes = palindrome_partitioning(s)
print(f"Palindrome partitions of '{s}': {palindromes}")

# IP address restoration
ip_string = "25525511135"
ip_addresses = restore_ip_addresses(ip_string)
print(f"Valid IP addresses from '{ip_string}': {ip_addresses}")



## 17. Subsets & Combinations Pattern

**When to use:** Generating all possible subsets, combinations, or when you need to consider "include/exclude" decisions for each element. This is a specialized form of backtracking.

**Key insight:** For each element, we have two choices: include it in the current subset or exclude it. This creates a binary decision tree that we can explore systematically.

**Problem types:** Power set generation, subset sum, combination sum, letter combinations.

```python
def generate_subsets(nums):
    """
    Generate all possible subsets (power set) of given array.
    
    For each element, we make binary choice: include or exclude.
    This gives us 2^n total subsets.
    
    Time: O(2^n × n), Space: O(2^n × n)
    """
    result = []
    
    def backtrack(start_index, current_subset):
        # Add current subset to result (including empty subset)
        result.append(current_subset[:])  # Make a copy
        
        # Try including each remaining element
        for i in range(start_index, len(nums)):
            # Include nums[i]
            current_subset.append(nums[i])
            # Recurse with next index
            backtrack(i + 1, current_subset)
            # Exclude nums[i] (backtrack)
            current_subset.pop()
    
    backtrack(0, [])
    return result

def subsets_with_duplicates(nums):
    """
    Generate subsets when array contains duplicates.
    
    Sort array first, then skip duplicate elements at same level
    to avoid duplicate subsets.
    
    Time: O(2^n × n), Space: O(2^n × n)
    """
    nums.sort()  # Sort to group duplicates together
    result = []
    
    def backtrack(start_index, current_subset):
        result.append(current_subset[:])
        
        for i in range(start_index, len(nums)):
            # Skip duplicates at same recursion level
            if i > start_index and nums[i] == nums[i-1]:
                continue
            
            current_subset.append(nums[i])
            backtrack(i + 1, current_subset)
            current_subset.pop()
    
    backtrack(0, [])
    return result

def combination_sum(candidates, target):
    """
    Find all combinations that sum to target.
    Same number can be used multiple times.
    
    At each step, we either include current candidate
    (and can use it again) or move to next candidate.
    
    Time: O(2^target), Space: O(target)
    """
    result = []
    candidates.sort()  # Sort for early termination
    
    def backtrack(start_index, current_combination, remaining_target):
        # Base case: found valid combination
        if remaining_target == 0:
            result.append(current_combination[:])
            return
        
        for i in range(start_index, len(candidates)):
            candidate = candidates[i]
            
            # Early termination: remaining candidates are too large
            if candidate > remaining_target:
                break
            
            # Include current candidate
            current_combination.append(candidate)
            # Can reuse same candidate, so pass i (not i+1)
            backtrack(i, current_combination, remaining_target - candidate)
            # Backtrack
            current_combination.pop()
    
    backtrack(0, [], target)
    return result

def combination_sum_unique(candidates, target):
    """
    Find combinations that sum to target.
    Each candidate can be used at most once.
    Array may contain duplicates.
    
    Time: O(2^n), Space: O(target)
    """
    candidates.sort()  # Sort to handle duplicates
    result = []
    
    def backtrack(start_index, current_combination, remaining_target):
        if remaining_target == 0:
            result.append(current_combination[:])
            return
        
        for i in range(start_index, len(candidates)):
            candidate = candidates[i]
            
            # Skip duplicates at same level
            if i > start_index and candidates[i] == candidates[i-1]:
                continue
            
            # Early termination
            if candidate > remaining_target:
                break
            
            current_combination.append(candidate)
            # Move to next index since we can't reuse
            backtrack(i + 1, current_combination, remaining_target - candidate)
            current_combination.pop()
    
    backtrack(0, [], target)
    return result

def letter_combinations_phone(digits):
    """
    Generate all letter combinations from phone number digits.
    
    Each digit maps to several letters. We build combinations
    by choosing one letter from each digit.
    
    Time: O(4^n × n), Space: O(4^n × n)
    """
    if not digits:
        return []
    
    # Phone digit to letters mapping
    phone_map = {
        '2': 'abc',
        '3': 'def', 
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    result = []
    
    def backtrack(index, current_combination):
        # Base case: processed all digits
        if index == len(digits):
            result.append(current_combination)
            return
        
        # Get letters for current digit
        current_digit = digits[index]
        letters = phone_map.get(current_digit, '')
        
        # Try each letter for current digit
        for letter in letters:
            backtrack(index + 1, current_combination + letter)
    
    backtrack(0, '')
    return result

def subset_sum_equal_partition(nums):
    """
    Check if array can be partitioned into two subsets with equal sum.
    
    This is equivalent to finding a subset that sums to total_sum/2.
    We can use backtracking, but DP is more efficient for this problem.
    
    Time: O(sum × n), Space: O(sum × n)
    """
    total_sum = sum(nums)
    
    # If total sum is odd, can't partition equally
    if total_sum % 2 != 0:
        return False
    
    target = total_sum // 2
    
    def backtrack(index, current_sum):
        # Base cases
        if current_sum == target:
            return True
        if index >= len(nums) or current_sum > target:
            return False
        
        # Include current number or exclude it
        return (backtrack(index + 1, current_sum + nums[index]) or
                backtrack(index + 1, current_sum))
    
    return backtrack(0, 0)

def generate_binary_strings(n):
    """
    Generate all binary strings of length n.
    
    At each position, we choose either '0' or '1'.
    This demonstrates the basic template for binary choices.
    
    Time: O(2^n × n), Space: O(2^n × n)
    """
    result = []
    
    def backtrack(current_string):
        # Base case: string is complete
        if len(current_string) == n:
            result.append(current_string)
            return
        
        # Choice 1: append '0'
        backtrack(current_string + '0')
        
        # Choice 2: append '1'  
        backtrack(current_string + '1')
    
    backtrack('')
    return result

def k_sum_combinations(nums, k, target):
    """
    Find all combinations of k numbers that sum to target.
    
    This combines subset generation with sum constraint
    and fixed size constraint.
    
    Time: O(C(n,k) × k), Space: O(k)
    """
    result = []
    nums.sort()
    
    def backtrack(start_index, current_combination, remaining_target, remaining_count):
        # Base case: found valid combination
        if remaining_count == 0:
            if remaining_target == 0:
                result.append(current_combination[:])
            return
        
        # Early termination conditions
        if remaining_target <= 0 or start_index >= len(nums):
            return
        
        for i in range(start_index, len(nums)):
            # Skip if remaining numbers can't possibly reach target
            if nums[i] > remaining_target:
                break
            
            # Skip if not enough numbers remaining
            if len(nums) - i < remaining_count:
                break
            
            current_combination.append(nums[i])
            backtrack(i + 1, current_combination, 
                     remaining_target - nums[i], remaining_count - 1)
            current_combination.pop()
    
    backtrack(0, [], target, k)
    return result

def word_break_all_sentences(s, word_dict):
    """
    Find all possible sentences formed by breaking string using word dictionary.
    
    At each position, we try all possible words that match the prefix,
    then recursively solve for the remaining string.
    
    Time: O(2^n × n), Space: O(2^n × n)
    """
    word_set = set(word_dict)  # O(1) lookup
    result = []
    
    def backtrack(start_index, current_sentence):
        # Base case: processed entire string
        if start_index == len(s):
            result.append(' '.join(current_sentence))
            return
        
        # Try all possible words starting at current position
        for end_index in range(start_index + 1, len(s) + 1):
            word = s[start_index:end_index]
            if word in word_set:
                current_sentence.append(word)
                backtrack(end_index, current_sentence)
                current_sentence.pop()
    
    backtrack(0, [])
    return result

# Example usage and comprehensive testing
print("=== Subsets & Combinations Examples ===")

# Generate all subsets
nums = [1, 2, 3]
subsets = generate_subsets(nums)
print(f"All subsets of {nums}: {subsets}")

# Subsets with duplicates
nums_dup = [1, 2, 2]
subsets_dup = subsets_with_duplicates(nums_dup)
print(f"Subsets with duplicates {nums_dup}: {subsets_dup}")

# Combination sum
candidates = [2, 3, 6, 7]
target = 7
comb_sum = combination_sum(candidates, target)
print(f"Combination sum for target {target}: {comb_sum}")

# Letter combinations
digits = "23"
letter_combs = letter_combinations_phone(digits)
print(f"Letter combinations for '{digits}': {letter_combs}")

# Binary strings
n = 3
binary_strings = generate_binary_strings(n)
print(f"Binary strings of length {n}: {binary_strings}")

# Equal partition
nums = [1, 5, 11, 5]
can_partition = subset_sum_equal_partition(nums)
print(f"Can partition {nums} equally: {can_partition}")

# K-sum combinations
nums = [1, 2, 3, 4]
k_combs = k_sum_combinations(nums, 2, 5)
print(f"2-sum combinations with target 5: {k_combs}")

# Word break sentences
s = "catsanddog"
words = ["cat", "cats", "and", "sand", "dog"]
sentences = word_break_all_sentences(s, words)
print(f"All sentences from '{s}': {sentences}")



# Part VI: Greedy & Selection

## 18. Greedy Algorithm Pattern

**When to use:** When local optimal choices lead to global optimal solution. Problems where making the best immediate choice doesn't prevent finding the overall best solution.

**Key insight:** Make the best choice at each step without reconsidering previous choices. This works when the problem has optimal substructure and the greedy choice property.

**Problem types:** Activity selection, fractional knapsack, Huffman coding, minimum spanning trees.

```python
def activity_selection_greedy(activities):
    """
    Select maximum number of non-overlapping activities.
    
    Greedy choice: Always select activity that finishes earliest.
    This leaves maximum room for subsequent activities.
    
    Time: O(n log n), Space: O(1)
    """
    if not activities:
        return []
    
    # Sort by finish time (key greedy insight)
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]  # Always select first activity
    last_finish_time = activities[0][1]
    
    for start, finish in activities[1:]:
        # Select if activity doesn't overlap with last selected
        if start >= last_finish_time:
            selected.append((start, finish))
            last_finish_time = finish
    
    return selected

def fractional_knapsack(items, capacity):
    """
    Fractional knapsack: maximize value within weight capacity.
    Items can be broken into fractions.
    
    Greedy choice: Sort by value/weight ratio, take highest ratios first.
    
    Time: O(n log n), Space: O(1)
    """
    # Calculate value/weight ratio for each item
    items_with_ratio = []
    for i, (weight, value) in enumerate(items):
        ratio = value / weight if weight > 0 else 0
        items_with_ratio.append((ratio, weight, value, i))
    
    # Sort by ratio in descending order
    items_with_ratio.sort(reverse=True)
    
    total_value = 0
    remaining_capacity = capacity
    selected_items = []
    
    for ratio, weight, value, original_index in items_with_ratio:
        if remaining_capacity == 0:
            break
        
        if weight <= remaining_capacity:
            # Take entire item
            total_value += value
            remaining_capacity -= weight
            selected_items.append((original_index, 1.0, value))
        else:
            # Take fraction of item
            fraction = remaining_capacity / weight
            total_value += value * fraction
            selected_items.append((original_index, fraction, value * fraction))
            remaining_capacity = 0
    
    return total_value, selected_items

def job_scheduling_deadlines(jobs):
    """
    Schedule jobs to maximize profit within deadlines.
    
    Greedy choice: Sort by profit, assign to latest possible slot.
    
    Time: O(n²), Space: O(n)
    """
    if not jobs:
        return [], 0
    
    # Sort jobs by profit in descending order
    jobs.sort(key=lambda x: x[1], reverse=True)  # (deadline, profit, job_id)
    
    # Find maximum deadline to determine time slots
    max_deadline = max(job[0] for job in jobs)
    
    # Initialize time slots as empty
    time_slots = [None] * max_deadline
    scheduled_jobs = []
    total_profit = 0
    
    for deadline, profit, job_id in jobs:
        # Find latest available slot before deadline
        for slot in range(min(deadline - 1, max_deadline - 1), -1, -1):
            if time_slots[slot] is None:
                # Schedule job in this slot
                time_slots[slot] = job_id
                scheduled_jobs.append((job_id, slot + 1, profit))
                total_profit += profit
                break
    
    return scheduled_jobs, total_profit

def minimum_coins_greedy(coins, amount):
    """
    Find minimum coins needed using greedy approach.
    Works for standard denominations (1, 5, 10, 25, etc.)
    
    Greedy choice: Always use largest denomination possible.
    
    Time: O(k) where k is number of denominations, Space: O(1)
    """
    coins.sort(reverse=True)  # Start with largest denomination
    coin_count = 0
    result = []
    
    for coin in coins:
        if amount >= coin:
            count = amount // coin
            coin_count += count
            result.extend([coin] * count)
            amount -= count * coin
    
    return result if amount == 0 else []  # Return empty if amount can't be made

def gas_station_circular_tour(gas, cost):
    """
    Find starting gas station for circular tour.
    
    Greedy insight: If we can't reach station i from any previous station,
    then station i+1 is the earliest possible starting point.
    
    Time: O(n), Space: O(1)
    """
    total_tank = 0
    current_tank = 0
    start_station = 0
    
    for i in range(len(gas)):
        total_tank += gas[i] - cost[i]
        current_tank += gas[i] - cost[i]
        
        # If we can't reach next station from current start
        if current_tank < 0:
            # Try starting from next station
            start_station = i + 1
            current_tank = 0
    
    # Check if tour is possible
    return start_station if total_tank >= 0 else -1

def jump_game_greedy(nums):
    """
    Determine if we can reach the last index.
    
    Greedy insight: Keep track of farthest position reachable.
    If current position is within reach, update farthest.
    
    Time: O(n), Space: O(1)
    """
    farthest = 0
    
    for i in range(len(nums)):
        # If current position is unreachable
        if i > farthest:
            return False
        
        # Update farthest reachable position
        farthest = max(farthest, i + nums[i])
        
        # Early termination: already can reach end
        if farthest >= len(nums) - 1:
            return True
    
    return farthest >= len(nums) - 1

def minimum_jumps_to_end(nums):
    """
    Find minimum jumps needed to reach end.
    
    Greedy insight: For each jump, we choose the position that
    allows us to reach farthest in the next jump.
    
    Time: O(n), Space: O(1)
    """
    if len(nums) <= 1:
        return 0
    
    jumps = 0
    current_max_reach = 0  # Farthest we can reach with current jumps
    next_max_reach = 0     # Farthest we can reach with one more jump
    
    for i in range(len(nums) - 1):  # Don't need to jump from last position
        # Update farthest we can reach with one more jump
        next_max_reach = max(next_max_reach, i + nums[i])
        
        # If we've reached the limit of current jump count
        if i == current_max_reach:
            jumps += 1
            current_max_reach = next_max_reach
            
            # Early termination
            if current_max_reach >= len(nums) - 1:
                break
    
    return jumps

def remove_k_digits_smallest(num_string, k):
    """
    Remove k digits to form smallest possible number.
    
    Greedy insight: Remove the first digit that is greater than
    its next digit. If no such digit exists, remove from right.
    
    Time: O(n), Space: O(n)
    """
    stack = []
    removals = k
    
    for digit in num_string:
        # Remove digits from stack while current digit is smaller
        while removals > 0 and stack and stack[-1] > digit:
            stack.pop()
            removals -= 1
        
        stack.append(digit)
    
    # Remove remaining digits from right if needed
    while removals > 0:
        stack.pop()
        removals -= 1
    
    # Convert to number and handle leading zeros
    result = ''.join(stack).lstrip('0')
    return result if result else '0'

def partition_labels(s):
    """
    Partition string so that each letter appears in at most one part.
    Maximize number of parts.
    
    Greedy insight: For each part, extend it to include all occurrences
    of letters seen so far.
    
    Time: O(n), Space: O(1)
    """
    # Find last occurrence of each character
    last_occurrence = {char: i for i, char in enumerate(s)}
    
    partitions = []
    start = 0
    end = 0
    
    for i, char in enumerate(s):
        # Extend current partition to include all occurrences of char
        end = max(end, last_occurrence[char])
        
        # If we've reached the end of current partition
        if i == end:
            partitions.append(end - start + 1)
            start = i + 1
    
    return partitions

def candy_distribution(ratings):
    """
    Distribute candy to children based on ratings.
    Each child gets at least 1 candy.
    Children with higher ratings get more candy than neighbors.
    
    Greedy approach: Two passes - left to right, then right to left.
    
    Time: O(n), Space: O(n)
    """
    n = len(ratings)
    if n == 0:
        return 0
    
    candies = [1] * n  # Each child gets at least 1 candy
    
    # Left to right pass: handle increasing sequences
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            candies[i] = candies[i-1] + 1
    
    # Right to left pass: handle decreasing sequences
    for i in range(n-2, -1, -1):
        if ratings[i] > ratings[i+1]:
            candies[i] = max(candies[i], candies[i+1] + 1)
    
    return sum(candies)

# Example usage and comprehensive testing
print("=== Greedy Algorithm Examples ===")

# Activity selection
activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)]
selected_activities = activity_selection_greedy(activities)
print(f"Selected activities: {selected_activities}")

# Fractional knapsack
items = [(10, 60), (20, 100), (30, 120)]  # (weight, value)
capacity = 50
max_value, selected = fractional_knapsack(items, capacity)
print(f"Fractional knapsack max value: {max_value}")

# Job scheduling
jobs = [(4, 20, 'a'), (1, 10, 'b'), (1, 40, 'c'), (1, 30, 'd')]  # (deadline, profit, id)
scheduled, profit = job_scheduling_deadlines(jobs)
print(f"Scheduled jobs: {scheduled}, Total profit: {profit}")

# Minimum coins
coins = [25, 10, 5, 1]
amount = 67
min_coins = minimum_coins_greedy(coins, amount)
print(f"Minimum coins for {amount}: {min_coins}")

# Gas station tour
gas = [1, 2, 3, 4, 5]
cost = [3, 4, 5, 1, 2]
start = gas_station_circular_tour(gas, cost)
print(f"Gas station tour starts at: {start}")

# Jump game
nums = [2, 3, 1, 1, 4]
can_jump = jump_game_greedy(nums)
min_jumps = minimum_jumps_to_end(nums)
print(f"Can jump to end: {can_jump}, Min jumps: {min_jumps}")

# Remove k digits
num_str = "1432219"
k = 3
smallest = remove_k_digits_smallest(num_str, k)
print(f"Remove {k} digits from {num_str}: {smallest}")

# Partition labels
s = "ababcbacadefegdehijhklij"
partitions = partition_labels(s)
print(f"Partition sizes for '{s}': {partitions}")

# Candy distribution
ratings = [1, 0, 2]
total_candies = candy_distribution(ratings)
print(f"Total candies needed for ratings {ratings}: {total_candies}")



## 19. Top K Elements Pattern

**When to use:** Finding k largest, smallest, or most/least frequent elements. When you need to maintain a dynamic set of top elements or when dealing with streaming data.

**Key insight:** Use heaps to efficiently maintain k elements. Min-heap for k largest elements, max-heap for k smallest elements. This avoids sorting the entire dataset.

**Problem types:** Kth largest element, top k frequent elements, k closest points, merge k sorted lists.

```python
import heapq
from collections import Counter

def find_kth_largest_heap(nums, k):
    """
    Find kth largest element using min-heap.
    
    Maintain min-heap of size k. The root is always kth largest.
    If heap size exceeds k, remove smallest element.
    
    Time: O(n log k), Space: O(k)
    """
    min_heap = []
    
    for num in nums:
        heapq.heappush(min_heap, num)
        
        # Keep only k largest elements
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    
    return min_heap[0]  # kth largest element

def top_k_frequent_elements(nums, k):
    """
    Find k most frequent elements.
    
    Count frequencies, then use min-heap to maintain k most frequent.
    
    Time: O(n log k), Space: O(n)
    """
    # Count frequencies
    freq_map = Counter(nums)
    
    # Use min-heap to keep k most frequent elements
    min_heap = []
    
    for num, freq in freq_map.items():
        heapq.heappush(min_heap, (freq, num))
        
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    
    # Extract elements (frequencies not needed in result)
    return [num for freq, num in min_heap]

def k_closest_points_to_origin(points, k):
    """
    Find k points closest to origin (0, 0).
    
    Use max-heap to maintain k closest points based on distance squared.
    
    Time: O(n log k), Space: O(k)
    """
    def distance_squared(point):
        return point[0]**2 + point[1]**2
    
    max_heap = []
    
    for point in points:
        dist_sq = distance_squared(point)
        
        # Python heapq is min-heap, so negate for max-heap behavior
        heapq.heappush(max_heap, (-dist_sq, point))
        
        if len(max_heap) > k:
            heapq.heappop(max_heap)
    
    return [point for dist, point in max_heap]

def kth_smallest_in_matrix(matrix, k):
    """
    Find kth smallest element in sorted matrix.
    Each row and column is sorted in ascending order.
    
    Use min-heap to explore matrix in order of increasing values.
    
    Time: O(k log min(k, m, n)), Space: O(min(k, m, n))
    """
    if not matrix or not matrix[0]:
        return None
    
    m, n = len(matrix), len(matrix[0])
    
    # Min-heap: (value, row, col)
    min_heap = [(matrix[0][0], 0, 0)]
    visited = {(0, 0)}
    
    for _ in range(k):
        value, row, col = heapq.heappop(min_heap)
        
        if _ == k - 1:  # Found kth smallest
            return value
        
        # Add adjacent elements to heap
        for dr, dc in [(0, 1), (1, 0)]:  # Right and down
            new_row, new_col = row + dr, col + dc
            
            if (new_row < m and new_col < n and 
                (new_row, new_col) not in visited):
                
                heapq.heappush(min_heap, (matrix[new_row][new_col], new_row, new_col))
                visited.add((new_row, new_col))
    
    return None

def merge_k_sorted_lists(lists):
    """
    Merge k sorted linked lists into one sorted list.
    
    Use min-heap to always merge the smallest current elements.
    
    Time: O(n log k) where n is total nodes, Space: O(k)
    """
    class ListNode:
        def __init__(self, val=0, next=None):
            self.val = val
            self.next = next
        
        def __lt__(self, other):
            return self.val < other.val
    
    if not lists:
        return None
    
    # Initialize heap with head of each list
    min_heap = []
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(min_heap, (head.val, i, head))
    
    dummy = ListNode(0)
    current = dummy
    
    while min_heap:
        val, list_idx, node = heapq.heappop(min_heap)
        
        # Add node to result
        current.next = node
        current = current.next
        
        # Add next node from same list to heap
        if node.next:
            heapq.heappush(min_heap, (node.next.val, list_idx, node.next))
    
    return dummy.next

def sliding_window_maximum(nums, k):
    """
    Find maximum in each sliding window of size k.
    
    Use max-heap with indices to handle window sliding.
    Remove elements outside current window.
    
    Time: O(n log k), Space: O(k)
    """
    if not nums or k == 0:
        return []
    
    result = []
    max_heap = []  # (negative_value, index) for max-heap behavior
    
    for i, num in enumerate(nums):
        # Add current element to heap
        heapq.heappush(max_heap, (-num, i))
        
        # Remove elements outside current window
        while max_heap and max_heap[0][1] <= i - k:
            heapq.heappop(max_heap)
        
        # Record maximum for current window
        if i >= k - 1:  # Window is complete
            result.append(-max_heap[0][0])
    
    return result

def k_smallest_pairs_sum(nums1, nums2, k):
    """
    Find k pairs with smallest sums from two sorted arrays.
    
    Use min-heap to explore pairs in order of increasing sum.
    Start with pairs involving first element of nums1.
    
    Time: O(k log k), Space: O(k)
    """
    if not nums1 or not nums2 or k == 0:
        return []
    
    # Min-heap: (sum, index1, index2)
    min_heap = [(nums1[0] + nums2[0], 0, 0)]
    visited = {(0, 0)}
    result = []
    
    for _ in range(min(k, len(nums1) * len(nums2))):
        pair_sum, i, j = heapq.heappop(min_heap)
        result.append([nums1[i], nums2[j]])
        
        # Add adjacent pairs
        if i + 1 < len(nums1) and (i + 1, j) not in visited:
            heapq.heappush(min_heap, (nums1[i + 1] + nums2[j], i + 1, j))
            visited.add((i + 1, j))
        
        if j + 1 < len(nums2) and (i, j + 1) not in visited:
            heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))
            visited.add((i, j + 1))
    
    return result

def reorganize_string_max_heap(s):
    """
    Reorganize string so no two adjacent characters are same.
    
    Use max-heap to always place most frequent remaining character.
    Alternate between two most frequent characters.
    
    Time: O(n log k) where k is unique characters, Space: O(k)
    """
    # Count frequencies
    freq_map = Counter(s)
    
    # Max-heap of frequencies (negate for max-heap behavior)
    max_heap = [(-freq, char) for char, freq in freq_map.items()]
    heapq.heapify(max_heap)
    
    result = []
    prev_char = None
    prev_freq = 0
    
    while max_heap:
        # Get most frequent character
        freq, char = heapq.heappop(max_heap)
        freq = -freq
        
        result.append(char)
        
        # Add back previous character if it still has frequency
        if prev_char and prev_freq > 0:
            heapq.heappush(max_heap, (-prev_freq, prev_char))
        
        # Update previous character info
        prev_char = char
        prev_freq = freq - 1
    
    # Check if reorganization is possible
    reorganized = ''.join(result)
    if len(reorganized) != len(s):
        return ""  # Impossible to reorganize
    
    return reorganized

def find_median_data_stream():
    """
    Design data structure to find median from data stream.
    
    Use two heaps: max-heap for smaller half, min-heap for larger half.
    Balance heaps to ensure sizes differ by at most 1.
    
    Time: O(log n) for add, O(1) for median, Space: O(n)
    """
    class MedianFinder:
        def __init__(self):
            self.small = []  # max-heap (negated values)
            self.large = []  # min-heap
        
        def add_number(self, num):
            # Add to appropriate heap
            if not self.small or num <= -self.small[0]:
                heapq.heappush(self.small, -num)
            else:
                heapq.heappush(self.large, num)
            
            # Balance heaps
            if len(self.small) > len(self.large) + 1:
                val = -heapq.heappop(self.small)
                heapq.heappush(self.large, val)
            elif len(self.large) > len(self.small) + 1:
                val = heapq.heappop(self.large)
                heapq.heappush(self.small, -val)
        
        def find_median(self):
            if len(self.small) == len(self.large):
                return (-self.small[0] + self.large[0]) / 2.0
            elif len(self.small) > len(self.large):
                return -self.small[0]
            else:
                return self.large[0]
    
    return MedianFinder()

# Example usage and comprehensive testing
print("=== Top K Elements Examples ===")

# Kth largest element
nums = [3, 2, 1, 5, 6, 4]
k = 2
kth_largest = find_kth_largest_heap(nums, k)
print(f"{k}th largest in {nums}: {kth_largest}")

# Top k frequent elements
nums = [1, 1, 1, 2, 2, 3]
k = 2
top_k_freq = top_k_frequent_elements(nums, k)
print(f"Top {k} frequent in {nums}: {top_k_freq}")

# K closest points
points = [[1, 1], [1, 3], [3, 4], [2, 1], [0, 0]]
k = 3
closest_points = k_closest_points_to_origin(points, k)
print(f"{k} closest points: {closest_points}")

# Kth smallest in matrix
matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
k = 8
kth_smallest_matrix = kth_smallest_in_matrix(matrix, k)
print(f"{k}th smallest in matrix: {kth_smallest_matrix}")

# Sliding window maximum
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
sliding_max = sliding_window_maximum(nums, k)
print(f"Sliding window maximum (k={k}): {sliding_max}")

# K smallest pairs
nums1 = [1, 7, 11]
nums2 = [2, 4, 6]
k = 3
smallest_pairs = k_smallest_pairs_sum(nums1, nums2, k)
print(f"{k} smallest pairs: {smallest_pairs}")

# Reorganize string
s = "aab"
reorganized = reorganize_string_max_heap(s)
print(f"Reorganized '{s}': '{reorganized}'")

# Median from data stream
median_finder = find_median_data_stream()
for num in [1, 2, 3, 4, 5]:
    median_finder.add_number(num)
    print(f"Added {num}, median: {median_finder.find_median()}")



## 20. K-way Merge Pattern

**When to use:** Merging multiple sorted sequences, finding elements across multiple sorted data structures, or when you need to maintain order while combining k sorted inputs.

**Key insight:** Use a min-heap to always pick the smallest element among the current candidates from all k sequences. This maintains overall sorted order efficiently.

**Problem types:** Merge k sorted arrays/lists, smallest range covering elements from k lists, k pairs with smallest sums.

```python
import heapq

def merge_k_sorted_arrays(arrays):
    """
    Merge k sorted arrays into one sorted array.
    
    Use min-heap to track smallest element from each array.
    Always pick globally smallest element and advance its array pointer.
    
    Time: O(n log k) where n is total elements, Space: O(k)
    """
    if not arrays:
        return []
    
    result = []
    # Min-heap: (value, array_index, element_index)
    min_heap = []
    
    # Initialize heap with first element from each array
    for i, arr in enumerate(arrays):
        if arr:  # Check if array is not empty
            heapq.heappush(min_heap, (arr[0], i, 0))
    
    while min_heap:
        value, array_idx, element_idx = heapq.heappop(min_heap)
        result.append(value)
        
        # Add next element from same array if available
        if element_idx + 1 < len(arrays[array_idx]):
            next_value = arrays[array_idx][element_idx + 1]
            heapq.heappush(min_heap, (next_value, array_idx, element_idx + 1))
    
    return result

def smallest_range_covering_k_lists(nums):
    """
    Find smallest range that includes at least one element from each list.
    
    Use min-heap to track current elements from each list.
    Maintain current range and update minimum range found.
    
    Time: O(n log k), Space: O(k)
    """
    if not nums:
        return []
    
    # Min-heap: (value, list_index, element_index)
    min_heap = []
    current_max = float('-inf')
    
    # Initialize heap with first element from each list
    for i, lst in enumerate(nums):
        if lst:
            heapq.heappush(min_heap, (lst[0], i, 0))
            current_max = max(current_max, lst[0])
    
    min_range_size = float('inf')
    range_start, range_end = 0, 0
    
    while len(min_heap) == len(nums):  # All lists are represented
        current_min, list_idx, element_idx = heapq.heappop(min_heap)
        
        # Update minimum range if current range is smaller
        if current_max - current_min < min_range_size:
            min_range_size = current_max - current_min
            range_start, range_end = current_min, current_max
        
        # Add next element from same list
        if element_idx + 1 < len(nums[list_idx]):
            next_val = nums[list_idx][element_idx + 1]
            heapq.heappush(min_heap, (next_val, list_idx, element_idx + 1))
            current_max = max(current_max, next_val)
    
    return [range_start, range_end]

class ListNode:
    """Helper class for linked list operations."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_sorted_linked_lists(lists):
    """
    Merge k sorted linked lists into one sorted list.
    
    Use min-heap to always merge the node with smallest value.
    Add next node from same list after processing current node.
    
    Time: O(n log k), Space: O(k)
    """
    if not lists:
        return None
    
    # Min-heap: (node_value, unique_id, node)
    # unique_id prevents comparison of nodes when values are equal
    min_heap = []
    node_id = 0
    
    # Initialize heap with head of each non-empty list
    for head in lists:
        if head:
            heapq.heappush(min_heap, (head.val, node_id, head))
            node_id += 1
    
    # Create dummy head for result list
    dummy = ListNode(0)
    current = dummy
    
    while min_heap:
        val, _, node = heapq.heappop(min_heap)
        
        # Add current node to result
        current.next = node
        current = current.next
        
        # Add next node from same list if available
        if node.next:
            heapq.heappush(min_heap, (node.next.val, node_id, node.next))
            node_id += 1
    
    return dummy.next

def kth_smallest_in_m_sorted_arrays(arrays, k):
    """
    Find kth smallest element among m sorted arrays.
    
    Similar to merge k arrays, but stop after finding kth element.
    
    Time: O(k log m), Space: O(m)
    """
    if not arrays or k <= 0:
        return None
    
    # Min-heap: (value, array_index, element_index)
    min_heap = []
    
    # Initialize heap with first element from each array
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(min_heap, (arr[0], i, 0))
    
    count = 0
    while min_heap and count < k:
        value, array_idx, element_idx = heapq.heappop(min_heap)
        count += 1
        
        # If this is the kth element, return it
        if count == k:
            return value
        
        # Add next element from same array
        if element_idx + 1 < len(arrays[array_idx]):
            next_value = arrays[array_idx][element_idx + 1]
            heapq.heappush(min_heap, (next_value, array_idx, element_idx + 1))
    
    return None

def merge_intervals_from_k_lists(interval_lists):
    """
    Merge overlapping intervals from k sorted interval lists.
    
    First merge all intervals using k-way merge, then merge overlaps.
    
    Time: O(n log k + n log n), Space: O(n)
    """
    if not interval_lists:
        return []
    
    # Merge all intervals from k lists
    all_intervals = []
    min_heap = []
    
    # Initialize heap with first interval from each list
    for i, intervals in enumerate(interval_lists):
        if intervals:
            start, end = intervals[0]
            heapq.heappush(min_heap, (start, end, i, 0))
    
    # Collect all intervals in sorted order by start time
    while min_heap:
        start, end, list_idx, interval_idx = heapq.heappop(min_heap)
        all_intervals.append([start, end])
        
        # Add next interval from same list
        if interval_idx + 1 < len(interval_lists[list_idx]):
            next_start, next_end = interval_lists[list_idx][interval_idx + 1]
            heapq.heappush(min_heap, (next_start, next_end, list_idx, interval_idx + 1))
    
    # Merge overlapping intervals
    if not all_intervals:
        return []
    
    merged = [all_intervals[0]]
    for current in all_intervals[1:]:
        last_merged = merged[-1]
        
        if current[0] <= last_merged[1]:  # Overlapping
            last_merged[1] = max(last_merged[1], current[1])
        else:  # Non-overlapping
            merged.append(current)
    
    return merged

def k_way_merge_with_condition(arrays, condition_func):
    """
    Generic k-way merge with custom condition function.
    
    Allows custom logic for determining which element to pick next.
    condition_func(elements) returns index of element to pick.
    
    Time: O(n log k), Space: O(k)
    """
    if not arrays:
        return []
    
    result = []
    # Track current position in each array
    positions = [0] * len(arrays)
    
    while True:
        # Get current elements from each array
        current_elements = []
        for i, arr in enumerate(arrays):
            if positions[i] < len(arr):
                current_elements.append((arr[positions[i]], i))
            else:
                current_elements.append((None, i))
        
        # Filter out exhausted arrays
        valid_elements = [(val, idx) for val, idx in current_elements if val is not None]
        
        if not valid_elements:
            break
        
        # Apply condition function to choose next element
        chosen_idx = condition_func([val for val, _ in valid_elements])
        chosen_value, array_idx = valid_elements[chosen_idx]
        
        result.append(chosen_value)
        positions[array_idx] += 1
    
    return result

def find_k_pairs_smallest_sum_multiple_arrays(arrays, k):
    """
    Find k pairs with smallest sum from multiple arrays.
    Each pair contains one element from each array.
    
    Use min-heap to explore pairs in order of increasing sum.
    
    Time: O(k log k), Space: O(k)
    """
    if not arrays or k == 0:
        return []
    
    num_arrays = len(arrays)
    if any(not arr for arr in arrays):
        return []
    
    # Min-heap: (sum, [indices])
    min_heap = []
    visited = set()
    
    # Start with first element from each array
    initial_indices = tuple([0] * num_arrays)
    initial_sum = sum(arrays[i][0] for i in range(num_arrays))
    heapq.heappush(min_heap, (initial_sum, initial_indices))
    visited.add(initial_indices)
    
    result = []
    
    for _ in range(k):
        if not min_heap:
            break
        
        current_sum, indices = heapq.heappop(min_heap)
        
        # Create pair from current indices
        pair = [arrays[i][indices[i]] for i in range(num_arrays)]
        result.append(pair)
        
        # Generate next candidates by incrementing each index
        for i in range(num_arrays):
            if indices[i] + 1 < len(arrays[i]):
                new_indices = list(indices)
                new_indices[i] += 1
                new_indices_tuple = tuple(new_indices)
                
                if new_indices_tuple not in visited:
                    new_sum = sum(arrays[j][new_indices[j]] for j in range(num_arrays))
                    heapq.heappush(min_heap, (new_sum, new_indices_tuple))
                    visited.add(new_indices_tuple)
    
    return result

# Example usage and comprehensive testing
print("=== K-way Merge Examples ===")

# Merge k sorted arrays
arrays = [
    [1, 4, 7],
    [2, 5, 8], 
    [3, 6, 9]
]
merged = merge_k_sorted_arrays(arrays)
print(f"Merged arrays: {merged}")

# Smallest range covering k lists
nums = [[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]
smallest_range = smallest_range_covering_k_lists(nums)
print(f"Smallest range: {smallest_range}")

# Kth smallest in multiple arrays
arrays = [[1, 3, 5], [2, 4, 6], [0, 8, 9]]
k = 5
kth_smallest = kth_smallest_in_m_sorted_arrays(arrays, k)
print(f"{k}th smallest across arrays: {kth_smallest}")

# Merge interval lists
interval_lists = [
    [[1, 3], [5, 7]],
    [[2, 4], [6, 8]],
    [[9, 12]]
]
merged_intervals = merge_intervals_from_k_lists(interval_lists)
print(f"Merged intervals: {merged_intervals}")

# K pairs with smallest sum from multiple arrays
arrays = [[1, 2], [3, 4], [5, 6]]
k = 3
k_pairs = find_k_pairs_smallest_sum_multiple_arrays(arrays, k)
print(f"{k} pairs with smallest sum: {k_pairs}")

# Custom condition merge (example: pick maximum element)
def pick_maximum(elements):
    """Condition function to always pick maximum element."""
    return elements.index(max(elements))

arrays = [[1, 5, 9], [2, 6, 10], [3, 7, 11]]
custom_merged = k_way_merge_with_condition(arrays, pick_maximum)
print(f"Merge picking maximum: {custom_merged}")



# Part VII: Advanced Data Structure Patterns

## 21. Trie (Prefix Tree) Pattern

**When to use:** String prefix matching, autocomplete systems, spell checkers, or when you need to efficiently store and query strings with common prefixes.

**Key insight:** Trie compresses common prefixes into shared paths. Each node represents a character, and paths from root to nodes represent prefixes. This enables efficient prefix-based operations.

**Problem types:** Word search, autocomplete, longest common prefix, word break problems.

```python
class TrieNode:
    """Node in a Trie data structure."""
    def __init__(self):
        self.children = {}  # Dictionary mapping character to TrieNode
        self.is_end_word = False  # True if this node marks end of a word
        self.word_count = 0  # Number of words ending at this node

class Trie:
    """
    Trie (Prefix Tree) implementation for efficient string operations.
    
    Core operations:
    - Insert: O(m) where m is word length
    - Search: O(m) where m is word length  
    - StartsWith: O(m) where m is prefix length
    """
    
    def __init__(self):
        """Initialize trie with empty root node."""
        self.root = TrieNode()
        self.total_words = 0
    
    def insert(self, word):
        """
        Insert word into trie.
        
        Traverse character by character, creating nodes as needed.
        Mark final node as end of word.
        
        Time: O(m), Space: O(m) in worst case
        """
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_end_word:  # New word
            node.is_end_word = True
            self.total_words += 1
        
        node.word_count += 1
    
    def search(self, word):
        """
        Search if word exists in trie.
        
        Traverse path corresponding to word characters.
        Word exists if we can traverse completely and end node marks word end.
        
        Time: O(m), Space: O(1)
        """
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end_word
    
    def starts_with(self, prefix):
        """
        Check if any word starts with given prefix.
        
        Similar to search, but don't need to check is_end_word.
        
        Time: O(m), Space: O(1)
        """
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return True
    
    def get_words_with_prefix(self, prefix):
        """
        Get all words that start with given prefix.
        
        First navigate to prefix node, then DFS to collect all words.
        
        Time: O(p + n) where p is prefix length, n is result size
        Space: O(n)
        """
        node = self.root
        
        # Navigate to prefix node
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all words from this node using DFS
        words = []
        
        def dfs(current_node, current_prefix):
            if current_node.is_end_word:
                words.append(current_prefix)
            
            for char, child_node in current_node.children.items():
                dfs(child_node, current_prefix + char)
        
        dfs(node, prefix)
        return words
    
    def delete(self, word):
        """
        Delete word from trie.
        
        Mark word as not ending, remove nodes if they become unnecessary.
        
        Time: O(m), Space: O(m) due to recursion
        """
        def delete_helper(node, word, index):
            if index == len(word):
                # Reached end of word
                if not node.is_end_word:
                    return False  # Word doesn't exist
                
                node.is_end_word = False
                node.word_count = 0
                
                # Delete node if it has no children and is not end of another word
                return len(node.children) == 0
            
            char = word[index]
            child_node = node.children.get(char)
            
            if not child_node:
                return False  # Word doesn't exist
            
            should_delete_child = delete_helper(child_node, word, index + 1)
            
            if should_delete_child:
                del node.children[char]
                
                # Delete current node if it's not end of word and has no children
                return not node.is_end_word and len(node.children) == 0
            
            return False
        
        if self.search(word):
            delete_helper(self.root, word, 0)
            self.total_words -= 1
            return True
        return False

def word_search_trie(board, words):
    """
    Find all words from list that exist in 2D character board.
    
    Build trie from word list, then DFS on board using trie for guidance.
    Trie pruning makes this much faster than searching each word individually.
    
    Time: O(m×n×4^l + w×l) where m×n is board, l is max word length, w is word count
    Space: O(w×l) for trie
    """
    if not board or not board[0] or not words:
        return []
    
    # Build trie from word list
    trie = Trie()
    for word in words:
        trie.insert(word)
    
    rows, cols = len(board), len(board[0])
    result = set()  # Use set to avoid duplicates
    
    def dfs(row, col, node, current_word):
        # Check bounds and visited status
        if (row < 0 or row >= rows or col < 0 or col >= cols or
            board[row][col] == '#'):  # '#' marks visited
            return
        
        char = board[row][col]
        if char not in node.children:
            return
        
        # Move to next trie node
        node = node.children[char]
        current_word += char
        
        # Check if we found a complete word
        if node.is_end_word:
            result.add(current_word)
        
        # Mark current cell as visited
        board[row][col] = '#'
        
        # Explore all 4 directions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, node, current_word)
        
        # Restore cell (backtrack)
        board[row][col] = char
    
    # Try starting from each cell
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, trie.root, "")
    
    return list(result)

def longest_word_in_dictionary(words):
    """
    Find longest word that can be built one character at a time.
    
    Insert all words into trie. A word can be built if all its prefixes exist.
    Use DFS to find longest such word.
    
    Time: O(sum of word lengths), Space: O(sum of word lengths)
    """
    trie = Trie()
    
    # Insert all words into trie
    for word in words:
        trie.insert(word)
    
    def dfs(node, current_word):
        """Find longest word that can be built character by character."""
        longest = current_word if node.is_end_word else ""
        
        for char, child_node in node.children.items():
            # Can only continue if child forms a complete word
            if child_node.is_end_word:
                candidate = dfs(child_node, current_word + char)
                if len(candidate) > len(longest) or (len(candidate) == len(longest) and candidate < longest):
                    longest = candidate
        
        return longest
    
    return dfs(trie.root, "")

def word_squares(words):
    """
    Find all valid word squares from given words.
    A word square is a sequence of words where kth row = kth column.
    
    Use trie for efficient prefix matching during backtracking.
    
    Time: O(N×26^L×L) worst case, Space: O(N×L)
    """
    if not words:
        return []
    
    word_len = len(words[0])
    trie = Trie()
    
    # Build trie from all words
    for word in words:
        trie.insert(word)
    
    def get_words_with_prefix_optimized(prefix):
        """Get words with prefix using trie traversal."""
        node = trie.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect words from this node
        result = []
        
        def collect_words(current_node, current_prefix):
            if current_node.is_end_word:
                result.append(current_prefix)
            for char, child in current_node.children.items():
                collect_words(child, current_prefix + char)
        
        collect_words(node, prefix)
        return result
    
    def backtrack(square):
        """Build word square using backtracking."""
        if len(square) == word_len:
            return [square[:]]  # Found complete square
        
        results = []
        row = len(square)
        
        # Build prefix for next word based on current square
        prefix = ""
        for col in range(row):
            prefix += square[col][row]
        
        # Get all words with this prefix
        candidates = get_words_with_prefix_optimized(prefix)
        
        for word in candidates:
            # Check if word is compatible with all existing constraints
            valid = True
            for col in range(row + 1, word_len):
                column_prefix = ""
                for existing_row in range(row):
                    column_prefix += square[existing_row][col]
                column_prefix += word[col]
                
                if not trie.starts_with(column_prefix):
                    valid = False
                    break
            
            if valid:
                square.append(word)
                results.extend(backtrack(square))
                square.pop()
        
        return results
    
    all_squares = []
    for word in words:
        all_squares.extend(backtrack([word]))
    
    return all_squares

def replace_words_with_roots(dictionary, sentence):
    """
    Replace words in sentence with their root words from dictionary.
    
    Build trie from dictionary roots. For each word in sentence,
    find shortest matching root.
    
    Time: O(d + s) where d is dictionary size, s is sentence length
    Space: O(d)
    """
    trie = Trie()
    
    # Insert all roots into trie
    for root in dictionary:
        trie.insert(root)
    
    def find_root(word):
        """Find shortest root that matches beginning of word."""
        node = trie.root
        root = ""
        
        for char in word:
            if char not in node.children:
                break
            
            root += char
            node = node.children[char]
            
            # Return immediately when we find a root
            if node.is_end_word:
                return root
        
        return word  # No root found, return original word
    
    words = sentence.split()
    result = []
    
    for word in words:
        result.append(find_root(word))
    
    return " ".join(result)

def stream_autocomplete_system():
    """
    Design autocomplete system for search queries.
    
    Support:
    - input(c): Input character c
    - Return top 3 historical hot sentences with same prefix
    
    Time: O(p + n log n) for each input, Space: O(ALPHABET_SIZE × N × M)
    """
    class AutocompleteSystem:
        def __init__(self, sentences, times):
            self.trie = Trie()
            self.current_input = ""
            
            # Build trie with sentence frequencies
            for i, sentence in enumerate(sentences):
                for _ in range(times[i]):
                    self.trie.insert(sentence)
        
        def input(self, c):
            if c == '#':
                # End of input, save sentence
                if self.current_input:
                    self.trie.insert(self.current_input)
                self.current_input = ""
                return []
            else:
                # Add character to current input
                self.current_input += c
                
                # Get all sentences with current prefix
                suggestions = self.trie.get_words_with_prefix(self.current_input)
                
                # Sort by frequency (count) then lexicographically
                # Get frequency for each suggestion
                suggestion_counts = []
                for suggestion in suggestions:
                    # Navigate to end of suggestion to get count
                    node = self.trie.root
                    for char in suggestion:
                        node = node.children[char]
                    suggestion_counts.append((suggestion, node.word_count))
                
                # Sort by count (desc) then alphabetically (asc)
                suggestion_counts.sort(key=lambda x: (-x[1], x[0]))
                
                # Return top 3
                return [s for s, _ in suggestion_counts[:3]]
    
    return AutocompleteSystem

# Example usage and comprehensive testing
print("=== Trie Examples ===")

# Basic trie operations
trie = Trie()
words = ["apple", "app", "application", "apply", "appreciate"]

for word in words:
    trie.insert(word)

print(f"Search 'app': {trie.search('app')}")  # True
print(f"Search 'appl': {trie.search('appl')}")  # False
print(f"Starts with 'app': {trie.starts_with('app')}")  # True
print(f"Words with prefix 'app': {trie.get_words_with_prefix('app')}")

# Word search in board
board = [
    ['o','a','a','n'],
    ['e','t','a','e'],
    ['i','h','k','r'],
    ['i','f','l','v']
]
words = ["oath","pea","eat","rain"]
found_words = word_search_trie(board, words)
print(f"Words found in board: {found_words}")

# Longest word in dictionary
words = ["w","wo","wor","worl","world"]
longest = longest_word_in_dictionary(words)
print(f"Longest word that can be built: '{longest}'")

# Replace words with roots
dictionary = ["cat", "bat", "rat"]
sentence = "the cattle was rattled by the battery"
replaced = replace_words_with_roots(dictionary, sentence)
print(f"Sentence with roots: '{replaced}'")



## 22. Monotonic Stack Pattern

**When to use:** Finding next/previous greater or smaller elements, histogram problems, or maintaining elements in monotonic (increasing/decreasing) order while processing sequentially.

**Key insight:** Maintain a stack where elements are in monotonic order. When a new element violates this order, pop elements until order is restored. This efficiently finds relationships between elements.

**Problem types:** Next greater element, largest rectangle in histogram, trapping rainwater, sliding window maximum.

```python
def next_greater_elements(nums):
    """
    Find next greater element for each element in array.
    
    Use decreasing monotonic stack. When we find larger element,
    it's the next greater element for all smaller elements in stack.
    
    Time: O(n), Space: O(n)
    """
    result = [-1] * len(nums)
    stack = []  # Store indices
    
    for i, num in enumerate(nums):
        # While stack not empty and current element is greater
        while stack and nums[stack[-1]] < num:
            prev_index = stack.pop()
            result[prev_index] = num
        
        stack.append(i)
    
    return result

def next_greater_elements_circular(nums):
    """
    Find next greater element in circular array.
    
    Process array twice to handle circular nature.
    Use same monotonic stack approach.
    
    Time: O(n), Space: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []
    
    # Process array twice for circular behavior
    for i in range(2 * n):
        current_num = nums[i % n]
        
        # Pop elements smaller than current
        while stack and nums[stack[-1]] < current_num:
            prev_index = stack.pop()
            result[prev_index] = current_num
        
        # Only add indices from first iteration
        if i < n:
            stack.append(i)
    
    return result

def largest_rectangle_in_histogram(heights):
    """
    Find area of largest rectangle in histogram.
    
    Use increasing monotonic stack. When we encounter smaller height,
    calculate rectangles using previously stored heights.
    
    Time: O(n), Space: O(n)
    """
    stack = []  # Store indices
    max_area = 0
    
    for i, height in enumerate(heights):
        # While stack not empty and current height is smaller
        while stack and heights[stack[-1]] > height:
            h = heights[stack.pop()]
            
            # Width is distance between current index and previous index in stack
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, h * width)
        
        stack.append(i)
    
    # Process remaining elements in stack
    while stack:
        h = heights[stack.pop()]
        width = len(heights) if not stack else len(heights) - stack[-1] - 1
        max_area = max(max_area, h * width)
    
    return max_area

def trapping_rainwater(heights):
    """
    Calculate trapped rainwater between elevation heights.
    
    Use monotonic stack to find areas where water can be trapped
    between higher bars on left and right.
    
    Time: O(n), Space: O(n)
    """
    if not heights:
        return 0
    
    stack = []  # Store indices
    water_trapped = 0
    
    for i, height in enumerate(heights):
        # While we can form a container
        while stack and heights[stack[-1]] < height:
            bottom_height = heights[stack.pop()]
            
            if not stack:  # No left boundary
                break
            
            # Calculate trapped water
            width = i - stack[-1] - 1
            bounded_height = min(heights[stack[-1]], height) - bottom_height
            water_trapped += width * bounded_height
        
        stack.append(i)
    
    return water_trapped

def sliding_window_maximum_monotonic(nums, k):
    """
    Find maximum in each sliding window using monotonic deque.
    
    Maintain decreasing monotonic deque. Front always has window maximum.
    
    Time: O(n), Space: O(k)
    """
    from collections import deque
    
    if not nums or k == 0:
        return []
    
    dq = deque()  # Store indices
    result = []
    
    for i, num in enumerate(nums):
        # Remove elements outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove elements smaller than current (maintain decreasing order)
        while dq and nums[dq[-1]] < num:
            dq.pop()
        
        dq.append(i)
        
        # Add maximum to result when window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

def daily_temperatures(temperatures):
    """
    Find how many days until warmer temperature.
    
    Classic monotonic stack problem. For each day, find next day
    with higher temperature.
    
    Time: O(n), Space: O(n)
    """
    result = [0] * len(temperatures)
    stack = []  # Store indices
    
    for i, temp in enumerate(temperatures):
        # While stack not empty and current temp is higher
        while stack and temperatures[stack[-1]] < temp:
            prev_day = stack.pop()
            result[prev_day] = i - prev_day
        
        stack.append(i)
    
    return result

def remove_k_digits_monotonic(num, k):
    """
    Remove k digits to make smallest number using monotonic stack.
    
    Maintain increasing stack. Remove digits that are larger than
    the next digit to minimize the result.
    
    Time: O(n), Space: O(n)
    """
    stack = []
    removals = k
    
    for digit in num:
        # Remove larger digits while we have removals left
        while removals > 0 and stack and stack[-1] > digit:
            stack.pop()
            removals -= 1
        
        stack.append(digit)
    
    # Remove remaining digits from end if needed
    while removals > 0:
        stack.pop()
        removals -= 1
    
    # Convert to number, handle leading zeros
    result = ''.join(stack).lstrip('0')
    return result if result else '0'

def valid_parentheses_stack(s):
    """
    Check if parentheses string is valid using stack.
    
    Not strictly monotonic, but uses stack pattern for matching.
    
    Time: O(n), Space: O(n)
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:  # Closing bracket
            if not stack or stack.pop() != mapping[char]:
                return False
        else:  # Opening bracket
            stack.append(char)
    
    return not stack  # Valid if stack is empty

def maximum_width_ramp(nums):
    """
    Find maximum width ramp where i < j and nums[i] <= nums[j].
    
    Use decreasing monotonic stack to find potential left boundaries,
    then scan from right to find maximum width.
    
    Time: O(n), Space: O(n)
    """
    stack = []
    n = len(nums)
    
    # Build decreasing monotonic stack of indices
    for i in range(n):
        if not stack or nums[stack[-1]] > nums[i]:
            stack.append(i)
    
    max_width = 0
    
    # Scan from right, find maximum width for each stack element
    for j in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] <= nums[j]:
            i = stack.pop()
            max_width = max(max_width, j - i)
    
    return max_width

def stock_spanner():
    """
    Design stock spanner to calculate price spans.
    Price span = number of consecutive days (including today) 
    where price <= today's price.
    
    Use monotonic stack to track previous higher prices.
    
    Time: O(1) amortized per call, Space: O(n)
    """
    class StockSpanner:
        def __init__(self):
            self.stack = []  # (price, span)
        
        def next(self, price):
            span = 1
            
            # Add spans of all previous lower prices
            while self.stack and self.stack[-1][0] <= price:
                prev_price, prev_span = self.stack.pop()
                span += prev_span
            
            self.stack.append((price, span))
            return span
    
    return StockSpanner()

# Example usage and comprehensive testing
print("=== Monotonic Stack Examples ===")

# Next greater elements
nums = [2, 1, 2, 4, 3, 1]
next_greater = next_greater_elements(nums)
print(f"Next greater elements: {next_greater}")

# Next greater in circular array
nums = [1, 2, 1]
next_greater_circ = next_greater_elements_circular(nums)
print(f"Next greater (circular): {next_greater_circ}")

# Largest rectangle in histogram
heights = [2, 1, 5, 6, 2, 3]
max_rectangle = largest_rectangle_in_histogram(heights)
print(f"Largest rectangle area: {max_rectangle}")

# Trapping rainwater
heights = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
trapped_water = trapping_rainwater(heights)
print(f"Trapped water: {trapped_water}")

# Daily temperatures
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
days_to_warmer = daily_temperatures(temperatures)
print(f"Days to warmer temperature: {days_to_warmer}")

# Stock spanner
spanner = stock_spanner()
prices = [100, 80, 60, 70, 60, 75, 85]
spans = [spanner.next(price) for price in prices]
print(f"Stock price spans: {spans}")



## 23. Heap Patterns

**When to use:** When you need to repeatedly access minimum or maximum elements, maintain a dynamic set of elements with priority, or solve optimization problems with changing priorities.

**Key insight:** Heaps provide O(log n) insertion/deletion and O(1) access to min/max element. They're perfect for priority queues and problems requiring dynamic ordering.

**Problem types:** Priority scheduling, merge sorted sequences, median maintenance, k-th element problems.

```python
import heapq

class MinHeap:
    """
    Min-heap implementation with additional utilities.
    
    Python's heapq provides min-heap by default.
    For max-heap, negate values or use custom comparison.
    """
    
    def __init__(self):
        self.heap = []
    
    def push(self, val):
        """Insert element into heap. Time: O(log n)"""
        heapq.heappush(self.heap, val)
    
    def pop(self):
        """Remove and return minimum element. Time: O(log n)"""
        if not self.heap:
            raise IndexError("pop from empty heap")
        return heapq.heappop(self.heap)
    
    def peek(self):
        """Get minimum element without removing. Time: O(1)"""
        if not self.heap:
            raise IndexError("peek from empty heap")
        return self.heap[0]
    
    def size(self):
        """Get number of elements. Time: O(1)"""
        return len(self.heap)
    
    def is_empty(self):
        """Check if heap is empty. Time: O(1)"""
        return len(self.heap) == 0

class MaxHeap:
    """Max-heap implementation using negated values."""
    
    def __init__(self):
        self.heap = []
    
    def push(self, val):
        """Insert element. Time: O(log n)"""
        heapq.heappush(self.heap, -val)
    
    def pop(self):
        """Remove and return maximum element. Time: O(log n)"""
        if not self.heap:
            raise IndexError("pop from empty heap")
        return -heapq.heappop(self.heap)
    
    def peek(self):
        """Get maximum element. Time: O(1)"""
        if not self.heap:
            raise IndexError("peek from empty heap")
        return -self.heap[0]
    
    def size(self):
        return len(self.heap)
    
    def is_empty(self):
        return len(self.heap) == 0

def merge_k_sorted_arrays_heap(arrays):
    """
    Merge k sorted arrays using min-heap.
    
    Alternative to k-way merge pattern using heap directly.
    
    Time: O(n log k), Space: O(k)
    """
    if not arrays:
        return []
    
    min_heap = []
    result = []
    
    # Initialize heap with first element from each array
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(min_heap, (arr[0], i, 0))  # (value, array_idx, element_idx)
    
    while min_heap:
        val, array_idx, element_idx = heapq.heappop(min_heap)
        result.append(val)
        
        # Add next element from same array
        if element_idx + 1 < len(arrays[array_idx]):
            next_val = arrays[array_idx][element_idx + 1]
            heapq.heappush(min_heap, (next_val, array_idx, element_idx + 1))
    
    return result

def task_scheduler_with_cooldown(tasks, n):
    """
    Schedule tasks with cooldown period between same tasks.
    
    Use max-heap to always schedule most frequent remaining task.
    Use queue to track tasks in cooldown.
    
    Time: O(m log k) where m is total tasks, k is unique tasks
    Space: O(k)
    """
    from collections import Counter, deque
    
    if not tasks:
        return 0
    
    # Count task frequencies
    task_counts = Counter(tasks)
    
    # Max-heap of task frequencies
    max_heap = [-count for count in task_counts.values()]
    heapq.heapify(max_heap)
    
    # Queue to track tasks in cooldown: (frequency, time_available)
    cooldown_queue = deque()
    time = 0
    
    while max_heap or cooldown_queue:
        time += 1
        
        # Check if any task is ready from cooldown
        if cooldown_queue and cooldown_queue[0][1] <= time:
            frequency = cooldown_queue.popleft()[0]
            heapq.heappush(max_heap, frequency)
        
        # Schedule highest frequency task if available
        if max_heap:
            current_freq = heapq.heappop(max_heap)
            
            # If task still has remaining executions, add to cooldown
            if current_freq < -1:  # -1 means 1 execution left, so < -1 means > 1 left
                cooldown_queue.append((current_freq + 1, time + n + 1))
    
    return time

def ugly_numbers_heap(n):
    """
    Find the nth ugly number (only factors 2, 3, 5).
    
    Use min-heap to generate ugly numbers in order.
    
    Time: O(n log n), Space: O(n)
    """
    if n <= 0:
        return 0
    
    min_heap = [1]
    seen = {1}
    
    for _ in range(n):
        current = heapq.heappop(min_heap)
        
        # Generate next ugly numbers
        for factor in [2, 3, 5]:
            new_ugly = current * factor
            if new_ugly not in seen:
                seen.add(new_ugly)
                heapq.heappush(min_heap, new_ugly)
    
    return current

def super_ugly_numbers_heap(n, primes):
    """
    Find nth super ugly number (only given prime factors).
    
    Generalization of ugly numbers with custom prime factors.
    
    Time: O(n × p × log(n × p)), Space: O(n × p)
    """
    if n <= 0:
        return 0
    
    min_heap = [1]
    seen = {1}
    
    for _ in range(n):
        current = heapq.heappop(min_heap)
        
        # Generate next numbers using all prime factors
        for prime in primes:
            new_number = current * prime
            if new_number not in seen:
                seen.add(new_number)
                heapq.heappush(min_heap, new_number)
    
    return current

def meeting_rooms_ii_heap(intervals):
    """
    Find minimum meeting rooms needed using heap.
    
    Sort by start time, use min-heap to track meeting end times.
    
    Time: O(n log n), Space: O(n)
    """
    if not intervals:
        return 0
    
    # Sort meetings by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min-heap to track meeting end times
    end_times = []
    
    for start, end in intervals:
        # If earliest meeting has ended, reuse room
        if end_times and end_times[0] <= start:
            heapq.heappop(end_times)
        
        # Add current meeting's end time
        heapq.heappush(end_times, end)
    
    return len(end_times)

def ipo_maximize_capital(k, w, profits, capital):
    """
    Maximize capital after k projects.
    
    Use two heaps: min-heap for available projects by capital,
    max-heap for available projects by profit.
    
    Time: O(n log n + k log n), Space: O(n)
    """
    if not profits or not capital:
        return w
    
    # Min-heap of projects by capital requirement
    min_capital_heap = [(c, p) for c, p in zip(capital, profits)]
    heapq.heapify(min_capital_heap)
    
    # Max-heap of available projects by profit
    max_profit_heap = []
    
    current_capital = w
    
    for _ in range(k):
        # Move all affordable projects to profit heap
        while min_capital_heap and min_capital_heap[0][0] <= current_capital:
            cap, prof = heapq.heappop(min_capital_heap)
            heapq.heappush(max_profit_heap, -prof)  # Negate for max-heap
        
        # If no projects available, break
        if not max_profit_heap:
            break
        
        # Take most profitable project
        max_profit = -heapq.heappop(max_profit_heap)
        current_capital += max_profit
    
    return current_capital

def find_k_closest_elements_heap(arr, k, x):
    """
    Find k closest elements to x in sorted array.
    
    Use max-heap to maintain k closest elements.
    
    Time: O(n log k), Space: O(k)
    """
    max_heap = []
    
    for num in arr:
        distance = abs(num - x)
        
        if len(max_heap) < k:
            heapq.heappush(max_heap, (-distance, -num))  # Max-heap by distance
        elif distance < -max_heap[0][0]:
            heapq.heapreplace(max_heap, (-distance, -num))
    
    # Extract elements and sort
    result = [-num for _, num in max_heap]
    return sorted(result)

class FrequencyTracker:
    """
    Track frequency of elements with efficient queries.
    
    Maintain heaps for frequencies and handle lazy deletion.
    """
    
    def __init__(self):
        self.freq_map = {}
        self.max_freq_heap = []  # (-frequency, element)
        self.min_freq_heap = []  # (frequency, element)
    
    def add(self, element):
        """Add element and update frequency. Time: O(log n)"""
        old_freq = self.freq_map.get(element, 0)
        new_freq = old_freq + 1
        self.freq_map[element] = new_freq
        
        # Add to both heaps
        heapq.heappush(self.max_freq_heap, (-new_freq, element))
        heapq.heappush(self.min_freq_heap, (new_freq, element))
    
    def get_max_frequency_element(self):
        """Get element with maximum frequency. Time: O(log n)"""
        # Clean up stale entries
        while (self.max_freq_heap and 
               -self.max_freq_heap[0][0] != self.freq_map.get(self.max_freq_heap[0][1], 0)):
            heapq.heappop(self.max_freq_heap)
        
        if not self.max_freq_heap:
            return None
        
        return self.max_freq_heap[0][1]
    
    def get_min_frequency_element(self):
        """Get element with minimum frequency. Time: O(log n)"""
        # Clean up stale entries
        while (self.min_freq_heap and 
               self.min_freq_heap[0][0] != self.freq_map.get(self.min_freq_heap[0][1], 0)):
            heapq.heappop(self.min_freq_heap)
        
        if not self.min_freq_heap:
            return None
        
        return self.min_freq_heap[0][1]

# Example usage and comprehensive testing
print("=== Heap Examples ===")

# Basic heap operations
min_heap = MinHeap()
max_heap = MaxHeap()

for val in [3, 1, 4, 1, 5, 9, 2, 6]:
    min_heap.push(val)
    max_heap.push(val)

print(f"Min heap peek: {min_heap.peek()}")  # 1
print(f"Max heap peek: {max_heap.peek()}")  # 9

# Merge k sorted arrays
arrays = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
merged = merge_k_sorted_arrays_heap(arrays)
print(f"Merged arrays: {merged}")

# Task scheduler
tasks = ['A', 'A', 'A', 'B', 'B', 'B']
n = 2
min_time = task_scheduler_with_cooldown(tasks, n)
print(f"Minimum time for tasks: {min_time}")

# Ugly numbers
n = 10
ugly_num = ugly_numbers_heap(n)
print(f"{n}th ugly number: {ugly_num}")

# Meeting rooms
intervals = [[0, 30], [5, 10], [15, 20]]
min_rooms = meeting_rooms_ii_heap(intervals)
print(f"Minimum meeting rooms: {min_rooms}")

# IPO capital maximization
k, w = 2, 0
profits = [1, 2, 3]
capital = [0, 1, 1]
max_capital = ipo_maximize_capital(k, w, profits, capital)
print(f"Maximum capital after {k} projects: {max_capital}")

# Frequency tracker
tracker = FrequencyTracker()
for element in [1, 1, 2, 2, 2, 3]:
    tracker.add(element)

print(f"Max frequency element: {tracker.get_max_frequency_element()}")  # 2
print(f"Min frequency element: {tracker.get_min_frequency_element()}")  # 3



## 24. Two Heaps Pattern

**When to use:** Finding median in data stream, balancing two sets of data, or when you need to maintain balance between smallest large elements and largest small elements.

**Key insight:** Use two heaps to divide data into two halves. Max-heap stores smaller half, min-heap stores larger half. Keep them balanced for O(1) median access.

**Problem types:** Median maintenance, sliding window median, IPO problems, balancing workloads.

```python
import heapq

class MedianFinder:
    """
    Data structure to find median from data stream.
    
    Use two heaps:
    - Max-heap (small) for smaller half of numbers
    - Min-heap (large) for larger half of numbers
    
    Keep heaps balanced: sizes differ by at most 1
    """
    
    def __init__(self):
        self.small = []  # Max-heap (negative values)
        self.large = []  # Min-heap
    
    def add_number(self, num):
        """
        Add number to data structure.
        
        Strategy: Add to appropriate heap, then rebalance if needed.
        
        Time: O(log n), Space: O(1)
        """
        # Decide which heap to add to
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num)
        else:
            heapq.heappush(self.large, num)
        
        # Rebalance heaps
        self._rebalance()
    
    def find_median(self):
        """
        Find median of all numbers added so far.
        
        Time: O(1), Space: O(1)
        """
        if len(self.small) == len(self.large):
            if not self.small:
                raise ValueError("No numbers added")
            return (-self.small[0] + self.large[0]) / 2.0
        elif len(self.small) > len(self.large):
            return -self.small[0]
        else:
            return self.large[0]
    
    def _rebalance(self):
        """Ensure heap size difference is at most 1."""
        if len(self.small) > len(self.large) + 1:
            # Move from small to large
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            # Move from large to small
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

def sliding_window_median(nums, k):
    """
    Find median of each sliding window of size k.
    
    Use two heaps with lazy deletion to handle sliding window.
    
    Time: O(n log k), Space: O(k)
    """
    from collections import defaultdict
    
    def rebalance(small, large, small_size, large_size):
        """Rebalance heaps considering logical sizes."""
        if small_size > large_size + 1:
            # Move from small to large
            val = -heapq.heappop(small)
            heapq.heappush(large, val)
            small_size -= 1
            large_size += 1
        elif large_size > small_size + 1:
            # Move from large to small
            val = heapq.heappop(large)
            heapq.heappush(small, -val)
            small_size += 1
            large_size -= 1
        
        return small_size, large_size
    
    def clean_heap(heap, removed_count, is_max_heap=False):
        """Remove elements that are marked for deletion."""
        while heap and removed_count[heap[0] if not is_max_heap else -heap[0]] > 0:
            val = heapq.heappop(heap)
            actual_val = val if not is_max_heap else -val
            removed_count[actual_val] -= 1
    
    if k == 1:
        return nums
    
    small = []  # Max-heap
    large = []  # Min-heap
    removed_count = defaultdict(int)  # Track removed elements
    result = []
    
    small_size = 0
    large_size = 0
    
    # Process first k elements
    for i in range(k):
        if not small or nums[i] <= -small[0]:
            heapq.heappush(small, -nums[i])
            small_size += 1
        else:
            heapq.heappush(large, nums[i])
            large_size += 1
        
        small_size, large_size = rebalance(small, large, small_size, large_size)
    
    # Get first median
    if small_size == large_size:
        result.append((-small[0] + large[0]) / 2.0)
    elif small_size > large_size:
        result.append(-small[0])
    else:
        result.append(large[0])
    
    # Process remaining elements
    for i in range(k, len(nums)):
        # Remove element going out of window
        out_val = nums[i - k]
        removed_count[out_val] += 1
        
        if out_val <= -small[0]:
            small_size -= 1
        else:
            large_size -= 1
        
        # Add new element
        in_val = nums[i]
        if not small or in_val <= -small[0]:
            heapq.heappush(small, -in_val)
            small_size += 1
        else:
            heapq.heappush(large, in_val)
            large_size += 1
        
        # Rebalance
        small_size, large_size = rebalance(small, large, small_size, large_size)
        
        # Clean heaps
        clean_heap(small, removed_count, is_max_heap=True)
        clean_heap(large, removed_count, is_max_heap=False)
        
        # Calculate median
        if small_size == large_size:
            result.append((-small[0] + large[0]) / 2.0)
        elif small_size > large_size:
            result.append(-small[0])
        else:
            result.append(large[0])
    
    return result

def ipo_problem_two_heaps(k, w, profits, capital):
    """
    IPO: Maximize capital after at most k distinct projects.
    
    Use two heaps: one for affordable projects (by profit),
    one for unaffordable projects (by capital requirement).
    
    Time: O(n log n), Space: O(n)
    """
    import heapq
    
    # Create list of (capital, profit) pairs
    projects = list(zip(capital, profits))
    projects.sort()  # Sort by capital requirement
    
    affordable_heap = []  # Max-heap by profit
    project_index = 0
    current_capital = w
    
    for _ in range(k):
        # Move all newly affordable projects to profit heap
        while project_index < len(projects) and projects[project_index][0] <= current_capital:
            cap, prof = projects[project_index]
            heapq.heappush(affordable_heap, -prof)  # Max-heap
            project_index += 1
        
        # If no projects are affordable, break
        if not affordable_heap:
            break
        
        # Take most profitable project
        max_profit = -heapq.heappop(affordable_heap)
        current_capital += max_profit
    
    return current_capital

class BalancedDataStream:
    """
    Maintain balanced data stream for various statistics.
    
    Supports finding median, kth smallest/largest elements.
    """
    
    def __init__(self):
        self.small = []  # Max-heap for smaller half
        self.large = []  # Min-heap for larger half
        self.size = 0
    
    def add_number(self, num):
        """Add number while maintaining balance."""
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num)
        else:
            heapq.heappush(self.large, num)
        
        self.size += 1
        self._rebalance()
    
    def remove_number(self, num):
        """Remove specific number (lazy deletion)."""
        # This is complex with heaps, typically use multiset or segment tree
        # For simplicity, we'll mark as removed and clean later
        pass
    
    def find_median(self):
        """Find current median."""
        if len(self.small) == len(self.large):
            return (-self.small[0] + self.large[0]) / 2.0
        elif len(self.small) > len(self.large):
            return -self.small[0]
        else:
            return self.large[0]
    
    def find_kth_smallest(self, k):
        """Find kth smallest element (1-indexed)."""
        if k <= len(self.small):
            # kth smallest is in small heap
            temp_heap = [-x for x in self.small]
            heapq.heapify(temp_heap)
            
            for _ in range(k - 1):
                heapq.heappop(temp_heap)
            
            return temp_heap[0]
        else:
            # kth smallest is in large heap
            target_in_large = k - len(self.small)
            temp_heap = self.large[:]
            
            for _ in range(target_in_large - 1):
                heapq.heappop(temp_heap)
            
            return temp_heap[0]
    
    def _rebalance(self):
        """Maintain heap balance."""
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

def maximize_minimum_pair_sum(nums):
    """
    Maximize the minimum sum among all pairs.
    
    Strategy: Sort array, pair smallest with largest iteratively.
    Use two pointers approach (not strictly two heaps, but similar concept).
    
    Time: O(n log n), Space: O(1)
    """
    nums.sort()
    n = len(nums)
    min_pair_sum = float('inf')
    
    left, right = 0, n - 1
    
    while left < right:
        pair_sum = nums[left] + nums[right]
        min_pair_sum = min(min_pair_sum, pair_sum)
        left += 1
        right -= 1
    
    return min_pair_sum

def find_right_interval(intervals):
    """
    Find right interval for each interval.
    Right interval has smallest start >= current interval's end.
    
    Use two heaps to efficiently find next intervals.
    
    Time: O(n log n), Space: O(n)
    """
    import heapq
    
    # Create list of (start, index) and (end, index)
    starts = [(interval[0], i) for i, interval in enumerate(intervals)]
    starts.sort()
    
    result = [-1] * len(intervals)
    start_heap = [(start, idx) for start, idx in starts]
    
    # Process intervals by end time
    ends = [(intervals[i][1], i) for i in range(len(intervals))]
    ends.sort()
    
    start_idx = 0
    
    for end_time, interval_idx in ends:
        # Find the smallest start time >= end_time
        while start_idx < len(starts) and starts[start_idx][0] < end_time:
            start_idx += 1
        
        if start_idx < len(starts):
            result[interval_idx] = starts[start_idx][1]
    
    return result

# Example usage and comprehensive testing
print("=== Two Heaps Examples ===")

# Median finder
median_finder = MedianFinder()
numbers = [1, 2, 3, 4, 5]

for num in numbers:
    median_finder.add_number(num)
    print(f"Added {num}, median: {median_finder.find_median()}")

# Sliding window median
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
window_medians = sliding_window_median(nums, k)
print(f"Sliding window medians (k={k}): {window_medians}")

# IPO problem
k, w = 2, 0
profits = [1, 2, 3]
capital = [0, 1, 1]
max_capital = ipo_problem_two_heaps(k, w, profits, capital)
print(f"IPO max capital: {max_capital}")

# Balanced data stream
stream = BalancedDataStream()
for num in [5, 15, 1, 3, 9, 8, 7]:
    stream.add_number(num)

print(f"Stream median: {stream.find_median()}")
print(f"3rd smallest: {stream.find_kth_smallest(3)}")

# Maximize minimum pair sum
nums = [3, 5, 2, 4]
min_pair_sum = maximize_minimum_pair_sum(nums)
print(f"Maximum minimum pair sum: {min_pair_sum}")



# Part VIII: Mathematical & Bitwise Patterns

## 25. Bitwise XOR Pattern

**When to use:** Problems involving finding unique elements, detecting differences, or when mathematical properties of XOR can simplify solutions. XOR has unique properties: a ⊕ a = 0, a ⊕ 0 = a, and is commutative/associative.

**Key insight:** XOR has special properties that make certain problems elegant. It's self-canceling (a ⊕ a = 0), identity-preserving (a ⊕ 0 = a), and can detect differences efficiently.

**Problem types:** Finding single number, missing numbers, duplicate detection, bit manipulation puzzles.

```python
def single_number(nums):
    """
    Find single number when all others appear twice.
    
    XOR property: a ⊕ a = 0, so all pairs cancel out,
    leaving only the single number.
    
    Time: O(n), Space: O(1)
    """
    result = 0
    for num in nums:
        result ^= num
    return result

def single_number_ii(nums):
    """
    Find single number when all others appear three times.
    
    Use bit manipulation to count occurrences of each bit position.
    Single number contributes 1 to bit count, triplets contribute 0 (mod 3).
    
    Time: O(n), Space: O(1)
    """
    ones = 0  # Bits that appeared 1 time
    twos = 0  # Bits that appeared 2 times
    
    for num in nums:
        # Update twos: bits that were in ones and now appear again
        twos |= ones & num
        
        # Update ones: toggle bits in current number
        ones ^= num
        
        # Remove bits that appeared 3 times (in both ones and twos)
        threes = ones & twos
        ones &= ~threes
        twos &= ~threes
    
    return ones

def single_number_iii(nums):
    """
    Find two single numbers when all others appear twice.
    
    XOR all numbers to get XOR of two singles.
    Use any set bit to partition array and find each single.
    
    Time: O(n), Space: O(1)
    """
    # XOR of two single numbers
    xor_two = 0
    for num in nums:
        xor_two ^= num
    
    # Find rightmost set bit
    rightmost_bit = xor_two & (-xor_two)
    
    # Partition numbers based on this bit
    num1 = 0
    num2 = 0
    
    for num in nums:
        if num & rightmost_bit:
            num1 ^= num
        else:
            num2 ^= num
    
    return [num1, num2]

def missing_number(nums):
    """
    Find missing number from 0 to n.
    
    XOR all indices with all numbers. Missing number remains.
    
    Time: O(n), Space: O(1)
    """
    n = len(nums)
    result = n  # Start with n (the potentially missing number)
    
    for i in range(n):
        result ^= i ^ nums[i]
    
    return result

def find_missing_numbers(nums):
    """
    Find all missing numbers from 1 to n where some numbers appear twice.
    
    Use XOR to mark visited numbers by negating values at corresponding indices.
    
    Time: O(n), Space: O(1)
    """
    missing = []
    
    # Mark numbers as visited by negating value at index
    for num in nums:
        index = abs(num) - 1
        if nums[index] > 0:
            nums[index] = -nums[index]
    
    # Find positive values (unmarked = missing)
    for i in range(len(nums)):
        if nums[i] > 0:
            missing.append(i + 1)
    
    return missing

def maximum_xor_pair(nums):
    """
    Find maximum XOR of any two numbers in array.
    
    Build numbers bit by bit, greedily choosing path that
    maximizes XOR at each bit position.
    
    Time: O(n × log(max_num)), Space: O(n × log(max_num))
    """
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_end = False
    
    def insert_binary(root, num):
        """Insert number's binary representation into trie."""
        node = root
        for i in range(31, -1, -1):  # 32-bit numbers
            bit = (num >> i) & 1
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]
        node.is_end = True
    
    def find_max_xor_with(root, num):
        """Find number in trie that gives maximum XOR with num."""
        node = root
        max_xor = 0
        
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            # Try to go opposite direction for maximum XOR
            toggle_bit = 1 - bit
            
            if toggle_bit in node.children:
                max_xor |= (1 << i)
                node = node.children[toggle_bit]
            else:
                node = node.children[bit]
        
        return max_xor
    
    if len(nums) < 2:
        return 0
    
    root = TrieNode()
    
    # Insert all numbers into trie
    for num in nums:
        insert_binary(root, num)
    
    max_xor = 0
    
    # For each number, find its maximum XOR pair
    for num in nums:
        max_xor = max(max_xor, find_max_xor_with(root, num))
    
    return max_xor

def subarray_xor_equal_k(nums, k):
    """
    Count subarrays with XOR equal to k.
    
    Use prefix XOR and hash map. If prefix_xor[i] ⊕ prefix_xor[j] = k,
    then subarray from j+1 to i has XOR = k.
    
    Time: O(n), Space: O(n)
    """
    count = 0
    xor_freq = {0: 1}  # Empty prefix has XOR 0
    current_xor = 0
    
    for num in nums:
        current_xor ^= num
        
        # Check if there's a prefix with XOR = current_xor ⊕ k
        target = current_xor ^ k
        count += xor_freq.get(target, 0)
        
        # Update frequency of current prefix XOR
        xor_freq[current_xor] = xor_freq.get(current_xor, 0) + 1
    
    return count

def decode_xored_array(encoded, first):
    """
    Decode XOR-encoded array given first element.
    
    If encoded[i] = original[i] ⊕ original[i+1],
    then original[i+1] = encoded[i] ⊕ original[i].
    
    Time: O(n), Space: O(n)
    """
    original = [first]
    
    for i in range(len(encoded)):
        original.append(original[-1] ^ encoded[i])
    
    return original

def xor_queries_subarray(arr, queries):
    """
    Answer XOR queries on subarrays efficiently.
    
    Use prefix XOR array. XOR of subarray [i, j] = prefix[j+1] ⊕ prefix[i].
    
    Time: O(n + q), Space: O(n)
    """
    # Build prefix XOR array
    prefix_xor = [0]
    for num in arr:
        prefix_xor.append(prefix_xor[-1] ^ num)
    
    result = []
    for left, right in queries:
        # XOR of subarray [left, right]
        subarray_xor = prefix_xor[right + 1] ^ prefix_xor[left]
        result.append(subarray_xor)
    
    return result

def count_triplets_xor(arr, r):
    """
    Count triplets (i, j, k) where i < j < k and 
    arr[i] ⊕ arr[i+1] ⊕ ... ⊕ arr[j-1] = arr[j] ⊕ arr[j+1] ⊕ ... ⊕ arr[k].
    
    Use prefix XOR and hash maps to count efficiently.
    
    Time: O(n), Space: O(n)
    """
    from collections import defaultdict
    
    count = 0
    prefix_xor = 0
    
    # Map prefix XOR to list of indices
    xor_indices = defaultdict(list)
    xor_indices[0].append(-1)  # Empty prefix
    
    for i, num in enumerate(arr):
        prefix_xor ^= num
        
        # For each previous occurrence of current prefix XOR
        for prev_idx in xor_indices[prefix_xor]:
            # Count valid middle points
            mid_count = 0
            temp_xor = 0
            
            for j in range(prev_idx + 1, i):
                temp_xor ^= arr[j]
                if temp_xor == r:
                    mid_count += 1
            
            count += mid_count
        
        xor_indices[prefix_xor].append(i)
    
    return count

def flip_bits_to_convert(a, b):
    """
    Count minimum bit flips to convert number a to number b.
    
    XOR a and b, then count set bits in result.
    
    Time: O(log n), Space: O(1)
    """
    xor_result = a ^ b
    
    # Count set bits
    count = 0
    while xor_result:
        count += xor_result & 1
        xor_result >>= 1
    
    return count

# Alternative counting using Brian Kernighan's algorithm
def count_set_bits_kernighan(n):
    """Count set bits using Brian Kernighan's algorithm."""
    count = 0
    while n:
        n &= n - 1  # Remove rightmost set bit
        count += 1
    return count

def xor_beauty_array(nums):
    """
    Calculate XOR beauty: sum of (nums[i] | nums[j]) & nums[k] for all i,j,k.
    
    Use bit manipulation properties to solve efficiently.
    
    Time: O(n × log(max_num)), Space: O(1)
    """
    n = len(nums)
    total_beauty = 0
    
    # Process each bit position
    for bit in range(32):  # 32-bit numbers
        ones = sum(1 for num in nums if num & (1 << bit))
        zeros = n - ones
        
        # For each bit position, calculate contribution to total beauty
        # (nums[i] | nums[j]) has bit set if at least one of nums[i], nums[j] has bit set
        # This happens in: n² - zeros² cases
        # Among these, nums[k] has bit set in 'ones' cases
        
        bit_contribution = ((n * n - zeros * zeros) * ones) * (1 << bit)
        total_beauty += bit_contribution
    
    return total_beauty

# Example usage and comprehensive testing
print("=== Bitwise XOR Examples ===")

# Single number variants
nums1 = [2, 2, 1]
single1 = single_number(nums1)
print(f"Single number in {nums1}: {single1}")

nums2 = [2, 2, 3, 2]
single2 = single_number_ii(nums2)
print(f"Single number (others appear 3 times) in {nums2}: {single2}")

nums3 = [1, 2, 1, 3, 2, 5]
singles3 = single_number_iii(nums3)
print(f"Two single numbers in {nums3}: {singles3}")

# Missing number
nums = [3, 0, 1]
missing = missing_number(nums)
print(f"Missing number in {nums}: {missing}")

# Maximum XOR pair
nums = [3, 10, 5, 25, 2, 8]
max_xor = maximum_xor_pair(nums)
print(f"Maximum XOR pair in {nums}: {max_xor}")

# Subarray XOR equal to k
nums = [4, 2, 2, 6, 4]
k = 6
xor_count = subarray_xor_equal_k(nums, k)
print(f"Subarrays with XOR {k}: {xor_count}")

# Decode XOR array
encoded = [1, 2, 3]
first = 1
decoded = decode_xored_array(encoded, first)
print(f"Decoded array: {decoded}")

# XOR queries
arr = [1, 3, 4, 8]
queries = [[0, 1], [1, 2], [0, 3], [3, 3]]
query_results = xor_queries_subarray(arr, queries)
print(f"XOR query results: {query_results}")

# Bit flip count
a, b = 10, 7  # 1010 and 0111
flips = flip_bits_to_convert(a, b)
print(f"Bit flips to convert {a} to {b}: {flips}")



## 26. Mathematical Patterns

**When to use:** Problems involving number theory, combinatorics, geometry, or mathematical relationships. Often these problems have elegant mathematical solutions that are more efficient than brute force.

**Key insight:** Look for mathematical properties, formulas, or patterns that can transform a complex problem into a simple calculation. Mathematical insights often lead to O(1) or O(log n) solutions.

**Problem types:** GCD/LCM, prime numbers, factorials, combinations, geometric problems, number sequences.

```python
import math
from collections import defaultdict

def gcd_euclidean(a, b):
    """
    Find Greatest Common Divisor using Euclidean algorithm.
    
    Key insight: gcd(a, b) = gcd(b, a % b)
    
    Time: O(log(min(a, b))), Space: O(1)
    """
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """
    Find Least Common Multiple using GCD.
    
    Formula: lcm(a, b) = (a * b) / gcd(a, b)
    
    Time: O(log(min(a, b))), Space: O(1)
    """
    return abs(a * b) // gcd_euclidean(a, b)

def sieve_of_eratosthenes(n):
    """
    Find all prime numbers up to n using Sieve of Eratosthenes.
    
    Mark multiples of each prime as composite.
    
    Time: O(n log log n), Space: O(n)
    """
    if n < 2:
        return []
    
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            # Mark multiples of i as composite
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    
    return [i for i in range(2, n + 1) if is_prime[i]]

def is_prime(n):
    """
    Check if number is prime using trial division.
    
    Only check divisors up to √n.
    
    Time: O(√n), Space: O(1)
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    
    return True

def prime_factorization(n):
    """
    Find prime factorization of number.
    
    Divide by small primes first, then check larger factors.
    
    Time: O(√n), Space: O(log n)
    """
    factors = []
    
    # Handle factor 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # Handle odd factors
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    
    # If n is still > 2, it's a prime factor
    if n > 2:
        factors.append(n)
    
    return factors

def count_divisors(n):
    """
    Count number of divisors of n.
    
    Use prime factorization: if n = p1^a1 * p2^a2 * ... * pk^ak,
    then divisors = (a1 + 1) * (a2 + 1) * ... * (ak + 1).
    
    Time: O(√n), Space: O(1)
    """
    count = 1
    
    # Count powers of 2
    power = 0
    temp = n
    while temp % 2 == 0:
        power += 1
        temp //= 2
    count *= (power + 1)
    
    # Count powers of odd primes
    for i in range(3, int(n**0.5) + 1, 2):
        power = 0
        while temp % i == 0:
            power += 1
            temp //= i
        count *= (power + 1)
    
    # If remaining number > 1, it's a prime
    if temp > 1:
        count *= 2
    
    return count

def modular_exponentiation(base, exp, mod):
    """
    Calculate (base^exp) % mod efficiently.
    
    Use binary exponentiation to avoid overflow.
    
    Time: O(log exp), Space: O(1)
    """
    result = 1
    base = base % mod
    
    while exp > 0:
        # If exp is odd, multiply base with result
        if exp % 2 == 1:
            result = (result * base) % mod
        
        # Square base and halve exponent
        exp >>= 1
        base = (base * base) % mod
    
    return result

def factorial_mod(n, mod):
    """
    Calculate n! % mod efficiently.
    
    Handle large factorials using modular arithmetic.
    
    Time: O(n), Space: O(1)
    """
    if n >= mod:
        return 0  # n! contains mod as factor
    
    result = 1
    for i in range(1, n + 1):
        result = (result * i) % mod
    
    return result

def combination_mod(n, r, mod):
    """
    Calculate C(n, r) % mod using modular arithmetic.
    
    C(n, r) = n! / (r! * (n-r)!)
    Use modular inverse for division.
    
    Time: O(n), Space: O(1)
    """
    if r > n or r < 0:
        return 0
    if r == 0 or r == n:
        return 1
    
    def mod_inverse(a, m):
        """Find modular inverse using extended Euclidean algorithm."""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a, m)
        if gcd != 1:
            return None  # Inverse doesn't exist
        return (x % m + m) % m
    
    # Calculate numerator and denominator
    numerator = 1
    denominator = 1
    
    # Use smaller range for efficiency
    r = min(r, n - r)
    
    for i in range(r):
        numerator = (numerator * (n - i)) % mod
        denominator = (denominator * (i + 1)) % mod
    
    # Calculate result using modular inverse
    inv_denominator = mod_inverse(denominator, mod)
    if inv_denominator is None:
        return None
    
    return (numerator * inv_denominator) % mod

def fibonacci_matrix_fast(n):
    """
    Calculate nth Fibonacci number using matrix exponentiation.
    
    [F(n+1)]   [1 1]^n   [1]
    [F(n)  ] = [1 0]   * [0]
    
    Time: O(log n), Space: O(1)
    """
    def matrix_multiply(A, B):
        """Multiply two 2x2 matrices."""
        return [
            [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
        ]
    
    def matrix_power(matrix, n):
        """Calculate matrix^n using binary exponentiation."""
        if n == 1:
            return matrix
        
        if n % 2 == 0:
            half = matrix_power(matrix, n // 2)
            return matrix_multiply(half, half)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, n - 1))
    
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(base_matrix, n)
    
    return result_matrix[0][1]  # F(n)

def catalan_number(n):
    """
    Calculate nth Catalan number.
    
    C(n) = (2n choose n) / (n + 1) = (2n)! / ((n+1)! * n!)
    
    Time: O(n), Space: O(1)
    """
    if n <= 1:
        return 1
    
    # Calculate using recurrence: C(n) = Σ C(i) * C(n-1-i)
    catalan = [0] * (n + 1)
    catalan[0] = catalan[1] = 1
    
    for i in range(2, n + 1):
        for j in range(i):
            catalan[i] += catalan[j] * catalan[i - 1 - j]
    
    return catalan[n]

def pascal_triangle_row(row_index):
    """
    Generate specific row of Pascal's triangle.
    
    Use combination formula: C(n, k) = C(n, k-1) * (n - k + 1) / k
    
    Time: O(n), Space: O(n)
    """
    row = [1]
    
    for k in range(1, row_index + 1):
        # C(n, k) = C(n, k-1) * (n - k + 1) / k
        next_val = row[-1] * (row_index - k + 1) // k
        row.append(next_val)
    
    return row

def sum_of_arithmetic_progression(first, diff, n):
    """
    Calculate sum of arithmetic progression.
    
    Sum = n/2 * (2*first + (n-1)*diff)
    
    Time: O(1), Space: O(1)
    """
    return n * (2 * first + (n - 1) * diff) // 2

def sum_of_geometric_progression(first, ratio, n):
    """
    Calculate sum of geometric progression.
    
    Sum = first * (ratio^n - 1) / (ratio - 1) if ratio != 1
    Sum = first * n if ratio == 1
    
    Time: O(log n), Space: O(1)
    """
    if ratio == 1:
        return first * n
    
    return first * (pow(ratio, n) - 1) // (ratio - 1)

def count_trailing_zeros_factorial(n):
    """
    Count trailing zeros in n!.
    
    Trailing zeros come from factors of 10 = 2 * 5.
    Since factors of 2 are more abundant, count factors of 5.
    
    Time: O(log n), Space: O(1)
    """
    count = 0
    power_of_5 = 5
    
    while power_of_5 <= n:
        count += n // power_of_5
        power_of_5 *= 5
    
    return count

def angle_between_clock_hands(hour, minute):
    """
    Calculate angle between clock hands.
    
    Hour hand moves 0.5° per minute, minute hand moves 6° per minute.
    
    Time: O(1), Space: O(1)
    """
    # Normalize hour to 12-hour format
    hour = hour % 12
    
    # Calculate angles from 12 o'clock
    minute_angle = minute * 6  # 360° / 60 minutes = 6° per minute
    hour_angle = hour * 30 + minute * 0.5  # 30° per hour + 0.5° per minute
    
    # Find absolute difference
    angle = abs(hour_angle - minute_angle)
    
    # Return smaller angle
    return min(angle, 360 - angle)

def water_container_max_area(heights):
    """
    Find maximum water that can be contained between two lines.
    
    Use two pointers: move pointer with smaller height inward.
    
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(heights) - 1
    max_area = 0
    
    while left < right:
        # Calculate current area
        width = right - left
        height = min(heights[left], heights[right])
        area = width * height
        max_area = max(max_area, area)
        
        # Move pointer with smaller height
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    
    return max_area

def integer_to_english_words(num):
    """
    Convert integer to English words representation.
    
    Break number into groups of thousands and convert each group.
    
    Time: O(log n), Space: O(1)
    """
    if num == 0:
        return "Zero"
    
    # Word mappings
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
            "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
            "Seventeen", "Eighteen", "Nineteen"]
    
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    
    thousands = ["", "Thousand", "Million", "Billion"]
    
    def convert_hundreds(n):
        """Convert number < 1000 to words."""
        result = ""
        
        if n >= 100:
            result += ones[n // 100] + " Hundred"
            n %= 100
            if n > 0:
                result += " "
        
        if n >= 20:
            result += tens[n // 10]
            n %= 10
            if n > 0:
                result += " " + ones[n]
        elif n > 0:
            result += ones[n]
        
        return result
    
    result = ""
    thousand_index = 0
    
    while num > 0:
        if num % 1000 != 0:
            group_words = convert_hundreds(num % 1000)
            if thousands[thousand_index]:
                group_words += " " + thousands[thousand_index]
            
            if result:
                result = group_words + " " + result
            else:
                result = group_words
        
        num //= 1000
        thousand_index += 1
    
    return result

# Example usage and comprehensive testing
print("=== Mathematical Patterns Examples ===")

# GCD and LCM
a, b = 48, 18
print(f"GCD({a}, {b}) = {gcd_euclidean(a, b)}")
print(f"LCM({a}, {b}) = {lcm(a, b)}")

# Prime numbers
n = 30
primes = sieve_of_eratosthenes(n)
print(f"Primes up to {n}: {primes}")

# Prime factorization
num = 60
factors = prime_factorization(num)
print(f"Prime factors of {num}: {factors}")

# Divisors count
print(f"Number of divisors of {num}: {count_divisors(num)}")

# Modular exponentiation
base, exp, mod = 3, 10, 1000
result = modular_exponentiation(base, exp, mod)
print(f"{base}^{exp} mod {mod} = {result}")

# Fast Fibonacci
n = 20
fib_fast = fibonacci_matrix_fast(n)
print(f"Fibonacci({n}) = {fib_fast}")

# Catalan number
n = 5
catalan = catalan_number(n)
print(f"Catalan({n}) = {catalan}")

# Pascal's triangle row
row_idx = 4
pascal_row = pascal_triangle_row(row_idx)
print(f"Pascal triangle row {row_idx}: {pascal_row}")

# Clock angle
hour, minute = 3, 30
angle = angle_between_clock_hands(hour, minute)
print(f"Angle at {hour}:{minute:02d} = {angle}°")

# Trailing zeros in factorial
n = 100
zeros = count_trailing_zeros_factorial(n)
print(f"Trailing zeros in {n}!: {zeros}")

# Integer to English words
num = 1234567
english = integer_to_english_words(num)
print(f"{num} in words: {english}")



# Conclusion

This comprehensive guide covers 26 essential patterns that form the foundation of algorithmic problem-solving. Each pattern represents a fundamental approach to thinking about and solving computational problems.

## Key Takeaways

**Pattern Recognition is Everything**: The most important skill in competitive programming and technical interviews is recognizing which pattern applies to a given problem. Once you identify the pattern, the implementation becomes much more straightforward.

**Start Simple, Build Up**: Most complex algorithms are built from combinations of these basic patterns. Master the fundamentals first, then learn to combine them effectively.

**Practice Implementation**: Understanding the theory is just the beginning. Practice implementing each pattern until it becomes second nature. Focus on writing clean, bug-free code quickly.

**Time and Space Complexity**: Always analyze and optimize your solutions. Understanding the trade-offs between time and space complexity is crucial for choosing the right approach.

## How to Use This Guide

1. **Study Each Pattern**: Understand the key insights and when to apply each pattern
2. **Implement Examples**: Code each example yourself to build muscle memory  
3. **Solve Related Problems**: Find similar problems on platforms like LeetCode, HackerRank, or Codeforces
4. **Combine Patterns**: Learn to recognize when problems require multiple patterns working together
5. **Review Regularly**: Revisit patterns you find challenging until they become intuitive

## Next Steps

- Practice problems from each category on coding platforms
- Time yourself implementing solutions to build speed
- Learn advanced variations of each pattern
- Study how patterns combine in complex problems
- Participate in competitive programming contests

Remember: algorithmic thinking is a skill that improves with deliberate practice. These patterns provide the building blocks, but mastery comes from applying them consistently across many different problems.

Happy coding! 🚀
        
