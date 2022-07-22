config = {
    "app_name": "elicit-paper-ingestor",
    "log_level": "INFO",
    "source": {
        "bucket": "paper-sources",
        "s2ag": {
            "samples_s3_key": "s2ag/samples/papers/papers-sample.jsonl.gz",
            "samples_local_path": "data/s2ag/samples/papers/papers-sample.jsonl.gz"
        }
    },
    "output": {
        "bucket": "enriched-papers",
        "local_path": "data/s2ag/output/papers-sample.jsonl.gz",
        "s3_key": "s2ag/output/papers-sample.jsonl.gz"
    }
}
