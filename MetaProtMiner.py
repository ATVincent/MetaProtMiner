#!/usr/bin/env python
import sys, getopt, os, re
from collections import Counter

def main(argv):

	Version = str('1.0')

	#Argument variables 
	Database = str()
	R1 = str()
	R2 = str()
	Threads = int()
	Sample = str()
	ISList = []
	LengthFile = str()
	Out = str()
	Cutoff = float ()
	HSP = float ()
	
	#Analysis variables 
	Dico_length = {}
	Numberofreads = float('0')
	Total_percent = float('0')
	Total_reads = float('0')
	Other_reads = float('0')
	
	try:
		opts, args = getopt.getopt(argv, "hD:1:2:T:S:L:O:C:A:")
	except getopt.GetoptError:
		print ("MetaProtMiner.py -D /Path/to/IS.faa -L /Path/to/Length.tsv -1 /Path/to/R1.fastq.gz -2 /Path/to/R2.fastq.gz -T Threads -S Sample_name -C Cutoff -A Alignment_length -O Output_directory")
		sys.exit(2)
	for opt, arg in opts:

		if opt == '-h':
			print ("MetaProtMiner.py -D /Path/to/IS.faa -L /Path/to/Length.tsv -1 /Path/to/R1.fastq.gz -2 /Path/to/R2.fastq.gz -T Threads -S Sample_name -C Cutoff -A Alignment_length -O Output_directory")
			sys.exit(2)
		elif opt == '-D':
			Database = str(arg)
		elif opt in ("-1"):
			R1 = str(arg)
		elif opt in ("-2"):
			R2 = str(arg)	
		elif opt in ("-T"):
			Threads = int(arg)
		elif opt in ("-S"):
			Sample = str(arg)
		elif opt in ("-L"):
			LengthFile = str(arg)
		elif opt in ("-C"):
			Cutoff = float(arg)
		elif opt in ("-A"):
			HSP = float(arg)
		elif opt in ("-O"):
			Out = str(arg)


	print ("== MetaProtMiner %s ==" %(Version))
	
	if not os.path.isdir(Out):
		os.system("mkdir %s" %(Out))

	Result_File = open("%s/%s.MPM" %(Out, Sample), 'w')

	if os.path.isfile("%s.dmnd" %(Database)):
		print ('--The database is already formatted')
	else:
		print ("--Formatting the database")
		os.system("diamond makedb --in %s -d %s.dmnd > %s/MetaProtMiner.log 2>&1 " %(Database, Database, Out))
		
	print ('--Preparing the reads')

	if os.path.isfile("%s/%s.fastq" %(Out, Sample)):
		print ("=>WARNING: The file %s.fastq already exist, skipping this step" %(Sample))
	else:
		if '.gz' in R1:
			os.system("zcat %s %s > %s/%s.fastq" %(R1, R2, Out, Sample))
		else:
			os.system("cat %s %s > %s/%s.fastq" %(R1, R2, Out, Sample))
	
	#Counts the number of reads present in the dataset 
	with open("%s/%s.fastq" % (Out, Sample)) as f:
		for line in f:
			Numberofreads = Numberofreads+1
	Numberofreads = Numberofreads/4

	
	print ('--Aligning the reads')
	if os.path.isfile("%s/%s.diamond" %(Out, Sample)):
		print ("=>WARNING: The file %s.diamond already exist, skipping this step" %(Sample))
	else:
		os.system("diamond blastx -q %s/%s.fastq -d %s.dmnd -p %d -c 1 -f 6 qseqid sseqid qlen slen evalue pident qcovhsp -k 1 -o %s/%s.diamond > %s/MetaProtMiner.log 2>&1 " %(Out, Sample, Database, Threads, Out, Sample, Out))


	print ('--Generating the finale output')
	
	with open("%s" % (LengthFile)) as f:
		for line in f:
			line = line.replace('\n', '').replace('\r', '')
			line = re.split("\t", line)
			IS = str(line[0])
			Family = str(line[1])
			Length = int (line[2])
			Dico_length.setdefault(IS, []).append(Family)
			Dico_length.setdefault(IS, []).append(Length)
	

	with open("%s/%s.diamond" % (Out, Sample)) as f:
		for line in f:
			line = line.replace('\n', '').replace('\r', '')
			line = re.split("\t", line)
			IS = line[1]
			Similarity = float(line[5])
			qcovhsp = float(line[6])

			if Similarity >= Cutoff and qcovhsp >= HSP:
				ISList.append(IS)

	Occurence = Counter(ISList)

	for IS_element, value in Occurence.items():
		Mapped_reads = float (value)
		Family = str (Dico_length[IS_element][0])
		Length = float (Dico_length[IS_element][1])
		
		Percent = float((((Mapped_reads*1000000)/Length)/Numberofreads))
		
		Total_percent = Total_percent + Percent
		Total_reads = Total_reads + Mapped_reads

		Result_File.write ("%s	%s	%f	%f\n" %(IS_element, Family, Mapped_reads, Percent))

	Other_reads = Numberofreads - Total_reads

	Result_File.write ("Mapped	NA	%f	NA\n" %(Total_reads))
	Result_File.write ("Not_mapped	NA	%f	NA\n" %(Other_reads))

	Result_File.close()
		
	print ("=> The score with the database %s for %s is %f" %(Database, Sample, Total_percent))


if __name__ == "__main__":
    main(sys.argv[1:])
