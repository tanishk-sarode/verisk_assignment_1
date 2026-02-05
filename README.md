5. An async app:

1.Fetches data from an API (I/O-bound)

2.Processes the data with heavy computation (CPU-bound)


Prevent blocking the event loop

Combine asyncio with executors?

------------------------------------------------------------------------------


Question 4: Data Aggregation

You have 5 JSON config files in S3. You need to:

· Download all files

· Merge configurations

· Detect conflicts

· Upload consolidated file to S3

How would you handle concurrent merging? What validation would you use?
