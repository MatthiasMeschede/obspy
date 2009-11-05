# -*- coding: utf-8 -*-
"""
Conversion test suite for Dataless SEED into SEED RESP files.

Runs tests against all Dataless SEED files within the data/dataless directory. 
Output is created within the output/resp folder. Once generated files will
be skipped. Clear the output/resp folder in order to rerun all tests.
"""

from obspy.xseed import Parser
import glob
import os

# paths
dataless_path = os.path.join("data", "dataless")
resp_path = os.path.join("data", "resp")
output_path = os.path.join("output", "resp")

# generate output directory 
if not os.path.isdir(output_path):
    os.mkdir(output_path)


def _compareRESPFiles(original, new):
    """
    Compares two RESP files.
    """
    org_file = open(original, 'r')
    new_file = open(new, 'r')
    org_list = []
    new_list = []
    for org_line in org_file:
        org_list.append(org_line)
    for new_line in new_file:
        new_list.append(new_line)
    # Skip the first line.
    for _i in xrange(1, len(org_list)):
        try:
            assert org_list[_i] == new_list[_i]
        except:
            # Skip if it is the header.
            if org_list[_i] == '#\t\t<< IRIS SEED Reader, Release 4.8 >>\n' and\
               new_list[_i] == '#\t\t<< obspy.xseed, Version 0.1.3 >>\n':
                continue
            # Skip if its a short time string.
            if org_list[_i].startswith('B052F22') and \
                new_list[_i].startswith('B052F22') and \
                org_list[_i].replace('\n',
                    ':00:00.0000\n'[-(len(new_list[_i]) - \
                                      len(org_list[_i])) - 1:]) == \
                new_list[_i]:
                continue
            if org_list[_i].startswith('B052F23') and \
                new_list[_i].startswith('B052F23') and \
                org_list[_i].replace('\n',
                    ':00:00.0000\n'[-(len(new_list[_i]) - \
                                      len(org_list[_i])) - 1:]) == \
                new_list[_i]:
                continue
            msg = '\nCompare failed for:\n' + \
                  'File :\t' + original.split(os.sep)[-1] + \
                  '\nLine :\t' + str(_i + 1) + '\n' + \
                  'EXPECTED:\n' + \
                  org_list[_i] + \
                  'GOT:\n' + \
                  new_list[_i]
            raise AssertionError(msg)

# build up file list and loop over all files
files = []
files += glob.glob(os.path.join(dataless_path, '*', '*'))
files += glob.glob(os.path.join(dataless_path, '*', '*', '*'))
for file in files:
    # check and eventually generate output directory
    path = os.path.dirname(file)
    relpath = os.path.relpath(path, dataless_path)
    path = os.path.join(output_path, relpath)
    if not os.path.isdir(path):
        os.mkdir(path)
    # skip directories
    if not os.path.isfile(file):
        continue
    # create folder from filename
    seedfile = os.path.basename(file)
    resp_path = os.path.join(path, seedfile)
    # skip existing directories
    if os.path.isdir(resp_path):
        print "Skipping", os.path.join(relpath, seedfile)
        continue
    else:
        os.mkdir(resp_path)
        print "Parsing %s\t\t" % os.path.join(relpath, seedfile)
    # Create the RESP file.
    try:
        sp = Parser()
        sp.read(file)
        sp.writeRESP(folder=resp_path)
        sp.writeRESP(folder=resp_path + '.zip', zipped=True)
        # Compare with RESP files generated with rdseed from IRIS 
        for resp_file in glob.iglob(resp_path + os.sep + '*'):
            print '  ' + os.path.basename(resp_file)
            org_resp_file = resp_file.replace('output' + os.sep, 'data' + os.sep)
            _compareRESPFiles(org_resp_file, resp_file)
    except Exception, e:
        # remove all related files
        if os.path.isdir(resp_path):
            os.remove(resp_path)
        # raise actual exception
        raise e
