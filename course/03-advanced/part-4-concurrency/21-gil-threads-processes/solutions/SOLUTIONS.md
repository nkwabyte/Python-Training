# Solutions & Commentary — Module 21: The GIL, Threads, and Processes

## Key Takeaways
- The GIL prevents multi-core CPU parallelism in standard Python threads; use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` for CPU-bound tasks.
- Threads excel at I/O-bound concurrency (`threading`, `ThreadPoolExecutor`) where threads release the GIL while waiting on network/disk.
- Use `queue.Queue` for thread-safe producer-consumer pipelines.
