import os
import sys
import re
import time

class YARAPerformanceBenchmark:
    def __init__(self, rules_file="rules.yar", samples_dir="test_samples"):
        self.rules_file = rules_file
        self.samples_dir = samples_dir
        self.rules = self.parse_rules()

    def parse_rules(self):
        """Lightweight parser to extract rule signatures and strings."""
        if not os.path.exists(self.rules_file):
            print(f"[-] Missing rules file: {self.rules_file}")
            sys.exit(1)

        rules = []
        current_rule = None

        with open(self.rules_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("rule "):
                    rule_name = line.split()[1]
                    current_rule = {"name": rule_name, "strings": [], "regexes": []}
                elif current_rule and line.startswith("$"):
                    parts = line.split("=", 1)
                    pattern = parts[1].strip().strip('"')
                    if pattern.startswith("/") and pattern.endswith("/"):
                        current_rule["regexes"].append(pattern.strip("/"))
                    else:
                        current_rule["strings"].append(pattern.lower())
                elif current_rule and line.startswith("}"):
                    rules.append(current_rule)
                    current_rule = None
        return rules

    def evaluate_rule(self, rule, file_bytes):
        """Matches strings and regular expressions against file bytes."""
        text_content = file_bytes.decode('utf-8', errors='ignore').lower()

        # String matching
        for s in rule["strings"]:
            if s in text_content:
                return True

        # Regex matching
        for r in rule["regexes"]:
            try:
                if re.search(r, text_content):
                    return True
            except Exception:
                pass

        return False

    def run_benchmark(self, iterations=100):
        if not os.path.exists(self.samples_dir):
            print(f"[-] Missing samples directory: {self.samples_dir}")
            sys.exit(1)

        samples = []
        total_bytes = 0
        for root, _, files in os.walk(self.samples_dir):
            for file in files:
                fpath = os.path.join(root, file)
                with open(fpath, "rb") as f:
                    content = f.read()
                    samples.append((fpath, content))
                    total_bytes += len(content)

        print("=" * 70)
        print("⚡ YARA Rule Performance & Overhead Benchmarking Suite")
        print("=" * 70)
        print(f"Loaded Rules: {len(self.rules)}")
        print(f"Loaded Samples: {len(samples)} ({total_bytes / 1024:.2f} KB total)")
        print(f"Benchmark Iterations: {iterations} cycles per rule\n")

        print(f"{'RULE NAME':<32} {'MATCHES':<10} {'TIME (ms)':<12} {'RATE (MB/s)':<12} {'STATUS'}")
        print("-" * 75)

        for rule in self.rules:
            matches_count = 0
            start_time = time.perf_counter()

            for _ in range(iterations):
                for path, content in samples:
                    if self.evaluate_rule(rule, content):
                        matches_count += 1

            duration_sec = time.perf_counter() - start_time
            duration_ms = duration_sec * 1000
            total_mb_scanned = (total_bytes * iterations) / (1024 * 1024)
            rate_mb_s = total_mb_scanned / duration_sec if duration_sec > 0 else 0

            # Flag performance status based on evaluation time
            status = "✓ FAST" if duration_ms < 50 else "⚠️ HIGH CPU"

            print(f"{rule['name']:<32} {matches_count // iterations:<10} {duration_ms:<12.2f} {rate_mb_s:<12.2f} {status}")

        print("-" * 75)
        print("[+] Benchmark testing completed.\n")

if __name__ == "__main__":
    tester = YARAPerformanceBenchmark()
    tester.run_benchmark(iterations=150)
