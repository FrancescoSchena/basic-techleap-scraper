from os import walk
import os
import multiprocessing
import functions
import re


if __name__ == "__main__":
	# Looking for the files in the /data folder
	mypath = os.path.abspath(os.getcwd()) + "/data"
	ext = "txt"
	files = []
	for (dirpath, dirnames, filenames) in walk(mypath):
		for file in filenames:
			if file.split(".")[1] == ext:  # Only files with the right extension
				files.append(file)
		break
	if not files:  # if files is empty
		raise Exception("Warning there are no files, check the path!")
		quit()  # no need to proceed

	s = "" if len(files) == 1 else "s"
	print(f"Analyzing {len(files)} file{s}:")
	[print("\t" + file) for file in files]


	# Generating list of links from the txt
	links = []
	for file in files:
		file = open(f"Data/{file}", "r").read()
		for i in [m.start() for m in re.finditer('href', file)]:
			closingcommas = file[i : i+50].find(">")
			link = file[i+6 : i+closingcommas-1]
			links.append(link)

	print("Starting processes")

	# Generating list of company links
	manager = multiprocessing.Manager()
	complinks = manager.list()
	jobs = []
	for link in links:
		p = multiprocessing.Process(target=functions.get_complink, args=(link, complinks))
		jobs.append(p)
		p.start()

	for proc in jobs:
		proc.join()

	# print(complinks)

	# Searching each link for emails
	manager = multiprocessing.Manager()
	compmails = manager.dict()
	jobs = []
	for link in complinks:
		p = multiprocessing.Process(target=functions.get_email, args=(link, compmails))
		jobs.append(p)
		p.start()

	for proc in jobs:
		proc.join()

'''	print(compmails)

	# Printing mails
	for i in compmails:
		print(i)
		[print("\t" + x) for x in compmails[i]]'''