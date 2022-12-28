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

## License
MetaProtMiner Copyright (C) 2022 Lucie Galiot, Xavier C. Monger, Antony T. Vincent. This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.