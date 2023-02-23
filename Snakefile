from lib import utils

ss = utils.SampleSheet(config["sample_sheet"])


rule all:
    input:
        expand("macs/{library_id}_peaks.narrowPeak", library_id=ss.chip_libraries),


rule bwa_index:
    input:
        genome=config["genome"],
    output:
        genome=config["genome"] + ".bwt",
    shell:
        r"""
        bwa index {input.genome}
        """


rule bwa:
    input:
        idx=config["genome"] + ".bwt",
        r1=lambda wc: ss.get_fastq(wc.library_id),
    output:
        bam="bwa/{library_id}.bam",
    params:
        genome=lambda wc, input: re.sub("\.bwt$", "", input.idx),
    shell:
        r"""
        bwa mem {params.genome} {input.r1} \
        | samtools sort > {output.bam}
        """


rule macs2:
    input:
        chip="bwa/{library_id}.bam",
        ctrl=lambda wc: "bwa/%s.bam" % ss.get_control_for_chip(wc.library_id),
    output:
        np="macs/{library_id}_peaks.narrowPeak",
    params:
        name=lambda wc, output: re.sub("_peaks\.narrowPeak$", "", output.np),
    shell:
        r"""
        macs2 callpeak --nomodel -t {input.chip} -c {input.ctrl} \
            -n {params.name}
        """
