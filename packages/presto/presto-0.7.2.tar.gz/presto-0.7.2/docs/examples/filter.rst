.. _Filter:

Filtering, Subsetting and Converting
================================================================================

Cleaning or removing poor quality sequences
--------------------------------------------------------------------------------

Data sets can be cleaned using one or more invocations of :ref:`FilterSeq`,
which provides multiple sequence quality control operations.  Four subcommands
remove sequences from the data that fail to meet some threshold: including length,
(:program:`length`), number of N or gap characters (:program:`missing`),
homopolymeric tract length (:program:`repeats`), or mean Phred quality score
(:program:`quality`). Two subcommands modify sequences
without removing them: :program:`trimqual` truncates the sequences when the mean
Phred quality scores decays under a threshold, and :program:`maskqual` replaces
positions with low Phred quality scores with N characters.

:ref:`FilterSeq` provides the following quality control subcommands:

============ =================
Subcommand   Operation
============ =================
length       Removes short sequences
missing      Removes sequences with too many Ns or gaps
repeats      Removes sequences with long homopolymeric tracts
quality      Removes sequences with low mean quality scores
trimqual     Truncates sequences where quality scores decay
maskqual     Masks low quality positions
============ =================

Subsetting sequence files by annotation
--------------------------------------------------------------------------------

The :program:`group` subcommand of :ref:`SplitSeq` allows you to split one file
into multiple files based on the values in a sequence annotation. For example,
splitting one file with multiple ``SAMPLE`` annotations into separate files
(one for each sample) would be accomplished by::

    SplitSeq.py group -s reads.fastq -f SAMPLE

which will create a set of files labelled ``SAMPLE-M1`` and ``SAMPLE-M2`` if samples are
named ``M1`` and ``M2``.

If you wanted to split based on a numeric value, rather than a set of categorical values,
then you would add the :option:`--num <SplitSeq group --num>` argument. :ref:`SplitSeq`
would then create two files: one containing sequences with values less than the threshold
specified by the :option:`--num <SplitSeq group --num>` argument and one file containing
sequences with values greater than or equal to the threshold::

    SplitSeq.py group -s reads.fastq -f DUPCOUNT --num 2

which will create two files with the labels ``atleast-2`` and ``under-2``.

.. _Filter-RandomSampling:

Random sampling from sequence files
--------------------------------------------------------------------------------

The :program:`sample` subcommand of :ref:`SplitSeq` may be used to generate a
random sample from a sequence file or set of pair-end files. The example below
will select a random sample of 1,000 sequences (:option:`-n 1000 <SplitSeq sample -n>`)
which all contain the annotation ``SAMPLE=M1``
(:option:`-f SAMPLE <SplitSeq sample -f>` and :option:`-u M1 <SplitSeq sample -u>`)::

    SplitSeq.py sample -s reads.fastq -f SAMPLE -u M1 -n 1000

Performing an analogous sampling of Illumina paired-end reads would be accomplished using
the :program:`samplepair` subcommand::

    SplitSeq.py samplepair -s reads.fastq -f SAMPLE -u M1 -n 1000 --coord illumina

.. note::

    Both the :option:`-f <SplitSeq sample -f>` and :option:`-n <SplitSeq sample -n>`
    arguments will accept a list of values (eg, ``-n 1000 100 10``), allowing you to
    sample multiple times from multiple files in one command.

Converting to FASTA for IMGT/HighV-QUEST or IgBLAST
--------------------------------------------------------------------------------

`IMGT/HighV-QUEST <http://imgt.org/HighV-QUEST>`__ and `IgBLAST <http://ncbi.github.io/igblast>`__
both require sequences in FASTA format. You can use the Immcantation script `fastq2fasta.py` to
convert `.fastq` to `.fasta`. The script is available from the
`repository <http://bitbucket.org/kleinstein/immcantation/src/master/scripts/fastq2fasta.py>`__
and is pre-installed in the Docker container.

.. code-block:: none

    fastq2fasta.py reads.fastq

Alternatively, you can request :ref:`SplitSeq.py` to output FASTA files by using
the flag :option:`--fasta`. In the example workflows, a common last step
in the data processing pipelines is filtering sequences with at least two
representative reads. By adding :option:`--fasta` to the command, the output
file will be a `.fasta` file.

.. code-block:: none

    SplitSeq.py group -s reads.fastq -f DUPCOUNT --num 2 --fasta


Reducing file size for submission to IMGT/HighV-QUEST
--------------------------------------------------------------------------------

`IMGT/HighV-QUEST <http://imgt.org/HighV-QUEST>`__ currently limits the size of
uploaded files to 500,000 sequences. To accomodate this limit, you can use
the :program:`count` subcommand of :ref:`SplitSeq` to divide your files into
small pieces.

.. code-block:: none

    SplitSeq.py count -s reads.fastq -n 500000 --fasta

The :option:`-n 500000 <SplitSeq count -n>` argument sets the maximum number of
sequences in each file and the :option:`--fasta <SplitSeq count --fasta>`
tells the tool to output a FASTA, rather than FASTQ, formatted file.

.. note::

    You can usually avoid the necessity of reducing file sizes by removing
    duplicate sequences first using the :ref:`CollapseSeq` tool.
