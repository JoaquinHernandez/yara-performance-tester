# yara-performance-tester

Markdown
# YARA Rule Performance Tester & Malware Matcher

A defensive benchmarking engine designed to measure rule execution performance, scan speed (MB/s), and CPU overhead across sample corpuses.

## Why Performance Testing Matters
Complex regular expressions and short string matches in YARA rules can introduce high CPU overhead and stall automated scanning pipelines. This suite profiles rules to identify performance bottlenecks before deploying signatures to production.

## Features
- **Execution Benchmarking**: Measures time (ms) and throughput (MB/s) across multi-cycle iterations.
- **Overhead Warning Flags**: Automatically flags slow rules (`HIGH CPU`) that exceed evaluation thresholds.
- **Zero Dependencies**: Pure Python implementation with no external C-library requirements.

## Usage
```bash
python3 yara_benchmark.py

---

## 🌐 How to Add to Your GitHub Repository via Web UI

1. Open your **`Blue-Team-Defensive-Security`** repository on GitHub.
2. Click **Add file** $\rightarrow$ **Create new file**.
3. In the file path input, type: `yara-performance-tester/rules.yar`
4. Paste the content of `rules.yar` and click **Commit changes**.
5. Repeat for:
   * `yara-performance-tester/test_samples/clean_sample.txt`
   * `yara-performance-tester/test_samples/webshell_sample.txt`
   * `yara-performance-tester/yara_benchmark.py`
   * `yara-performance-tester/README.md`

