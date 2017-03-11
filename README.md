# primer_library_scanner
Given a file of mature miRNA sequences, determines if corresponding primers are present in primer library file.

## Usage
Given a miRNA primer library file:

| miRNA_name_1   | ACACTCCAGCTGGGTGAGGTAGTAGGTTG |
|:----------|:-------------|
| miRNA_name_2 | ACACTCCAGCTGGGTGAGGTAGTAGGGGC |
| miRNA_name_3 | ACACTCCAGCTGGGTGCGCTAGTAGGTTG |
| miRNA_name_4 | ACACTCCAGCTGGGTGAGGTAATTGGTTG |
| ... | ... |

and a query file with mature miRNA sequences:

| query_miRNA_name_1   | GGGGUUCCUGGGGAUGGGAUUU |
|:----------|:-------------|
| query_miRNA_name_2 | AAGCUGCCAGUUGAAGAACUGU |
| query_miRNA_name_3 | CCACUGCCCCAGGUGCUGCU |
| query_miRNA_name_4 | AGGGACUUUUGGGGGCAGAUGUG |
| ... | ... |

primer_library_scanner outputs two files, matches.csv and no_matches.csv

matches.csv:

| mirName   | mirSeq          | pSeq  | matches  | unique  |
|:----------|:--------------|:---|:---|:---|
| query_miRNA_name_1 | GGGGTTCCTGGGGATGGGATTT | ACACTCCAGCTGGGGGGGTTCCTGGGGAT  | itr-mir-23a  | OK  |
| query_miRNA_name_x | GGGGTTCCTGGGGATGGGATTC | ACACTCCAGCTGGGGGGGTTCCTGGGGAC  | example_primer_x  | NOT UNIQUE  |
| ... | ...     | ...  | ...  | ...  |

no_matches.csv

| mirName   | mirSeq          | pSeq  | matches  |
|----------|--------------|---|---|
| query_miRNA_name_4 | CTATACAATCTACTGTCTTTCC | ACACTCCAGCTGGGCTATACAATCTACTG  |   |

"matches.csv" contains the miRNA and corresponding primers found in the primer library file. If a given primer corresponds to only one query sequence it is 'OK' in the unique column. If it is found 2 or more times it is 'NOT UNIQUE'. If it is NOT UNIQUE it will match multiple miRNA from the query list and therefore will produce multiple products and should not be used.

The no_matches.csv file contains all the miRNA that did not match any of the primers in the library file.
