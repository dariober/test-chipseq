#!/usr/bin/env python3

import unittest
import sys
import shutil
import os
import subprocess as sp

from importlib.machinery import SourceFileLoader

utils = SourceFileLoader("utils.py", "lib/utils.py").load_module()


class Utils(unittest.TestCase):
    def setUp(self):
        sys.stderr.write("\n" + self.id().split(".")[-1] + " ")  # Print test name
        if os.path.exists("test_out"):
            shutil.rmtree("test_out")
        os.mkdir("test_out")

    def tearDown(self):
        if os.path.exists("test_out"):
            shutil.rmtree("test_out")

    def testCanGetFastqRead1(self):
        ss = utils.SampleSheet("test/data/sample_sheet.tsv")
        r1 = ss.get_fastq("smp1")
        self.assertTrue("test/data/smp1_R1.fastq.gz" in r1)

    def testCanGetChipLibrariesFromSampleSheet(self):
        ss = utils.SampleSheet("test/data/sample_sheet.tsv")
        chip = ss.chip_libraries
        self.assertEqual(len(chip), 2)
        self.assertTrue("smp1" in chip)
        self.assertTrue("smp2" in chip)

    def testCanGetControlLibrary(self):
        ss = utils.SampleSheet("test/data/sample_sheet.tsv")
        ctrl = ss.get_control_for_chip("smp1")
        self.assertEqual(ctrl, "ctrl1")

    def testCanExecuteTestRun(self):
        cmd = r"""
        snakemake -p -j 1 -d test_out \
           -C sample_sheet=$PWD/test/data/sample_sheet.tsv \
              genome=$PWD/test/data/genome.fa
        """
        p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        stdout, stderr = p.communicate()
        self.assertTrue(p.returncode == 0)
        self.assertTrue(os.path.isfile("test_out/macs/smp2_peaks.narrowPeak"))


if __name__ == "__main__":
    unittest.main()
