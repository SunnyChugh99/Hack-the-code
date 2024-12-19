import time

def cpu_intensive_code(n):
    sum_of_squares = 0
    for i in range(1, n+1):
        sum_of_squares += i ** 2
    return sum_of_squares

start_time = time.time()
result = cpu_intensive_code(10**7)
end_time = time.time()

print(f"Result: {result}")
print(f"Time taken: {end_time - start_time} seconds")
