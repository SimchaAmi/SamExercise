Here's a `README.md` file for your project:

---

# Stress Test Tool for Reputation API

This project provides a command-line tool for stress testing a Reputation API by sending concurrent requests to a list of domains. It gathers and outputs statistics on the requests and saves the results in a CSV file.

## Features

- Stress testing with configurable number of concurrent requests, timeouts, and domain limits.
- Support for domain input via a JSON file or directly through the command line.
- Gathers detailed statistics like total request time, average request time, error rate, and more.
- Saves the results into a CSV file for further analysis.

## Prerequisites

- Python 3.x
- Required Python libraries:
  - `argparse`
  - `json`
  - `os`
  - `time`
  - `pandas`

  You can install the required dependencies with:

  ```bash
  pip install -r requirements.txt
  ```

## Usage

### 1. Clone the repository

Not include GitHub link

download the Zip file to your computer instead
```

### 2. Run the stress test tool

Run the tool using the following command:

```bash
python main.py --threads 10 --num_domains 50 --timeout 30 --domains_file /path/to/domains.json
```

### 3. Command-Line Options

| Argument            | Description                                                              | Default                                 |
|---------------------|--------------------------------------------------------------------------|-----------------------------------------|
| `--threads`         | Number of concurrent requests                                            | 20                                      |
| `--num_domains`     | Number of domains to test (max 5000)                                     | 20                                      |
| `--timeout`         | Timeout for the entire stress test in seconds                            | 10                                      |
| `--domains`         | Space-separated list of domains to test (overrides domains from the file) | []                                      |
| `--conf_file`       | Path to the service configuration file                                   | `C:\GIT\SAM\service_configuration.json` |
| `--domains_file`    | Path to a JSON file containing domains                                   | `C:\GIT\SAM\domains.json`               |
| `--request_timeout` | Timeout for individual requests (in seconds)                             | 1                                       |
| `--csv`             | create csv file                                                          | True                                       |

### Example

Stress test with 50 domains, using 15 concurrent threads and a 20-second test duration:

```bash
python main.py --threads 15 --num_domains 50 --timeout 20
```

### 4. Output

Once the stress test is completed, the program will output statistics and generate a CSV file with the following information:

- Total requests sent
- Total requests time
- Total test duration
- Error rate
- Average time per request
- Maximum time for a single request
- Minimum time for a single request
- P90 percentile time measure

Sample output:

```
Start stress service test...
Test is over!
Requests in total: 100
Total requests time: 79.802 seconds
Time in total: 12.128 seconds
Error rate: 31.579%
Average time for one request: 1.050 seconds
Max time for one request: 2.591 seconds
Min time for one request: 0.504 seconds
P90 time measure: 1.880 seconds
```

The data will also be saved to a CSV file for further analysis.

### CSV Data

The CSV file will contain the following fields:

1. Total Requests
2. Total Requests Time
3. Total Test Time
4. Error Rate
5. Average Request Time
6. Max Request Time
7. Min Request Time
8. P90 Request Time

### Graceful Exit

The stress test tool supports `KeyboardInterrupt` to stop the test at any time. If interrupted, the tool will still output the collected results and statistics.

## How It Works

1. **`main.py`**: The entry point for the tool, handling argument parsing, domain selection, and running the stress test.
2. **`editor.py`**: Contains helper functions for loading configurations and saving results to a CSV file.
3. **`service_stress.py`**: Implements the `StressService` class to send requests and the `Statistics` class to compute metrics (like error rates, response times, etc.).

## License

---
