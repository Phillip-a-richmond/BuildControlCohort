# Build Control Cohort
> This repo is for building a control set of data for WGS and RNAseq in human.

## Overview
I'll use data sources from IGSR for WGS (thousand genomes GRCh38) and RNAseq (Geuvadis). The WGS is already mapped and is in CRAM, so I'll just use that natively. The RNAseq needs to be mapped and I'll be grabbing fastqs.


## Workflow

Info for merging Thousand Genomes and Geuvadis TSVs and making a download script

1. Data sheets downloaded from IGSR.

Geuvadis CSV:
https://www.internationalgenome.org/api/beta/file/_search/igsr_Geuvadis.tsv
Note, had to copy this since the wget didn't play nicely.


THousand Genomes
https://www.internationalgenome.org/api/beta/file/_search/igsr_30x%20GRCh38.tsv.tsv


2. Cut out only mRNA from Geuvadis, and sort by filename (so that _1 and _2 are adjacent)

```
grep "mRNA" igsr_Geuvadis.tsv | sort -k1V - > igsr_Geuvadis_Subset.tsv
```

3. Run the join python script
```
python JoinTSVs.py -1 ThousandGenomes.tsv -2 igsr_Geuvadis_mRNA.tsv -O Merged.tsv -B DownloadMerged.sh 
```

