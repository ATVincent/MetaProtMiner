# MetaProtMiner
## What is MetaProtMiner ?
MetaProtMiner is a tool to evaluate the occurrence of protein sequences in a dataset composed of sequencing reads.

The DIAMOND tool is required and must be installed on the system (https://github.com/bbuchfink/diamond).
## How to use MetaProtMiner?

```sh
-D File with protein sequences
-L A tabular file with protein information: Name\tFamily\tLength
-1 R1 file
-2 R2 file
-T Threads
-S Name of the sample
-C Minimum % of similarity
-A Minimum % of query cover
-O Output file
```
