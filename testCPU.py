import sys
import time

start_time = time.time()
# Your CPU-intensive code here
end_time = time.time()

cpu_utilization = (end_time - start_time) / sys.getswitchinterval()
print(f"CPU utilization: {cpu_utilization}%")
