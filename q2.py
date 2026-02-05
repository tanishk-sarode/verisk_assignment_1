import boto3
import json
import pprint
from botocore.config import Config
from concurrent.futures import ThreadPoolExecutor, as_completed

# ------------------ CONFIG ------------------

BUCKET_NAME = "my-test-bucket-3321"
FILES = [f"config_{i}.json" for i in range(5)]
OUTPUT_FILE = "consolidated_config.json"

session = boto3.Session(
    profile_name="sandbox",
    region_name="us-east-1"
)

s3 = session.client(
    "s3",
    config=Config(signature_version="s3v4"),
    verify=False
)


def download_file(key):
    s3.download_file(BUCKET_NAME, key, key)
    return key

def download_files():
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_file, key) for key in FILES]
        for future in as_completed(futures):
            future.result() 


def merge_dicts(dicts):
    merged = {}
    conflicts = {}

    def deep_merge(target, source, path=""):
        for key, value in source.items():
            current_path = f"{path}.{key}" if path else key

            if key not in target:
                target[key] = value
            else:
                existing = target[key]

                if isinstance(existing, dict) and isinstance(value, dict):
                    deep_merge(existing, value, current_path)
                elif existing == value:
                    continue
                else:
                    conflicts[current_path] = (existing, value)

    for d in dicts:
        deep_merge(merged, d)

    return merged, conflicts



def load_configs():
    configs = []
    for file in FILES:
        with open(file) as f:
            configs.append(json.load(f))
    return configs



def upload_to_s3():
    s3.upload_file(
        OUTPUT_FILE,
        BUCKET_NAME,
        OUTPUT_FILE
    )

    

# ------------------ EXECUTE ------------------

if __name__ == "__main__":
    download_files()
    configs = load_configs()

    # Merge
    merged, conflicts = merge_dicts(configs)

    print("\nConflicts Detected:")
    pprint.pprint(conflicts)

    # raise Exception("Resolve conflicts before proceeding.")

    user_input = input("\nDo you want to proceed with uploading the consolidated file? (y/n): ")
    if user_input.lower() != "y":
        print("Upload cancelled.")
        exit(0)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(merged, f, indent=4)
    upload_to_s3()
    print("\nUpload successful.")
