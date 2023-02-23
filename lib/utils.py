import os
import pandas

LIBRARY_TYPES = ["chip", "input"]


class SampleSheetException(Exception):
    pass


class SampleSheet:
    def __init__(self, tsv_file):
        self.data = self._get_data(tsv_file)
        self.chip_libraries = self._get_chip_libraries()

    def get_fastq(self, library_id, mate=1):
        """Get fastq file associated to this library_id"""
        if mate != 1:
            raise NotImplementedError("Only mate 1 is currently implemented")
        if library_id not in set(self.data["library_id"]):
            raise SampleSheetException(f"{library_id} not in sample sheet")
        fq = self.data[self.data["library_id"] == library_id]["fastq_r1"].iloc[0]
        fq = os.path.abspath(fq)
        return fq

    def get_control_for_chip(self, library_id):
        """Get the control library for this library_id."""
        ctrl = self.data[self.data["library_id"] == library_id]["control_id"].iloc[0]
        if ctrl is None:
            raise SampleSheetException(
                f"No control found for ChIP library {library_id}"
            )
        return ctrl

    def _get_data(self, tsv_file):
        data = pandas.read_csv(tsv_file, sep="\t")
        # Some sanity checks
        if len(data["library_id"]) != len(set(data["library_id"])):
            raise SampleSheetException("Duplicate library IDs found")
        if len([x for x in data["type"] if x not in LIBRARY_TYPES]) != 0:
            raise SampleSheetException(f"Type must be one of {LIBRARY_TYPES}")
        return data

    def _get_chip_libraries(self):
        """Get list of all ChIP libraries."""
        chip = list(self.data[self.data["type"] == "chip"]["library_id"])
        return chip
