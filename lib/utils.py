import os
import pandas

class SampleSheetException(Exception):
    pass

class SampleSheet:
    def __init__(self, tsv_file):
        self.data = pandas.read_csv(tsv_file, sep='\t')

    def get_fastq(self, library_id, mate=1):
        if mate != 1:
            raise NotImplementedError('Only mate 1 is currently implemented')
        if library_id not in set(self.data['library_id']):
            raise SampleSheetException(f'{library_id} not in sample sheet')
        fq = self.data[self.data['library_id'] == library_id]['fastq_r1'].iloc[0]
        fq = os.path.abspath(fq)
        return fq

    def get_chip_libraries(self):
        """Get list of all ChIP libraries
        """
        chip = list(self.data[self.data['type'] == 'chip']['library_id'])
        return chip
    
    def get_control_for_chip(self, chip):
        """Get the control library for libray_id `chip`
        """
        ctrl = self.data[self.data['library_id'] == chip]['control_id'].iloc[0]
        if ctrl is None:
            raise SampleSheetException(f'No control found for ChIP library {chip}')
        return ctrl
