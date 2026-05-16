import subprocess
import time
import os
import platform

# ============ configuration ============
DATASET = "Comp3041J MiniProject 2 Dataset.csv"
OUTPUT_DIR = "mr_outputs"

JOBS = [
    ("Output 1: Request Count by Service",  "mr_request_count.py", "output1_full.txt"),
    ("Output 2: Server Error Count",        "mr_error_count.py",   "output2_full.txt"),
    ("Output 3: Top 10 Slow Endpoints",     "mr_slow_endpoints.py","output3_full.txt"),
]
# ==============================

# check
if not os.path.exists(DATASET):
    print(f"ERROR: Dataset file not found: {DATASET}")
    exit(1)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# environmental message
print("=" * 60)
print("EXECUTION ENVIRONMENT")
print("=" * 60)
print(f"OS:            {platform.system()} {platform.release()}")
print(f"Python:        {platform.python_version()}")
print(f"Machine:       {platform.machine()}")
print(f"Dataset:       {DATASET}")
print(f"Dataset size:  {os.path.getsize(DATASET)/1024/1024:.2f} MB")

# Number of rows in the dataset
with open(DATASET, 'r', encoding='utf-8') as f:
    line_count = sum(1 for _ in f)
print(f"Total lines:   {line_count} (incl. header)")
print()

# Run three MR Jobs
results = []
for name, script, outfile in JOBS:
    out_path = os.path.join(OUTPUT_DIR, outfile)
    print(f"=== Running: {name} ===")
    start = time.time()
    with open(out_path, 'w', encoding='utf-8') as f:
        subprocess.run(
            ["python", script, "-r", "inline", DATASET],
            stdout=f
        )
    elapsed = time.time() - start
    results.append((name, elapsed, out_path))
    print(f"  Output:  {out_path}")
    print(f"  Time:    {elapsed:.2f} seconds\n")


print("=" * 60)
print("RUNTIME SUMMARY")
print("=" * 60)
for name, elapsed, _ in results:
    print(f"  {name:<45}: {elapsed:>7.2f} s")
total = sum(t for _, t, _ in results)
print(f"  {'TOTAL':<45}: {total:>7.2f} s")

# Write to the operation log
log_path = os.path.join(OUTPUT_DIR, "runtime_log.txt")
with open(log_path, 'w', encoding='utf-8') as f:
    f.write("MapReduce Execution Log\n")
    f.write("=" * 60 + "\n")
    f.write(f"OS:           {platform.system()} {platform.release()}\n")
    f.write(f"Python:       {platform.python_version()}\n")
    f.write(f"Dataset:      {DATASET}\n")
    f.write(f"Dataset size: {os.path.getsize(DATASET)/1024/1024:.2f} MB\n")
    f.write(f"Total lines:  {line_count}\n\n")
    f.write("Job Runtimes:\n")
    for name, elapsed, out_path in results:
        f.write(f"  {name}: {elapsed:.2f} s  -> {out_path}\n")
    f.write(f"\n  TOTAL: {total:.2f} s\n")

print(f"\nLog saved to: {log_path}")
print("Done!")