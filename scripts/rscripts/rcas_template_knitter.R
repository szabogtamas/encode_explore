#!/usr/bin/env Rscript

############################################################################
#                                                                          #
#   Generate transcript type and boundary stats report based on template   #
#                                                                          #
############################################################################

# Usage: Rscript rcas_template_knitter.R [path_to_template_nb] [path_to_bed_file]

args = commandArgs(trailingOnly=TRUE)

template_path <- args[1]
bed <- args[2]

bed_base <- unlist(strsplit(basename(bed_inputs[1]), '.', fixed=TRUE))[1]

rmarkdown::render(
    template_path,
    output_file = paste(bed_base, "html", sep="."),
    params = list(
        report_author = "",
        report_title = paste("Transcript-based read stats for", bed_base, sep=" "),
        genome_annotation = genome_annotation_gtf,
        input_path = bed,
        transcript_table_path = paste(bed_base, "transcripts.csv", sep="_"),
        boundary_table_path = paste(bed_base, "boundaries.csv", sep="_")
    )
)