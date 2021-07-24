#!/usr/bin/env Rscript

############################################################################
#                                                                          #
# Calculate the ration of UTR vs. non-UTR overlapping reads for each gene  #
#                                                                          #
############################################################################

# Usage: Rscript utr_exon_ratio_calculator.R [path_to_bed_file] [path_to_gtf] [path_to_output]

args = commandArgs(trailingOnly=TRUE)

bed <- args[1]
annotation_gtf <- args[2]
output_path <- args[3]

library(dplyr)
library(tidyr)
library(tibble)
library(RCAS)
library(GenomicRanges)
library(GenomicFeatures)

### Download annotation if not loacl file

remove_gtf <- FALSE
genome_annotation_gtf <- annotation_gtf
if (substr(annotation_gtf, 1, 5) == "s3://") {
  genome_annotation_gtf <- "genome_annotation.gtf.gz"
  remove_gtf <- TRUE
  system(
    paste(
      "aws s3 cp", annotation_gtf,
      genome_annotation_gtf, "--no-sign-request", sep=" "
    ),
    intern=FALSE
  )
}

### Parse genome annotation

genome_range_features <- importGtf(genome_annotation_gtf)
if (remove_gtf) unlink(genome_annotation_gtf)
cat("Genome annotation parsed.\n")

### Annotate samples BED file
transcript_info <- bed %>%
  importBed() %>%
  queryGff(queryRegions=., gffData=genome_range_features) %>%
  data.frame() %>%
  dplyr::distinct(
    gene_id, gene_name, gene_type, transcript_type, type, query_name, query_score,
    width
  )

cat("Retrieved anotations for bed file.\n")

### Calculate ratio of UTR to exon reads
trx_type_tab <- transcript_info %>%
  dplyr::distinct(gene_name, query_name, type, .keep_all=TRUE) %>%
  dplyr::filter(type %in% c("exon", "UTR")) %>%
  dplyr::count(gene_name, type) %>%
  pivot_wider(names_from=type, values_from=n, values_fill=0) %>%
  mutate(
    utr_to_exon = UTR / exon
  )

write.csv(trx_type_tab, output_path, row.names=FALSE)