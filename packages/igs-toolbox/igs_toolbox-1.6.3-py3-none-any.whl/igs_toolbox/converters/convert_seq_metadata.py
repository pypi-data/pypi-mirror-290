import json
import logging
import re
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from igs_toolbox.file_utils import read_json_file
from igs_toolbox.formatChecker.seq_metadata_schema import federal_states
from igs_toolbox.log_utils import setup_logging

if sys.version_info >= (3, 10):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import pandas as pd
import typer

if sys.version_info >= (3, 9):
    from zoneinfo import ZoneInfo
else:
    from backports.zoneinfo import ZoneInfo  # type: ignore[import-not-found]


from igs_toolbox.formatChecker import json_checker
from igs_toolbox.formatChecker.seq_metadata_schema import SeqMetadataKeys, ValidationError, seq_metadata_schema
from igs_toolbox.version_utils import version_callback

TIMESTAMP = datetime.now(tz=ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%dT%H-%M-%S")


app = typer.Typer()


def nest_files_and_upload_entries(entry_dict: Dict[str, str]) -> Dict[str, Any]:
    """Move files and uploads entries into list of dicts."""
    # If any file entry exists, add to dict
    entry_dict_out: Dict[str, Any] = entry_dict.copy()
    if any(
        filename in entry_dict for filename in ["file_1_name", "file_1_sha256sum", "file_2_name", "file_2_sha256sum"]
    ):
        entry_dict_out[SeqMetadataKeys.FILES] = []
        for idx in ["1", "2"]:
            file_info = {}
            for field in ["name", "sha256sum"]:
                key = f"file_{idx}_{field}"
                if key in entry_dict_out:
                    file_info.update({f"file_{field}": entry_dict_out[key]})
                    del entry_dict_out[key]
            if len(file_info) > 0:
                entry_dict_out[SeqMetadataKeys.FILES].append(file_info)

    # If any upload entry exists, add to dict
    upload_keys = [
        SeqMetadataKeys.UPLOAD_DATE,
        SeqMetadataKeys.UPLOAD_STATUS,
        SeqMetadataKeys.UPLOAD_SUBMITTER,
        SeqMetadataKeys.REPOSITORY_ID,
        SeqMetadataKeys.REPOSITORY_NAME,
        SeqMetadataKeys.REPOSITORY_LINK,
    ]
    if any(fieldname in entry_dict_out for fieldname in upload_keys):
        entry_dict_out[SeqMetadataKeys.UPLOADS] = [{}]
        for field in upload_keys:
            if field in entry_dict_out:
                entry_dict_out[SeqMetadataKeys.UPLOADS][0].update({field: entry_dict_out[field]})
                del entry_dict_out[field]
    return entry_dict_out


def is_empty_string(value: Any) -> bool:  # noqa: ANN401
    return isinstance(value, str) and not value.strip()


def fix_metadata(metadata_dict: Dict[str, Any], *, schema: Any = seq_metadata_schema) -> None:  # noqa: ANN401, C901, PLR0912
    """Provide simple fixes and conversions."""
    for k in list(metadata_dict.keys()):
        # For string fields
        if isinstance(metadata_dict[k], str):
            # Strip white spaces from string
            metadata_dict[k] = metadata_dict[k].strip()
            # Replacee \n \t and double spaces with one space
            metadata_dict[k] = re.sub(r"\s+", " ", metadata_dict[k])
            # Remove field if (provided, not required and empty) or it is an extra field
            if (len(metadata_dict[k]) == 0 and k not in schema["required"]) or k not in schema["properties"]:
                del metadata_dict[k]

    # Add default HOST Homo sapiens if not provided
    if SeqMetadataKeys.HOST not in metadata_dict or metadata_dict[SeqMetadataKeys.HOST] == "":
        metadata_dict[SeqMetadataKeys.HOST] = "Homo sapiens"

    for prop, cont in schema["properties"].items():
        if prop in metadata_dict:
            # Match fields with valid enum but wrong case and fix it
            if "enum" in cont:
                lower_val = str(metadata_dict[prop]).lower()
                lower_enum = [e.lower() for e in cont["enum"]]
                if lower_val in lower_enum:
                    metadata_dict[prop] = cont["enum"][lower_enum.index(lower_val)]

            # ensure string encoding if required by field
            elif "type" in cont and cont["type"] == "string":
                metadata_dict[prop] = str(metadata_dict[prop])

    # Add DEMIS- prefix to DEMIS_LAB_ID, ensure is a string
    for lab in [SeqMetadataKeys.PRIME_DIAGNOSTIC_LAB_DEMIS_LAB_ID, SeqMetadataKeys.SEQUENCING_LAB_DEMIS_LAB_ID]:
        if lab in metadata_dict:
            lid = str(metadata_dict[lab])
            if len(lid) == 5 and all(v.isdigit() for v in lid):  # noqa: PLR2004
                metadata_dict[lab] = "DEMIS-" + lid

    # Convert federal states code to display name
    for state in [SeqMetadataKeys.PRIME_DIAGNOSTIC_LAB_FEDERAL_STATE, SeqMetadataKeys.SEQUENCING_LAB_FEDERAL_STATE]:
        if state in metadata_dict and metadata_dict[state] in federal_states:
            metadata_dict[state] = federal_states[metadata_dict[state]]


def convert_table_file_to_dicts(input_file: Path) -> List[Dict[str, Any]]:
    """Parse a csv/tsv/xlsx file into a list of IGS-compatible metadata dictionaries."""
    meta_df: pd.DataFrame
    suffix = input_file.suffix
    if suffix.lower() == ".csv":
        meta_df = pd.read_csv(input_file, sep=",", dtype=str)
        # If csv was parsed in one col/row, probably not comma separated, try semicolon
        if meta_df.shape == (
            1,
            1,
        ):
            meta_df = pd.read_csv(input_file, sep=";", dtype=str)
    elif suffix.lower() == ".tsv":
        meta_df = pd.read_csv(input_file, sep="\t", dtype=str)
    elif suffix.lower() == ".xlsx":
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                category=UserWarning,
                message="Data Validation extension is not supported and will be removed",
            )
            meta_df = pd.read_excel(
                input_file,
                dtype=str,  # Cannot use parse dates here because missing optional columns will lead to an error.
            )

    else:
        raise ValueError(
            f"Files of type {suffix} cannot be converted yet. Please provide either a xlsx, csv or tsv file.",
        )

    # Conver cols to lower case
    meta_df.columns = meta_df.columns.str.lower()

    # Remove the time from the datetime if coming from excel
    if suffix.lower() == ".xlsx":
        for date_col in [
            SeqMetadataKeys.DATE_OF_RECEIVING,
            SeqMetadataKeys.DATE_OF_SAMPLING,
            SeqMetadataKeys.DATE_OF_SEQUENCING,
            SeqMetadataKeys.DATE_OF_SUBMISSION,
            SeqMetadataKeys.UPLOAD_DATE,
        ]:
            if date_col in meta_df:
                meta_df[date_col] = meta_df[date_col].str.replace(" 00:00:00", "")

    # Convert to json
    raw_rows: List[Dict[str, str]] = meta_df.to_dict(orient="records")  # type: ignore[assignment]
    metadata_dicts = []
    for row_dict in raw_rows:
        # remove empty strings and NANs
        clean_dict = {key: value for key, value in row_dict.items() if not is_empty_string(value)}
        clean_dict = {key: value for key, value in clean_dict.items() if not pd.isna(value)}

        # transform file and upload entries into nested list
        clean_dict = nest_files_and_upload_entries(clean_dict)

        metadata_dicts.append(clean_dict)
    return metadata_dicts


@app.command(name="convertSeqMetadata", help="Convert table of seq metadata to json files.")
def convert(  # noqa: PLR0913
    input_file: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            dir_okay=False,
            file_okay=True,
            exists=True,
            help="Path to input excel, csv/tsv or json file.",
        ),
    ],
    output: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            dir_okay=True,
            file_okay=False,
            help="Path to output folder for json files.",
        ),
    ],
    strict_mode: Annotated[  # noqa: FBT002
        Optional[bool],
        typer.Option(
            "--strict",
            help="Perform strict validation.",
        ),
    ] = False,
    skip_validation: Annotated[  # noqa: FBT002
        Optional[bool],
        typer.Option(
            "--skip-validation",
            help="Skip all validations, this can generate invalid JSON metadata files.",
        ),
    ] = False,
    fix: Annotated[  # noqa: FBT002
        Optional[bool],
        typer.Option(
            "--fix",
            help="Apply fixes whenever possible.",
        ),
    ] = False,
    log_file: Annotated[
        Path,
        typer.Option("--log_file", "-l", dir_okay=False, help="Path to log file."),
    ] = Path(f"./convertSeqMetadata_{TIMESTAMP}.log"),
    version: Annotated[  # noqa: ARG001
        Optional[bool],
        typer.Option("--version", "-V", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    setup_logging(log_file=log_file, debug=False)

    try:
        if input_file.suffix.lower() == ".json":
            metadata_dicts = read_json_file(input_file, lower_keys=True)
            if not isinstance(metadata_dicts, list):
                metadata_dicts = [metadata_dicts]
        else:
            metadata_dicts = convert_table_file_to_dicts(input_file)
    except ValueError as e:
        logging.error(str(e), exc_info=False)  # noqa: TRY400 (we don't want to log the full traceback)
        raise typer.Abort from None

    # validate and write
    output.mkdir(parents=True, exist_ok=True)
    failed = []
    for idx, metadata_dict in enumerate(metadata_dicts, start=1):
        # fix
        if fix:
            fix_metadata(metadata_dict)
        # validate metadata
        if not skip_validation:
            try:
                json_checker.check_seq_metadata(metadata_dict, strict_mode=strict_mode)  # type: ignore[arg-type]
                sample_id = metadata_dict[SeqMetadataKeys.LAB_SEQUENCE_ID]
            except ValidationError as e:
                failed.append(idx)
                logging.error(f"Invalid data in row {idx}: {e}")  # noqa: TRY400
                continue
        elif metadata_dict.get(SeqMetadataKeys.LAB_SEQUENCE_ID):
            sample_id = metadata_dict[SeqMetadataKeys.LAB_SEQUENCE_ID]
        else:
            sample_id = idx

        # write metadata
        output_file = output / f"{sample_id}_sequencing_metadata.json"
        output_file.write_text(json.dumps(metadata_dict, ensure_ascii=False, indent=4))

    if len(failed):
        logging.error(f"The following rows did not pass validation and were hence not converted: {failed}")
        print(  # noqa: T201
            f"Some rows did not pass validation, "
            f"please consult the log file at {log_file.resolve()} for more information.",
        )
        raise typer.Exit


def main() -> None:
    """Entry point of CLI tool."""
    app()


if __name__ == "__main__":
    main()
