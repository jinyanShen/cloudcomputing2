import ray
import requests
from collections import defaultdict
import time

TEST_DATA_URL = "https://cloud-22207230.oss-cn-hangzhou.aliyuncs.com/test_500.csv"
FULL_DATA_URL = "https://cloud-22207230.oss-cn-hangzhou.aliyuncs.com/Comp3041J%20MiniProject%202%20Dataset.csv"

ray.init(ignore_reinit_error=True)


@ray.remote
def process_chunk(chunk_lines):
    stats = defaultdict(lambda: {
        "total": 0,
        "slow": 0,
        "server_error": 0,
        "timeout": 0
    })

    for line in chunk_lines:
        line = line.strip()
        if not line or line.startswith("timestamp"):
            continue

        parts = line.split(",")
        if len(parts) < 10:
            continue

        service = parts[3]
        resp_time = int(parts[7]) if parts[7].isdigit() else 0
        status_code = int(parts[6]) if parts[6].isdigit() else 0
        error_type = parts[9].strip()

        stats[service]["total"] += 1
        if resp_time > 800:
            stats[service]["slow"] += 1
        if status_code >= 500:
            stats[service]["server_error"] += 1
        if error_type == "Timeout":
            stats[service]["timeout"] += 1

    return stats


def main(data_url, chunk_size=2000):
    response = requests.get(data_url)
    response.raise_for_status()
    lines = response.text.splitlines()

    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    futures = [process_chunk.remote(chunk) for chunk in chunks]
    chunk_results = ray.get(futures)

    final_stats = defaultdict(lambda: {
        "total": 0,
        "slow": 0,
        "server_error": 0,
        "timeout": 0
    })

    for res in chunk_results:
        for service, s in res.items():
            for k, v in s.items():
                final_stats[service][k] += v

    degraded = []
    for service, s in final_stats.items():
        total = s["total"]
        if total == 0:
            continue

        slow_rate = s["slow"] / total
        error_rate = s["server_error"] / total
        timeout_count = s["timeout"]
        reasons = []

        if slow_rate > 0.2:
            reasons.append("high slow request rate")
        if error_rate > 0.1:
            reasons.append("high server error rate")
        if timeout_count >= 5:
            reasons.append("repeated timeout errors")

        if reasons:
            degraded.append((service, "; ".join(reasons)))

    print("\n===== Service Degradation Results =====")
    for service, reason in degraded:
        print(f"{service}, {reason}")

    return len(lines)


if __name__ == "__main__":
    print("=== Running Test Dataset ===")
    start = time.time()
    main(TEST_DATA_URL)
    print(f"Test time: {time.time() - start:.2f}s\n")

    print("=== Running Full Dataset ===")
    start = time.time()
    main(FULL_DATA_URL)
    print(f"Full dataset time: {time.time() - start:.2f}s")