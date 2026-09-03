def largest(arr):
    if not arr:
        return None  # Handle empty array case

    largest = arr[0]  # Initialize with the first element

    for num in arr:
        if num > largest:
            largest = num

    return largest