import gzip
import json
import logging
import os
from typing import Dict, List

import boto3
import pandas as pd

from paper_ingestor.config import config
from paper_ingestor.models.paper import Paper

logging.basicConfig(
    format=f"[{config['app_name']}] %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=config["log_level"]
)
logger = logging.getLogger()


def load_papers(source="s2ag", sample=True) -> List[Dict]:
    """Load papers from source."""
    if source != "s2ag":
        raise NotImplementedError("Sorry, only 's2ag' source is supported.")
    if not sample:
        raise NotImplementedError("Sorry, only sample data loading is supported.")
    if source == "s2ag":
        if sample:
            papers = []
            samples_local_path = config["source"][source]["samples_local_path"]
            if not os.path.exists(samples_local_path):
                download_data_file_from_s3(
                    config["source"]["bucket"],
                    config["source"][source]["samples_s3_key"],
                    samples_local_path
                )
            with gzip.open(samples_local_path, 'rt') as f:
                for line in f:
                    paper_raw = json.loads(line)
                    paper = create_paper_from_s2ag(paper_raw)
                    papers.append(paper)
    return papers


def download_data_file_from_s3(bucket: str, s3_file_path: str, local_file_path: str):
    """Download file from S3 and create required local folders if they don't exist."""
    logger.info("Downloading %s from %s bucket in S3 to %s.", bucket, s3_file_path, local_file_path)
    s3 = boto3.resource('s3')
    local_folders = "/".join(local_file_path.split("/")[:-1])
    logger.info("Creating directories %s.", local_folders)
    os.makedirs(local_folders, exist_ok=True)
    s3.Bucket(bucket).download_file(s3_file_path, local_file_path)


def create_paper_from_s2ag(paper_raw: Dict) -> Paper:
    """Create paper objec from dictionary from S2AG"""
    return Paper(
        uniqueId=paper_raw["corpusid"],
        title=paper_raw["title"],
        abstract="",
        authorNames=[author["name"] for author in paper_raw["authors"]], # get name, up to 500
        publicationYear = paper_raw["year"],
        doi=paper_raw["externalids"]["DOI"],
        urls=[paper_raw["url"]],
        outCitations=[],
        inCitations=[]
    )

if __name__=="__main__":
    logger.info("Starting with configurations: %s", config)
    logger.info("Loading papers.")
    sample_s2ag_papers = load_papers()
    logger.info("Deduplicating papers by the id.")
    sample_s2ag_papers_df = pd.DataFrame(sample_s2ag_papers).drop_duplicates(subset=["uniqueId"])
    logger.info(sample_s2ag_papers_df.head())
