#!/usr/bin/env python
import sys
import os.path
import random
import subprocess
import re

# as per the metadata file, input and output directories are the arguments
[_, input_dir, output_dir, program_dir] = sys.argv

# unzipped submission data is always in the 'res' subdirectory
# unzipped reference data is always in the 'ref' subdirectory

scores = []
overall = True

for i in xrange(1, 7):
    preds = os.path.join(input_dir, 'res', 'track' + str(i) + '_preds.txt')
    gold = os.path.join(input_dir, 'ref', 'track' + str(i) + '_gold.txt')

    if os.path.exists(preds):
        sys.stdout.write("{0} found\n".format(preds))
        checkOutput = subprocess.check_output([os.path.join(program_dir, "check.pl"), preds])

        if ("OK!" not in checkOutput):
            sys.exit("Input has incorrect format. Check input before submitting!!")

        result = subprocess.check_output([os.path.join(program_dir, "correlation.pl"), gold, preds])
        result = re.findall("\d+\.\d+", result)

        if (len(result) != 1):
            sys.exit("Input has incorrect number of lines. Check input before submitting!!")
        scores.append(result[0])

    else:
        sys.stdout.write("{0} not found\n".format(preds))
        overall = False
        scores.append(0)


#with open(submission_path) as submission_file:
#    submission = submission_file.read()


#with open(os.path.join(input_dir, 'ref', 'truth.txt')) as truth_file:
#    truth = truth_file.read()

# the scores for the leaderboard must be in a file named "scores.txt"

with open(os.path.join(output_dir, 'scores.txt'), 'w') as out:
    if (overall):
        out.write("Overall:{0}\n".format( (float(scores[0]) + float(scores[1]) + float(scores[2]) + float(scores[3]) + float(scores[4]) + float(scores[5])) / 6 ))
    else:
        out.write("Overall:{0}\n".format(0))
    out.write("Track1:{0}\n".format(scores[0]))
    out.write("Track2:{0}\n".format(scores[1]))
    out.write("Track3:{0}\n".format(scores[2]))
    out.write("Track4:{0}\n".format(scores[3]))
    out.write("Track5:{0}\n".format(scores[4]))
    out.write("Track6:{0}\n".format(scores[5]))
