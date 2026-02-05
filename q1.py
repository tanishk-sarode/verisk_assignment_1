# 5. An async app:
# 1.Fetches data from an API (I/O-bound)
# 2.Processes the data with heavy computation (CPU-bound)
# Prevent blocking the event loop
# Combine asyncio with executors?

import asyncio
from concurrent.futures import ProcessPoolExecutor


async def fetch_data():
    print("Fetching data from API...")
    await asyncio.sleep(5)
    print("fetched data from the API...")
    return {"data": [1, 2, 3, 4, 5]}

def process_data(data):
    print("Processing data...")
    total = 0
    for number in data["data"]:
        for _ in range(10**6):
            total += number
    print("Data processed.")
    return total

async def main():
    loop = asyncio.get_running_loop()
    fetch_futures = [fetch_data() for _ in range(0,5)]

    fetch_results = [await fetch_future for fetch_future in asyncio.as_completed(fetch_futures)]

    with ProcessPoolExecutor() as executor:
        results = [
            loop.run_in_executor(executor, process_data, data) for data in fetch_results
        ]
        results = await asyncio.gather(*results)

        

    print(f"Result: {results}")

if __name__ == "__main__":
    asyncio.run(main())


    