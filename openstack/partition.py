import sys
import subprocess
from itertools import groupby, count
from operator import itemgetter

if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

def make_list(output):
    return [line.split()[0] for line in output.split('\n') if line]

def clusters():
    """List the clusters in this xCAT environment"""
    cmd = 'lsdef -t group | grep -v compute'
    output = subprocess.check_output(cmd, shell=True)
    return make_list(output)

def count():
    """Count the nodes in this xCAT environment"""
    cmd = 'lsdef -t node | wc -l'
    output = subprocess.check_output(cmd, shell=True)
    return make_list(output)

def nodes():
    """Return all the nodes in thix xCAT environment"""
    cmd = 'lsdef -t node'
    output = subprocess.check_output(cmd, shell=True)
    return make_list(output)

def group_nodes(nodes, group):
    """Assign this node to a virtual cluster"""
    cmd = 'nodech %s groups=compute,%s' % (nodes, group)
    output = subprocess.check_output(cmd, shell=True)
    print output

def as_ints(nodes):
    return [int(node[4:]) for node in nodes]

def as_ranges(data, prefix=''):
    ranges = []
    for key, group in groupby(enumerate(data), lambda (index, item): index - item):
        group = map(itemgetter(1), group)
        if len(group) > 1:
            ranges.append((group[0], group[-1]))
        else:
            ranges.append(group[0])
    return ','.join(['%s%03d-%s%03d' % (prefix, e[0], prefix, e[1]) if isinstance(e, tuple) else '%s%03d' % (prefix, e) for e in ranges])

def partition(groups):
    lst = as_ints(nodes())
    ranges = []
    if sum(groups) > len(lst):
        raise ValueError("You have allocated more nodes (%d) than are in the system (%d)" % (sum(groups), len(lst)))
    for cluster, size in enumerate(groups, 1):
        head, lst = lst[:size], lst[size:]
        group_nodes(as_ranges(head, 'node'), 'vc-%d' % cluster)

if __name__ == '__main__':
    # first do the list command
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = 'clusters'

    for line in eval('%s()' % command):
       print line

   
