from collections import Counter, defaultdict
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Iterable


@dataclass
class AssemblyInfo:
    gc: float
    n50: int
    n_contigs: int
    min_contig_length: int
    length: int
    single_base_content: float
    double_base_content: float
    triple_base_content: float
    n_content: float
    gap_content: float
    ambiguous_content: float
    non_acgt_content: float

    def __post_init__(self):
        for field in fields(self):
            field_value = field.type(getattr(self, field.name))
            setattr(
                self,
                field.name,
                round(field_value, 4) if field.type == float else field_value,
            )


def SimpleFastaParser(handle):
    """
    This method is a duplicate of biopython Bio.SeqIO.FastaIO.SimpleFastaParser
    We've copied it to avoid being dependant on biopython within the lib

    """
    # Skip any text before the first record (e.g. blank lines, comments)
    for line in handle:
        if line[0] == ">":
            title = line[1:].rstrip()
            break
    else:
        # no break encountered - probably an empty file
        return

    # Main logic
    # Note, remove trailing whitespace, and any internal spaces
    # (and any embedded \r which are possible in mangled files
    # when not opened in universal read lines mode)
    lines = []
    for line in handle:
        if line[0] == ">":
            yield title, "".join(lines).replace(" ", "").replace("\r", "")
            lines = []
            title = line[1:].rstrip()
            continue
        lines.append(line.rstrip())

    yield title, "".join(lines).replace(" ", "").replace("\r", "")


def add_base_counts(seq: str, total_base_counts: dict[str, int]) -> None:
    """Counts bases in a sequence and adds them to the input dictionary"""
    for base, counts in Counter(seq.upper()).items():
        total_base_counts[base] += counts


def get_sum_of_base_counts(
    total_base_counts: dict[str, int], bases: Iterable[str]
) -> int:
    """Gets the sum of counts for specific bases in a dictionary where `total_base_counts[base] = counts`"""
    return sum(total_base_counts[base] for base in bases)


def get_length_metrics(lengths: list[int]) -> tuple[int, int, int]:
    """
    Iterates over all sequence lengths and calculates length metrics:
    returns `total_length, min_contig_length, n50`
    """
    sorted_lengths = sorted(lengths, reverse=True)

    total_length: int = sum(lengths)
    min_contig_length: int = sorted_lengths[-1] if sorted_lengths else 0
    n50: int = 0

    half_length: float = total_length / 2
    cumulated_length = 0
    for length in sorted_lengths:
        cumulated_length += length
        if cumulated_length >= half_length:
            n50 = length
            break
    return total_length, min_contig_length, n50


def compute_metrics(fasta: Path) -> AssemblyInfo:
    """
    Computes: GC content, ambiguous base contents, gap content, n50, number of contigs, assembly length
    """
    total_base_counts = defaultdict(int)
    number_of_contigs = 0
    lengths: list[int] = []
    with open(fasta, encoding="utf-8") as reader:
        for _, seq in SimpleFastaParser(reader):
            lengths.append(len(seq))
            add_base_counts(seq, total_base_counts)
            number_of_contigs += 1
    gc_count = get_sum_of_base_counts(total_base_counts, "GC")
    single_base_count = gc_count + get_sum_of_base_counts(total_base_counts, "AT")
    double_bases_count = get_sum_of_base_counts(total_base_counts, "RYSWKM")
    triple_bases_count = get_sum_of_base_counts(total_base_counts, "BDHV")
    ambiguous_count = double_bases_count + triple_bases_count + total_base_counts["N"]
    total_length, min_contig_length, n50 = get_length_metrics(lengths)

    return AssemblyInfo(
        gc=(gc_count / total_length if total_length else 0),
        n50=n50,
        n_contigs=number_of_contigs,
        min_contig_length=min_contig_length,
        length=total_length,
        single_base_content=(single_base_count / total_length if total_length else 0),
        double_base_content=(double_bases_count / total_length if total_length else 0),
        triple_base_content=(triple_bases_count / total_length if total_length else 0),
        n_content=(total_base_counts["N"] / total_length if total_length else 0),
        gap_content=(total_base_counts["-"] / total_length if total_length else 0),
        ambiguous_content=(ambiguous_count / total_length if total_length else 0),
        non_acgt_content=(
            1 - (single_base_count / total_length) if total_length else 0
        ),
    )
