# ClusterVision
# Generate a minimal slurm configuration based on the contents
# of the hwinv table.

import cmd
import subprocess
from itertools import groupby, count
from operator import itemgetter
from collections import defaultdict

import csv

from fast import as_strings, as_ints, ranges, check_output

class hashabledict(dict):
  def __key(self):
    return tuple((k,self[k]) for k in sorted(self))
  def __hash__(self):
    return hash(self.__key())
  def __eq__(self, other):
    return self.__key() == other.__key()

process = subprocess.Popen("tabdump hwinv", stdout=subprocess.PIPE, shell=True)
table=csv.DictReader(process.stdout)
types = defaultdict(list)

for node in table:
    name = node['#node']
    keys = ["cputype", "cpucount", "memory", "cputype", "disksize"]
    types[hashabledict(zip(keys, itemgetter(*keys)(node)))].append(name)
    
for type, nodes in types.items():
    node_list = as_strings(ranges(as_ints(nodes)))
    if len(node_list) > 1:
        names = 'c[' + ','.join(as_strings([(1,20), 33])) + ']'
    else:
        names = 'c' + node_list[0]
    print "NodeName=%s RealMemory=%s CPUs=%s" % (names, type['memory'], type['cpucount'])


