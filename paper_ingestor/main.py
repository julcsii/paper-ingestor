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


def main():
    logger.info("Starting with configurations: %s", config)
    logger.info("Loading papers.")
    sample_s2ag_papers = load_papers()
    sample_s2ag_papers_deduped_df = deduplicate_papers(sample_s2ag_papers)
    save_df_as_jsonl(sample_s2ag_papers_deduped_df, config["output"]["local_path"])
    upload_output_to_s3(
        config["output"]["bucket"],
        config["output"]["local_path"],
        config["output"]["s3_key"]
    )
    logger.info("Completed.")


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


def deduplicate_papers(papers: List[Dict]) -> pd.DataFrame:
    """Deduplicate list of papers by the id and return as DF."""
    logger.info("Deduplicating papers by the id.")
    return pd.DataFrame(papers).drop_duplicates(subset=["uniqueId"])


def download_data_file_from_s3(bucket: str, s3_file_path: str, local_file_path: str):
    """Download file from S3 and create required local folders if they don't exist."""
    logger.info("Downloading %s from %s bucket in S3 to %s.", bucket, s3_file_path, local_file_path)
    s3 = boto3.resource('s3')
    make_non_existing_dirs(local_file_path)
    s3.Bucket(bucket).download_file(s3_file_path, local_file_path)


def make_non_existing_dirs(local_file_path: str):
    """Given a UNIX file path create non existing directories."""
    local_folders = extract_folder_from_file_path(local_file_path)
    logger.info("Creating directories %s.", local_folders)
    os.makedirs(local_folders, exist_ok=True)


def extract_folder_from_file_path(file_path: str) -> str:
    """Given a local UNIX file path extract the directory path."""
    return "/".join(file_path.split("/")[:-1])


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


def save_df_as_jsonl(df: pd.DataFrame, local_file_path: str):
    """Save DataFrame as compressed JSONL."""
    logger.info("Saving locally as json lines to %s.", local_file_path)
    make_non_existing_dirs(local_file_path)
    df.to_json(local_file_path, orient='records', lines=True, compression="gzip")


def upload_output_to_s3(bucket: str, local_file_path: str, s3_file_path: str):
    """Upload a local file to an S3 bucket."""
    logger.info("Uploading %s to %s bucket in S3 with %s key.", local_file_path, bucket, s3_file_path)
    s3 = boto3.client('s3')
    s3.upload_file(local_file_path, bucket, s3_file_path)


if __name__=="__main__":
    main()
