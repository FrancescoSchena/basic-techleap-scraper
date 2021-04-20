from os import walk
import os
import multiprocessing
import functions
import re

externalfile = False
only_complinks = True


if __name__ == "__main__":
	if externalfile:
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

		functions.line(2)

		# Generating list of links from the txt
		links = []
		for file in files:
			file = open(f"Data/{file}", "r").read()
			for i in [m.start() for m in re.finditer('href', file)]:
				closingcommas = file[i : i+50].find(">")
				link = file[i+6 : i+closingcommas-1]
				if link:
					links.append(link)

	else:  # Fallback
		links = ['/companies/scope_biosciences', '/companies/luuno', '/companies/deeptrial', '/companies/arize', '/companies/amberscript', '/companies/be_sure_healthcare_b_v_', '/companies/join', '/companies/vitestro', '/companies/recheck', '/companies/frame_therapeutics', '/companies/the_close_app', '/companies/we4sea', '/companies/neurolytics', '/companies/hellomaas', '/companies/go_build_it_bouw7_']

	print("Starting processes")

	# Printing links
	print(f"There are {len(links)} links")
	functions.line()
	print("Finding links...")

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


	# Printing links
	functions.line(1)
	print(f"There are {len(links)} links")
	functions.line(1)

	# Printing complinks
	print(f"There are {len(complinks)} comp_links")

	if externalfile:
		with open('complinks.txt', 'w') as f:  # Saving the complinks for later ;)
			for i in complinks:
				f.write(i+"\n")

	if only_complinks:
		quit()
	functions.line(1)
	print("Finding mails...")

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

	functions.line(2)

	# Printing mails
	print(f"There are {len(compmails)} mails")
	

	for i in compmails:
		print(i)
		[print("\t" + x) for x in compmails[i]]
