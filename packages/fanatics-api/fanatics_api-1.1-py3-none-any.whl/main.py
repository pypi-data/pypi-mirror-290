import os
import requests
import time
import json
import csv
import argparse


def fetch_data(prefix, begin, end, failed_file, time_sleep):
    url = "https://www.fanatics.com/api/authenticity-verification/validate"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.fanatics.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }
    count = 0
    for i in range(begin, end):
        serialNumber = prefix + str(i).zfill(6)
        if os.path.exists(f"data/{serialNumber}.json"):
            continue

        payload = {
            "serialNumber": serialNumber,
            "vc": "",
            "use24carat": "true"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")
            with open(failed_file, "a") as file:
                file.write(f"{serialNumber} Request Exception: {e}\n")
            count += 1
            if(count > 20):
                print("Too many request exceptions. Exiting.")
                break
            continue
        time.sleep(time_sleep)

        if response.status_code == 200:
            print(f"Serial Number: {serialNumber}")
            with open(f"data/{serialNumber}.json", "w") as file:
                file.write(response.text)
        else:
            with open(failed_file, "a") as file:
                file.write(f"{serialNumber} {response.status_code} {response.text}\n")
            break


def retry_failed(failed_file, time_sleep):
    url = "https://www.fanatics.com/api/authenticity-verification/validate"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.fanatics.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }

    with open(failed_file, "r") as file:
        lines = file.readlines()

    for line in lines:
        serialNumber, status_code, _ = line.split(" ", 2)
        payload = {
            "serialNumber": serialNumber,
            "vc": "",
            "use24carat": "true"
        }

        response = requests.post(url, headers=headers, json=payload)
        time.sleep(time_sleep)

        if response.status_code == 200:
            print(f"Retry Successful for: {serialNumber}")
            with open(f"data/{serialNumber}.json", "a") as file:
                file.write(response.text)
            # Remove from failed file after successful retry
            lines.remove(line)

    # Update the failed file
    with open(failed_file, "w") as file:
        file.writelines(lines)


def json_to_csv(output_csv):
    fieldnames = ["HologramID", "SignedBy", "productDescription", "Inscription", "LimitedEdition", "valid"]
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for filename in os.listdir("data"):
            if filename.endswith(".json"):
                HologramID = filename.split(".")[0]
                with open(f"data/{filename}", "r") as file:
                    data = json.load(file)
                    athletes = data.get("athletes", [])
                    if(athletes is None):
                        athletes = []
                    writer.writerow({
                        "HologramID": HologramID,
                        "SignedBy": "，".join(athletes),
                        "productDescription": data.get("productDescription", "").replace(",", "，"),
                        "Inscription": data.get("Inscription", "").replace(",", "，"),
                        "LimitedEdition": data.get("LE", "").replace(",", "，"),
                        "valid": data.get("valid", "")
                    })

import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Fanatics API Data Fetcher (Fanatics API 数据抓取工具)"
    )
    parser.add_argument(
        "--start", 
        type=int, 
        help="Start number for fetching data (开始抓取数据的编号)"
    )
    parser.add_argument(
        "--end", 
        type=int, 
        help="End number for fetching data (结束抓取数据的编号)"
    )
    parser.add_argument(
        "--prefix", 
        type=str, 
        default="B", 
        help="Prefix letter for serial numbers (序列号的前缀字母)"
    )
    parser.add_argument(
        "--failed-file", 
        type=str, 
        default="failed.txt", 
        help="Path to the failed file (失败文件的路径)"
    )
    parser.add_argument(
        "--time-sleep", 
        type=float, 
        default=1.0, 
        help="Time sleep duration between requests (每次请求之间的休眠时间, 单位：秒)"
    )
    parser.add_argument(
        "--fetch", 
        action="store_true", 
        help="Fetch data based on start and end range (根据起始和结束范围抓取数据)"
    )
    parser.add_argument(
        "--retry", 
        action="store_true", 
        help="Retry failed serial numbers (重试失败的序列号)"
    )
    parser.add_argument(
        "--to-csv", 
        action="store_true", 
        help="Convert JSON files to CSV (将JSON文件转换为CSV)"
    )
    parser.add_argument(
        "--output-csv", 
        type=str, 
        default="output.csv", 
        help="Output CSV file name (输出CSV文件的名称)"
    )

    args = parser.parse_args()

    
    print("You are asked to provide the password to continue. (您被要求提供密码以继续。)")
    password = input("Password: ")
    if password != "qw!io.val@$kt%pa.cli#dkgp;":
        print("Incorrect password. (密码错误。)")
        return

    if args.fetch:
        if args.start is not None and args.end is not None:
            if(not os.path.exists("data")):
                os.makedirs("data")
            fetch_data(args.prefix, args.start, args.end + 1, args.failed_file, args.time_sleep)
        else:
            print("Please provide both --start and --end arguments for fetching data. (请提供用于抓取数据的--start和--end参数。)")

    if args.retry:
        retry_failed(args.failed_file, args.time_sleep)

    if args.to_csv:
        json_to_csv(args.output_csv)

if __name__ == "__main__":
    main()