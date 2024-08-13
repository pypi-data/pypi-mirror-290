import subprocess
from pathlib import Path

from aislib.misc_utils import get_logger

logger = get_logger(name=__name__)


def run_prepare_data(final_genotype_data_path: str, output_folder: str) -> Path:
    logger.info("Running data generation pipeline for EIR.")

    command = [
        "plink_pipelines",
        "--raw_data_path",
        final_genotype_data_path,
        "--output_folder",
        output_folder,
        "--output_format",
        "disk",
        "--array_chunk_size",
        "1000",
    ]

    subprocess.run(command, check=True)

    return Path(output_folder, "processed/full_inds/full_chrs/encoded_outputs")
