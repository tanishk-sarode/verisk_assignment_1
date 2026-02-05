import json
import random
import string

def random_string(n=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def generate_complex_json_files(num_files=5):
    for i in range(num_files):
        config = {
            "service": {
                "name": random.choice(["auth", "billing", "orders"]),
                "enabled": random.choice([True, False]),
                "timeout": random.choice([30, 60, "30"]),  # intentional type conflict
            },
            "database": {
                "host": random.choice(["localhost", "db.internal"]),
                "port": random.choice([5432, "5432"]),  # type conflict
                "retries": random.randint(1, 5),
            },
            "features": {
                "beta": random.choice([True, False]),
                "flags": [
                    random_string(4),
                    random_string(4)
                ]
            },
            "limits": {
                "cpu": random.choice([1, 2, 4]),
                "memory": random.choice(["512Mi", "1Gi"])
            },
            # top-level conflicts
            "version": random.choice([1, "1.0"]),
            "owner": random.choice(["team-a", "team-b"])
        }

        with open(f"config_{i}.json", "w") as f:
            json.dump(config, f, indent=4)

generate_complex_json_files()

