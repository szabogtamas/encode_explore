#!/usr/bin/env Rscript

############################################################################
#                                                                          #
#   Generate transcript type and boundary stats report based on template   #
#                                                                          #
############################################################################

# Usage: Rscript rcas_template_knitter.R [path_to_template_nb] [path_to_bed_file]
# Optional 3rd argument: sample prefix (in this case not the basename of the file)
# Optional 4th argument: author name to be shown in notebook report

args = commandArgs(trailingOnly=TRUE)

template_path <- args[1]
bed <- args[2]
if (length(args) == 3) {
    bed_base <- args[3]
} else {
    bed_base <- unlist(strsplit(basename(bed), '.', fixed=TRUE))[1]
}
if (length(args) == 4) {
    author_name <- args[4]
} else {
    author_name <- ""
} 

rmarkdown::render(
    template_path,
    output_file = paste(bed_base, "html", sep="."),
    params = list(
        report_author = author_name,
        report_title = paste("Transcript-based read stats for", bed_base, sep=" "),
        genome_annotation = genome_annotation_gtf,
        input_path = bed,
        transcript_table_path = paste(bed_base, "transcripts.csv", sep="_"),
        boundary_table_path = paste(bed_base, "boundaries.csv", sep="_")
    )
)