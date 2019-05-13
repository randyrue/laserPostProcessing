#!/usr/bin/python
###########################################################################
# Application:  laser_pp.py
###########################################################################
#load the required modules
import os, sys, string


def main():
    """ main entry point; only called if __main__ """
    # new file tag, this will be added to the input
    # file name for the output file
    global tag
    tag = "pp"
    
    
    # define the line changes here
    # in the form [["list","of","targets"], "replacement string"],\
    # note the last line has no comma at the end
    # any lines beginning with the targets will be replaced
    # if the target is an empty string the line will be removed
    changes = [\
		[["G0","G00"],"M10P1 G0  (turn off laser)"],\
		[["G1","G01"],"M11P1 G1 (turn on laser)"],\
		[["G2","G02"],"M11P1 G2 (turn on laser)"],\
		[["G3","G03"],"M11P1 G3 (turn on laser)"],\
		[["M3","M4","S"],""] # a blank space in the replacement string means remove these lines \
	       ]
    
    # try opening the input file, if it fails for any reason
    # return the usage message
    # entering wrong arguments or no arguments will also
    # launch the usage message
    try:
	infile = open(sys.argv[1])
	print "loading %s\n" % sys.argv[1]
    except:
	usage()
    
    nf_parts = sys.argv[1].split(".")
    new_file = "%s.%s.%s" % (string.join(nf_parts[0:-1],"."), tag, nf_parts[-1])

    # open the output file
    outfile = open(new_file, 'w')
	
    # parse the input file line by line
    # and write the output file
    lines = infile.readlines()
    for line in lines: # for each line in the input file
	if line.strip() == "": continue # skip blank lines
	# set a flag for whether this line should change
	change_me = 0
	for change in changes:	# for each entry in the changes list
	    targs = change[0]	# list of possible finds
	    rep = change[1]	# what to replace them with
	    for targ in targs: # for each possible target
		if line.split()[0].strip() == targ:
		    if rep == "": continue # skip this line
		    else: # replace the line
			print "changed line: %s" % line.strip()
			print "to: %s" % line.strip().replace(targ, rep)
			outfile.write(line.strip().replace(targ, rep) + "\n")
			# flip the change_me flag
			change_me = 1
	if change_me == 0: # if the line doesn't change, write it as is
	    outfile.write(line.strip() + "\n")
	    print "unchanged: %s" % line.strip()
		    
    outfile.close()	    
    print "\nwrote output file %s" % new_file

def usage():
    print "usage: laser_pp.py <input_file>"
    print "output file will be in the same location with \"%s\" included in its name" % tag
    sys.exit()

if __name__ == '__main__': main()
