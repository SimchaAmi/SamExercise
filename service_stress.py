from asyncio import as_completed
from editor import load_config
import numpy as np
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


class Request:
    def __init__(self, conf_file):
        self.conf = load_config(conf_file)
        self.base_url = self.conf['request']['base_url']
        self.headers = {'Authorization': f'{self.conf["token"]}'}
        self.request = requests

    def send_request(self, domain, timeout):
        url = f"{self.base_url}/{domain}"
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout)
            # print(response.status_code)
            return domain, response.status_code, response.elapsed.total_seconds(), response.json()
        except requests.RequestException as e:
            return domain, "Error", str(e), 0

class StressService(Request):
    def stress(self, domains, req_timeout, concurrent_requests):
        results = []
        # Create a ThreadPoolExecutor with a number of concurrent threads
        with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            # Submit tasks to the executor
            futures = [executor.submit(self.send_request, domain, req_timeout) for domain in domains]

            # Retrieve the results as they complete
            for i, future in enumerate(as_completed(futures)):
                domain, status_code, response_time, data = future.result()
                results.append({"req_domain": domain, "status_code": status_code, "response_time": response_time, "data": data})
        # print(results)
        return results

class Statistics:
    @staticmethod
    def avg_time(response_times):
        if not response_times:
            return None
        return np.mean(response_times)

    @staticmethod
    def max_time(response_times: list):
        if not response_times:
            return None
        return np.max(response_times)

    @staticmethod
    def min_time(response_times: list):
        if not response_times:
            return None
        return np.min(response_times)

    @staticmethod
    def calculate_percentile(response_times: list, percentile: int):
        if not response_times:
            return None
        return np.percentile(response_times, percentile)

    @staticmethod
    def total_req(data: dict):
        if not data:
            return None
        return len(data['data'])

    @staticmethod
    def total_time(response_times: list):
        if not response_times:
            return None
        return sum(response_times)

    @staticmethod
    def error_rate(data):
        if not data:
            return None
        error_count = 0
        success_count = 0
        for response in data:
            if response['status_code'] == 'Error':
                error_count += 1
            else:
                success_count += 1
        # print(f"error count: {error_count}")
        # print(f"success count: {success_count}")
        return (error_count/success_count)*100
