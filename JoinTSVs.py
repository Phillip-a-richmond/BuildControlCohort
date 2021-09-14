import argparse,sys

def GetOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument("-1","--File1",help="ThousandGenomesTSV", type=str, required=True)
    parser.add_argument("-2","--File2",help="GeuvadisTSV", type=str, required=True)
    parser.add_argument("-O","--Outfile",help="Joined Outfile", type=str, required=True)
    parser.add_argument("-B","--Bashscript",help="Bash Script for downloading files", type=str, required=True)

    args = parser.parse_args()
    thousandgenomesfilename=args.File1
    geuvadisfilename=args.File2
    outfilename=args.Outfile
    outbashscript=args.Bashscript
    return thousandgenomesfilename,geuvadisfilename,outfilename,outbashscript


# input files look like this tsv:
# url	md5	Data collection	Data type	Analysis group	Sample	Population	Data reuse policy

# Geuvadis
# ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR204/ERR204768/ERR204768.fastq.gz	a8a8da1d46f73484e1ce62d12c290dd4	Geuvadis	sequence	small RNA	HG00355	Finnish in Finland	http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/geuvadis/README_geuvadis_datareuse_statement.md 

# 1KG on GRCh38
# ftp://ftp.sra.ebi.ac.uk/vol1/run/ERR323/ERR3239480/NA12718.final.cram	923ca8ff7d4cd65fddd28e855e5f173d	1000 Genomes 30x on GRCh38	alignment	PCR-free high coverage	NA12718	Utah residents (CEPH) with Northern and Western European ancestry	http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000G_2504_high_coverage/20200526_1000G_2504plus698_high_cov_data_reuse_README.txt

# Doing this for the 1kG tsv
def ReadFileToDict(infilename):
    infile = open(infilename,'r')
    infile_dict = {}
    
    for line in infile.readlines():
        cols = line.strip('\n').split('\t')
        sampleId = cols[5]
        # some odd multi-sample lines for merged vcfs?
        if ',' in sampleId:
            continue
        infile_dict[sampleId] = cols

    return infile_dict
    

# This function parses a file, cuts out the sampleID column, and uses it to grab the corresponding line from the other file with matching sampleID
def ParseFileGrabFromDict(inputdict,infilename,outfilename,outbashscriptfilename):
    infile = open(infilename, 'r')
    outfile = open(outfilename, 'w')
    outbashscript = open(outbashscriptfilename,'w')

    # give outfile a new header
    outfile.write("#sampleID\tPopulation\tmRNA_link_R1\tmRNA_link_R2\tgenome_link\n")

    for line in infile.readlines():
        cols = line.strip('\n').split('\t')
        if cols[0]=='url':
            continue
        sampleId = cols[5]
        geu_link=cols[0]
        # skip over the _2 reads, since we'll grab them alongside the _1 reads
        if "_2.fastq.gz" in geu_link:
            continue
        geu_pop = cols[6]
        if sampleId in inputdict:
            #print(cols)
            #print(inputdict[sampleId])
            thousand_link=inputdict[sampleId][0]
            
            # here I'll use the geuvadis link to make the _2.fastq.gz too
            geu_link_r2 = geu_link.replace("_1.fastq.gz","_2.fastq.gz")

            outfile.write("%s\t%s\t%s\t%s\t%s\n"%(sampleId,geu_pop,geu_link,geu_link_r2,thousand_link))
            outbashscript.write("# Downloading sample: %s\n"%sampleId)
            outbashscript.write("wget -c -q %s -O %s_mRNA_1.fastq.gz\n"%(geu_link,sampleId))
            outbashscript.write("wget -c -q %s -O %s_mRNA_2.fastq.gz\n"%(geu_link_r2,sampleId))
            outbashscript.write("wget -c -q %s\n"%thousand_link)

        




def Main():
    print("join these bad boys")
    ThousandGenomesFilename,GeuvadisFilename,Outfilename,OutBashScript = GetOptions()

    # get 1kg file into a dict
    ThousandGenomesDict = ReadFileToDict(ThousandGenomesFilename)

    # parse geuvadis and grab from 1kg dict
    ParseFileGrabFromDict(ThousandGenomesDict,GeuvadisFilename,Outfilename,OutBashScript)
    


if __name__=="__main__":
    Main()


