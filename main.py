import argparse
import os
from editor import load_config
from service_stress import StressService, Statistics
import time
from editor import csv_data, create_csv_file, ROOT_DIR


def validate_args(args):
    # Ensure the number of domains is within valid range
    if args.num_domains < 1 or args.num_domains > 5000:
        print(f"--num_domains must be between 1 and 5000. You provided {args.num_domains}.")

    # Ensure the file exists
    if not os.path.exists(args.domains_file):
        print(f"Domain file not found: {args.domains_file}")

    # Check if --domains list length matches --num_domains
    if args.domains and len(args.domains) < args.num_domains:
        print(
            f"Warning: You provided {len(args.domains)} domains, but --num_domains is set to {args.num_domains}. Using {len(args.domains)} domains instead.")

def main():
    parser = argparse.ArgumentParser(description="Stress test tool for Reputation API")
    parser.add_argument('--threads', type=int, default=20, help='Number of concurrent requests')
    parser.add_argument('--num_domains', type=int, default=20, help='Number of domains to test (max 5000)')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout in seconds')
    parser.add_argument('--domains', nargs='+', default=[], help='Add a list of domains (space-separated), prioritize using them instead domains_file')
    parser.add_argument('--conf_file', type=str, default=fr"{ROOT_DIR}/service_configuration.json", help="Service configuration file")
    parser.add_argument('--domains_file', default=fr'{ROOT_DIR}\domains.json', help="JSON file with all domains")
    parser.add_argument('--request_timeout', type=int, default=1, help="timeout to send request")
    parser.add_argument('--csv', type=bool, default=True, help="Create csv file - True/False")


    args = parser.parse_args()
    print("Start stress service test...")
    validate_args(args)

    # Load domains from the file first
    domain_data = load_config(args.domains_file)
    domains_from_file = domain_data.get('domains', [])

    # If additional domains are provided via --domains, prioritize using them
    if args.domains:
        selected_domains = args.domains[:args.num_domains]  # Respect num_domains limit
    else:
        # Limit the number of domains from the file based on --num_domains argument
        if len(domains_from_file) < args.num_domains:
            print(f"Warning: Only {len(domains_from_file)} domains available in the file. Using available domains.")
            selected_domains = domains_from_file  # Use all available domains from the file
        else:
            selected_domains = domains_from_file[:args.num_domains]  # Use only num_domains from the file

    # Validate that the total number of selected domains does not exceed 5000
    if len(selected_domains) > 5000:
        raise print(f"Total number of domains exceeds the maximum allowed (5000). You provided {len(selected_domains)} domains.")

    # Proceed with the stress test if the number of domains is valid
    stress_results = []
    if args.conf_file:
        stress_service = StressService(args.conf_file)
        start_time = time.time()
        try:
            while True:
                if time.time() - start_time <= args.timeout:
                    # Run the stress test with the selected domains
                    stress_results.extend(stress_service.stress(selected_domains, args.request_timeout, args.threads))
                    # print(stress_result)
                else:
                    break
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
        end_time = time.time() - start_time
        response_times = [result['response_time'] for result in stress_results if not isinstance(result['response_time'], str)]
        print("Test is over!")
        print(f"Requests in total: {len(stress_results)}")
        print(f"Total requests time:{Statistics.total_time(response_times):.3f} seconds")
        print(f"Time in total:{end_time:.3f} seconds")
        print(f"error rate : {Statistics.error_rate(stress_results):.3f}%")
        print(f"Average time for one request: {Statistics.avg_time(response_times):.3f} seconds")
        print(f"Max time for one request: {Statistics.max_time(response_times):.3f} seconds")
        print(f"Min time for one request: {Statistics.min_time(response_times):.3f} seconds")
        print(f"P90 time measure: {Statistics.calculate_percentile(response_times, 90):.3f} seconds")

        if args.csv:
            print("created csv file: ")
            value = [f'{len(stress_results)}',
                     f"{Statistics.total_time(response_times):.3f}",
                     f"{end_time:.3f}",
                     f"{Statistics.error_rate(stress_results):.3f}",
                     f"{Statistics.avg_time(response_times):.3f}",
                     f"{Statistics.max_time(response_times):.3f}",
                     f"{Statistics.min_time(response_times):.3f}",
                     f"{Statistics.calculate_percentile(response_times, 90):.3f}"]
            csv_data["Results"] = value
            create_csv_file(csv_data)


if __name__ == "__main__":
    main()
