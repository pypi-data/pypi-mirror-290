from typing import Any, Dict, List


class ValidationError(Exception):
    def __init__(self, error_messages: List[str]) -> None:
        super().__init__(
            "\n".join(
                [
                    f"Validation failed ({len(error_messages)} issues)",
                    *[f"- {message}" for message in error_messages],
                ],
            ),
        )
        self.error_messages = error_messages


class SeqMetadataKeys:
    MELDETATBESTAND = "meldetatbestand"
    SPECIES = "species"
    LAB_SEQUENCE_ID = "lab_sequence_id"
    DEMIS_NOTIFICATION_ID = "demis_notification_id"
    STATUS = "status"
    VERSION = "version"
    IGS_ID = "igs_id"
    DATE_OF_RECEIVING = "date_of_receiving"
    DATE_OF_SAMPLING = "date_of_sampling"
    DATE_OF_SEQUENCING = "date_of_sequencing"
    DATE_OF_SUBMISSION = "date_of_submission"
    DATE_OF_DELETION = "date_of_deletion"
    SEQUENCING_INSTRUMENT = "sequencing_instrument"
    SEQUENCING_PLATFORM = "sequencing_platform"
    ADAPTER = "adapter"
    SEQUENCING_STRATEGY = "sequencing_strategy"
    ISOLATION_SOURCE = "isolation_source"
    HOST = "host"
    HOST_SEX = "host_sex"
    HOST_BIRTH_MONTH = "host_birth_month"
    HOST_BIRTH_YEAR = "host_birth_year"
    SEQUENCING_REASON = "sequencing_reason"
    GEOGRAPHIC_LOCATION = "geographic_location"
    ISOLATE = "isolate"
    AUTHOR = "author"
    NAME_AMP_PROTOCOL = "name_amp_protocol"
    PRIMER_SCHEME = "primer_scheme"
    METADATA_QC = "metadata_qc"
    METADATA_QC_REASON = "metadata_qc_reason"
    PRIME_DIAGNOSTIC_LAB_DEMIS_LAB_ID = "prime_diagnostic_lab.demis_lab_id"
    PRIME_DIAGNOSTIC_LAB_NAME = "prime_diagnostic_lab.name"
    PRIME_DIAGNOSTIC_LAB_ADDRESS = "prime_diagnostic_lab.address"
    PRIME_DIAGNOSTIC_LAB_POSTAL_CODE = "prime_diagnostic_lab.postal_code"
    PRIME_DIAGNOSTIC_LAB_FEDERAL_STATE = "prime_diagnostic_lab.federal_state"
    SEQUENCING_LAB_DEMIS_LAB_ID = "sequencing_lab.demis_lab_id"
    SEQUENCING_LAB_NAME = "sequencing_lab.name"
    SEQUENCING_LAB_ADDRESS = "sequencing_lab.address"
    SEQUENCING_LAB_POSTAL_CODE = "sequencing_lab.postal_code"
    SEQUENCING_LAB_FEDERAL_STATE = "sequencing_lab.federal_state"
    UPLOADS = "uploads"
    REPOSITORY_NAME = "repository_name"
    REPOSITORY_LINK = "repository_link"
    REPOSITORY_ID = "repository_id"
    UPLOAD_DATE = "upload_date"
    UPLOAD_STATUS = "upload_status"
    UPLOAD_SUBMITTER = "upload_submitter"
    FILES = "files"
    FILE_NAME = "file_name"
    FILE_SHA256SUM = "file_sha256sum"


# Code and display from https://simplifier.net/packages/de.basisprofil.r4/1.4.0/files/656722
federal_states = {
    "DE-BW": "Baden-Württemberg",
    "DE-BY": "Bayern",
    "DE-BE": "Berlin",
    "DE-BB": "Brandenburg",
    "DE-HB": "Bremen",
    "DE-HH": "Hamburg",
    "DE-HE": "Hessen",
    "DE-MV": "Mecklenburg-Vorpommern",
    "DE-NI": "Niedersachsen",
    "DE-NW": "Nordrhein-Westfalen",
    "DE-RP": "Rheinland-Pfalz",
    "DE-SL": "Saarland",
    "DE-SN": "Sachsen",
    "DE-ST": "Sachsen-Anhalt",
    "DE-SH": "Schleswig-Holstein",
    "DE-TH": "Thüringen",
}

seq_metadata_schema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        SeqMetadataKeys.MELDETATBESTAND: {
            "enum": [
                "EHCP",
                "LISP",
                "SALP",
                "STYP",
                "INVP",
                "NEIP",
                "MSVP",
                "MYTP",
                "CVDP",
                "HIVP",
                "NEGP",
                "EBCP",
                "ACBP",
                "CDFP",
                "MRAP",
                "SALP",
                "HEVP",
                "HAVP",
                "LEGP",
                "SPNP",
                "WNVP",
            ],
        },
        SeqMetadataKeys.SPECIES: {
            "type": "string",
            "minLength": 1,
        },
        SeqMetadataKeys.LAB_SEQUENCE_ID: {
            "type": "string",
            "pattern": "^[A-Za-z0-9-_]+$",
        },
        SeqMetadataKeys.DEMIS_NOTIFICATION_ID: {
            "type": "string",
            "minLength": 1,
        },
        SeqMetadataKeys.STATUS: {"enum": ["preliminary", "amended", "final", ""]},
        SeqMetadataKeys.VERSION: {"$ref": "#/$defs/int"},
        SeqMetadataKeys.IGS_ID: {
            "type": "string",
            "pattern": (
                "^(IMS|IGS)-[0-9]{5}-[A-Z]{3}P-"
                "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
                "|"
                "^(IMS|IGS)-[0-9]{5}-[A-Z]{3}P-[0-9]{2,6}$"  # for migration of old sequences
            ),
        },
        SeqMetadataKeys.DATE_OF_RECEIVING: {"$ref": "#/$defs/date-datetime"},
        SeqMetadataKeys.DATE_OF_SAMPLING: {"$ref": "#/$defs/date-datetime"},
        SeqMetadataKeys.DATE_OF_SEQUENCING: {"$ref": "#/$defs/date-datetime"},
        SeqMetadataKeys.DATE_OF_SUBMISSION: {"$ref": "#/$defs/date-datetime"},
        SeqMetadataKeys.DATE_OF_DELETION: {"$ref": "#/$defs/date-datetime"},
        SeqMetadataKeys.SEQUENCING_INSTRUMENT: {
            "enum": [
                "454_GS",
                "454_GS_20",
                "454_GS_FLX",
                "454_GS_FLX+",
                "454_GS_FLX_Titanium",
                "454_GS_Junior",
                "HiSeq_X_Five",
                "HiSeq_X_Ten",
                "Illumina_Genome_Analyzer",
                "Illumina_Genome_Analyzer_II",
                "Illumina_Genome_Analyzer_IIx",
                "Illumina_HiScanSQ",
                "Illumina_HiSeq_1000",
                "Illumina_HiSeq_1500",
                "Illumina_HiSeq_2000",
                "Illumina_HiSeq_2500",
                "Illumina_HiSeq_3000",
                "Illumina_HiSeq_4000",
                "Illumina_iSeq_100",
                "Illumina_MiSeq",
                "Illumina_MiniSeq",
                "Illumina_NovaSeq_6000",
                "NextSeq_500",
                "NextSeq_550",
                "PacBio_RS",
                "PacBio_RS_II",
                "Sequel",
                "Ion_Torrent_PGM",
                "Ion_Torrent_Proton",
                "Ion_Torrent_S5",
                "Ion_Torrent_S5_XL",
                "AB_3730xL_Genetic_Analyzer",
                "AB_3730_Genetic_Analyzer",
                "AB_3500xL_Genetic_Analyzer",
                "AB_3500_Genetic_Analyzer",
                "AB_3130xL_Genetic_Analyzer",
                "AB_3130_Genetic_Analyzer",
                "AB_310_Genetic_Analyzer",
                "MinION",
                "GridION",
                "PromethION",
                "BGISEQ-500",
                "DNBSEQ-T7",
                "DNBSEQ-G400",
                "DNBSEQ-G50",
                "DNBSEQ-G400_FAST",
                "Illumina_NextSeq_1000",
                "Illumina_NextSeq_2000",
                "Illumina_NovaSeq_X",
                "Illumina_NovaSeq_X_PLUS",
                "Sequel_II",
                "Sequel_IIe",
                "Flongle",
                "DNBSEQ-T10",
                "DNBSEQ-T20",
                "DNBSEQ-G99",
                "Ion_Torrent_Genexus",
                "Onso",
                "Revio",
                "UG_100",
                "G4",
                "PX",
                "unspecified",
            ],
        },
        SeqMetadataKeys.SEQUENCING_PLATFORM: {
            "enum": [
                "LS454",
                "ILLUMINA",
                "PACBIO_SMRT",
                "ION_TORRENT",
                "CAPILLARY",
                "OXFORD_NANOPORE",
                "BGISEQ",
                "DNBSEQ",
                "OTHER",
            ],
        },
        SeqMetadataKeys.ADAPTER: {
            "type": "string",
            "pattern": "^[\\+a-zA-Z0-9_ ,-]+$",
        },
        SeqMetadataKeys.SEQUENCING_STRATEGY: {
            "enum": [
                "WGS",
                "WGA",
                "WXS",
                "RNA-Seq",
                "ssRNA-seq",
                "miRNA-Seq",
                "ncRNA-Seq",
                "FL-cDNA",
                "EST",
                "Hi-C",
                "ATAC-seq",
                "WCS",
                "RAD-Seq",
                "CLONE",
                "POOLCLONE",
                "AMPLICON",
                "CLONEEND",
                "FINISHING",
                "ChIP-Seq",
                "MNase-Seq",
                "DNase-Hypersensitivity",
                "Bisulfite-Seq",
                "CTS",
                "MRE-Seq",
                "MeDIP-Seq",
                "MBD-Seq",
                "Tn-Seq",
                "VALIDATION",
                "FAIRE-seq",
                "SELEX",
                "RIP-Seq",
                "ChIA-PET",
                "Synthetic-Long-Read",
                "Targeted-Capture",
                "Tethered Chromatin Conformation Capture",
                "OTHER",
            ],
        },
        SeqMetadataKeys.ISOLATION_SOURCE: {
            "type": "string",
            "minLength": 1,
        },
        SeqMetadataKeys.HOST: {"enum": ["Homo sapiens"]},
        SeqMetadataKeys.HOST_SEX: {"enum": ["unknown", "other", "female", "male"]},
        SeqMetadataKeys.HOST_BIRTH_MONTH: {
            "type": "string",
            "pattern": "^(0?[1-9]|1[012])$",
        },
        SeqMetadataKeys.HOST_BIRTH_YEAR: {
            "type": "string",
            "pattern": "^\\d{4}$",
        },
        SeqMetadataKeys.SEQUENCING_REASON: {"enum": ["random", "requested", "other", "clinical"]},
        SeqMetadataKeys.GEOGRAPHIC_LOCATION: {
            "type": "string",
            "pattern": "^[0-9]{3}$",
        },
        SeqMetadataKeys.ISOLATE: {
            "type": "string",
        },
        SeqMetadataKeys.AUTHOR: {
            "type": "string",
            "minLength": 1,
        },
        SeqMetadataKeys.NAME_AMP_PROTOCOL: {
            "type": "string",
            "pattern": "^[a-zA-Z0-9_ ,-]+$",
        },
        SeqMetadataKeys.PRIME_DIAGNOSTIC_LAB_DEMIS_LAB_ID: {
            "type": "string",
            "pattern": "^DEMIS-[0-9]{5}$",
        },
        SeqMetadataKeys.PRIME_DIAGNOSTIC_LAB_NAME: {
            "type": "string",
            "pattern": "^[a-zA-Z0-9_ ,-äöüÄÖÜß]+$",
        },
        SeqMetadataKeys.PRIME_DIAGNOSTIC_LAB_ADDRESS: {
            "type": "string",
        },
        SeqMetadataKeys.PRIME_DIAGNOSTIC_LAB_POSTAL_CODE: {
            "type": "string",
            "pattern": "^[0-9]{5}$",
        },
        SeqMetadataKeys.PRIME_DIAGNOSTIC_LAB_FEDERAL_STATE: {"$ref": "#/$defs/federalStates"},
        SeqMetadataKeys.PRIMER_SCHEME: {
            "type": "string",
            "pattern": "^[a-zA-Z0-9_ ,-\\.]+$",
        },
        SeqMetadataKeys.METADATA_QC: {
            "$ref": "#/$defs/bool",
        },
        SeqMetadataKeys.METADATA_QC_REASON: {
            "type": "string",
            "pattern": "^([a-zA-Z0-9_:-]|; (?!$))+$",
        },
        SeqMetadataKeys.SEQUENCING_LAB_DEMIS_LAB_ID: {
            "type": "string",
            "pattern": "^DEMIS-[0-9]{5}$",
        },
        SeqMetadataKeys.SEQUENCING_LAB_NAME: {
            "type": "string",
            "pattern": "^[a-zA-Z0-9_ ,-äöüÄÖÜß]+$",
        },
        SeqMetadataKeys.SEQUENCING_LAB_ADDRESS: {
            "type": "string",
            "minLength": 1,
        },
        SeqMetadataKeys.SEQUENCING_LAB_POSTAL_CODE: {
            "type": "string",
            "pattern": "^[0-9]{5}$",
        },
        SeqMetadataKeys.SEQUENCING_LAB_FEDERAL_STATE: {"$ref": "#/$defs/federalStates"},
        SeqMetadataKeys.UPLOADS: {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    SeqMetadataKeys.REPOSITORY_NAME: {"enum": ["GISAID", "ENA", "SRA", "PubMLST", "GenBank", "Other"]},
                    SeqMetadataKeys.REPOSITORY_LINK: {"type": "string"},
                    SeqMetadataKeys.REPOSITORY_ID: {"type": "string"},
                    SeqMetadataKeys.UPLOAD_DATE: {"$ref": "#/$defs/date-datetime"},
                    SeqMetadataKeys.UPLOAD_STATUS: {"enum": ["Accepted", "Planned", "Denied", "Other"]},
                    SeqMetadataKeys.UPLOAD_SUBMITTER: {"type": "string"},
                },
                "additionalProperties": False,
                "required": [
                    SeqMetadataKeys.REPOSITORY_NAME,
                    SeqMetadataKeys.REPOSITORY_ID,
                    SeqMetadataKeys.UPLOAD_STATUS,
                ],
            },
        },
        SeqMetadataKeys.FILES: {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    SeqMetadataKeys.FILE_NAME: {
                        "type": "string",
                        "pattern": "^[a-zA-Z0-9_-]+\\.(fasta|fa|fastq|fq)(\\.gz)?$",
                    },
                    SeqMetadataKeys.FILE_SHA256SUM: {
                        "type": "string",
                        "pattern": "^[A-Fa-f0-9]{64}$",
                    },
                },
                "required": [SeqMetadataKeys.FILE_NAME, SeqMetadataKeys.FILE_SHA256SUM],
                "additionalProperties": False,
            },
            "minItems": 1,
            "uniqueItems": True,
        },
    },
    "$defs": {
        "bool": {
            "type": "string",
            "pattern": "^(true)|(false)$",
        },
        "int": {
            "type": "string",
            "pattern": "^-?[0-9]+$",
        },
        "date": {
            "type": "string",
            "format": "date",
        },
        "date-datetime": {
            "type": "string",
            "anyOf": [
                {"format": "date-time"},
                {"format": "date"},
            ],
        },
        "federalStates": {
            "enum": list(federal_states.values()),
        },
    },
    "required": [
        SeqMetadataKeys.MELDETATBESTAND,
        SeqMetadataKeys.LAB_SEQUENCE_ID,
        SeqMetadataKeys.DATE_OF_SUBMISSION,
        SeqMetadataKeys.SEQUENCING_INSTRUMENT,
        SeqMetadataKeys.SEQUENCING_PLATFORM,
        SeqMetadataKeys.HOST,
        SeqMetadataKeys.SEQUENCING_REASON,
        SeqMetadataKeys.SEQUENCING_LAB_DEMIS_LAB_ID,
    ],
}


def loose_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    new_schema = schema.copy()
    # Allows extra fields to the schema
    new_schema["additionalProperties"] = True
    # Remove requirement for HOST
    if SeqMetadataKeys.HOST in new_schema["required"]:
        new_schema["required"].remove(SeqMetadataKeys.HOST)
    # Accept code in addition to display for deferal states
    new_schema["$defs"]["federalStates"]["enum"].extend(list(federal_states.keys()))
    # Accept DEMIS_LAB_ID without prefix "DEMIS-"
    for lab in [SeqMetadataKeys.PRIME_DIAGNOSTIC_LAB_DEMIS_LAB_ID, SeqMetadataKeys.SEQUENCING_LAB_DEMIS_LAB_ID]:
        new_schema["properties"][lab]["pattern"] = "^DEMIS-[0-9]{5}$|^[0-9]{5}$"

    return new_schema
