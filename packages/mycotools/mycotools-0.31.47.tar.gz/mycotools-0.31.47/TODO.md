- [ ] Conserved log class
    - [ ] Must be capable of determining if the run is congruent or new
- [ ] Annotate code (all)
    - [ ] add type constraints to functions
- [ ] Conform old scripts to PEP8 (all)
- [o] Build all-in-one stable conda package
- [ ] Transition code-base to Rust
- [ ] implement kon_log class, paying attention to verbosity control
- [ ] kon_log class output to local configuration directory
- [ ] support compressed databases
- [ ] register mycotools with NCBI
- [ ] configuration to output mtdb name + date in output directory
- [ ] discuss multigene phylo pipeline
- [x] discuss db2hgs
- [ ] uniform argument parser
- [ ] allow for inputting multiple DBs with full paths

### crap
- [ ] *Outgroup manager for clusters that fit within min and maximum sequences*
- [ ] Percent positives filter
- [ ] Integrate agglomerative clustering
- [ ] Allow for inputing a specific run order
- [ ] Log-based resume
- [ ] Do not reiterate running a gene in the same homology group
- [ ] Allow converting HG runs' names
- [ ] *Better root inference*
- [ ] Assembly query method, i.e. through tblastn
- [ ] Allow changing the clustering variable
- [x] locus output using percent similarity

### curGFF3
- [ ] pseudogenes can have RNAs, and CDSs from NCBI may reference those
  pseudogene parents or their RNAs (GCA_900074715.1_LAME0)
- [ ] some pseudogenes fail because they are given an "Alias" without being
  completed (GCA_004920355.1)
- [ ] make universal interface to remove need for source column
- [ ] allow including entries that cannot be hiearchically assimilated into
  genes or transcripts
- [ ] build to universally include genes and transcript-assimilated types

### db2hgs
- [ ] implement db2search to identify NSCHGs best-hits 
- [ ] implement an automated NSCHG extraction based on minimum gene #

### db2microsyntree
- [ ] Allow log removal

### db2search
- [ ] Distinguish between nt and aa mmseqs dbs
- [ ] Allow for blastdb construction
- [ ] Streamline mmseqs parsing
- [ ] mmseqs save db option
- [ ] profile mmseqs search
- [ ] concatenate mmseqs query dbs
- [ ] optional fail upon any failures
- [ ] Log hmmer runs
- [ ] *nhmmer option*
- [ ] create all outputs as temp files and move when complete
- [ ] extract covered portion of hits
- [ ] max hits post blast compilation
- [ ] hsp option

### dbtools
- [ ] Vectorize MTDB class
- [ ] make mtdb compiled class
- [ ] remove Entrez email login, simplify API access
- [ ] Get taxonomy of non-genus names
- [ ] get taxonomy XML - if it exists - instead of independent queries

### extract_mtdb
- [ ] allow for a lineage list from command line (may already be integrated)
- [ ] stdin argument input
- [ ] *Fix when lineages have multiple ranks, e.g. Tremellales sp. will be
  extracted from Tremellales input, when the order is likely what's requested*

### fa2clus
- [ ] sort log by default, and only unique run parameters
- [ ] percent positive mode
- [ ] integrate MCL
- [ ] rerun aggclus on new data

### fa2hmmer2fa
- [ ] Move from extracthmm to simplified output parsing

### fa2tree
- [ ] Implement fa2clus
- [ ] ignore non-fasta inputs
- [ ] take to phylogenomic tree from db2hgs

### gff2svg
- [ ] find a prettier way to create SVGs
- [ ] parse for in gene coordinates and annotations
- [ ] create a single file output option for multiple inputs

### jgiDwnld
- [x] remove gff v gff3 option

### manage_mtdb
- [ ] delete database feature
- [x] *fix local password encryption*
- [x] overwrite old password
- [x] move database feature
- [ ] archive and unarchive genomes
- [ ] remove logfiles as parting of clearing the cache
- [x] add combine DB option

### mtdb
- [x] add a log option of connected MTDBs
- [ ] remove standalone scripts from PATH
- [ ] look for old ome versions in query
- [x] add a version querying option
- [ ] add an option to query log of analyses

### ncbiDwnld
- [ ] db check to ensure log is relevant to input
- [ ] convert downloading to NCBI datasets
- [ ] add strain parsing from within GenBank records for entries that don't
  have an obvious strain entry

### predb2mtdb
- [ ] source to reference the annotation source/project name
- [ ] *integrate prokka/bakta*
- [x] error check FAA
- [ ] allow for just assembly accession in known sources
- [ ] allow inputting GBK

### update_mtdb
- [x] optimize dereplication, currently too slow
- [x] initial JGI predb2mtdb fails because assemblyPath doesn't exist as a
  column, but restarts are fine
- [ ] allow updating from Predb.tsv immediately
- [ ] update introduction output
- [ ] need a verbose option
- [ ] reversion option
- [ ] *reference a manually curated duplicate check*
- [ ] prohibit specific IDs implementation
- [ ] finish --save
- [ ] singular strain download option
- [ ] *pull failed JGI downloads from NCBI*
- [ ] remove overlap when rerunning failed genomes
- [ ] central MTDB repository and reference option
- [ ] Improve MD5 check efficiency (update_mtdb)
- [ ] print organism name with genome accession
- [ ] don't remove files until after predb2mtdb (requires update_mtdb specific
  function)
- [ ] Need a manually curated file to correct errors in naming, e.g. Vararia v
  Vavraia, Fibularhizoctonia v Fibulorhizoctonia
- [x] initialize from a predb
- [ ] option to remove entries that have been removed from genbank
- [ ] option to not dereplicate by genus and species alone
- [ ] main MTDB files for prokaryotes and fungi uploaded and that can be parsed
- [x] add option to update taxonomy of existing entries
- [ ] sp. will also not dereplicate
- [ ] make add option check for overwriting entries (indicating incorrect PREDB
  linkage)
- [ ] ensure `-t` overlooks non-JGI/NCBI sources
- [ ] ensure assembly accessions from non-JGI/NCBI sources are not included in
  download
- [ ] still use a redundancy check when --ncbi_only is specified, or prevent
  changing between NCBI only and non-ncbi database
