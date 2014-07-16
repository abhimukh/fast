import cmd
import subprocess
from itertools import groupby, count
from operator import itemgetter

def check_output(*popenargs, **kwargs):
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    return output

def as_ints(nodes):
    return [int(node[4:]) for node in nodes]

def as_strings(nodes, format1="%03d", format2="%03d-%03d"):
    return [(format2 if isinstance(node, tuple) else format1) % node for node in nodes]

def ranges(data):
    ranges = []
    for key, group in groupby(enumerate(data), lambda (index, item): index - item):
        group = map(itemgetter(1), group)
        if len(group) > 1:
            ranges.append((group[0], group[-1]))
        else:
            ranges.append(group[0])
    return ranges


class FastShell(cmd.Cmd):
    intro = "Welcome to the fast cloud shell.	Type help of ? to list commands.\n"
    prompt = "(fast)"
   
    def do_clusters(self, arg):
        "List clusters"
        print check_output("lsdef -t network -w domain!='' -i domain | grep domain | awk -F= '{print $2}'", shell=True)

    def do_nodes(self, arg):
        "List nodes"
        print check_output("nodels compute", shell=True)

    def do_containers(self, arg):
        """Return all the nodes in thix xCAT environment"""
        cmd = 'nodels %s | grep -P "^c\d+$"' % arg
        output = check_output(cmd, shell=True)
        print output

    def do_partition(self, args):
        groups = [int(group) for group in args.split()]
        nodes = check_output("nodels compute", shell=True).split()
        nodes = [int(node[4:]) for node in nodes]
        clusters = check_output("lsdef -t network -w domain!='' -i domain | grep domain | awk -F= '{print $2}'", shell=True).split()
        if sum(groups) > len(nodes):
            raise ValueError("You have allocated more nodes (%d) than are in the system (%d)" % (sum(groups), len(nodes)))
        if len(groups) > len(clusters):
            raise ValueError("You have allocated more clusters (%d) than are in the system (%d)" % (len(groups), len(nodes)))
        for cluster, size in zip(clusters, groups):
            head, nodes = nodes[:size], nodes[size:]
            # update xCAT config
            for node in head:
                cmd = 'nodech c%03d groups=%s' % (node, cluster)
                output = check_output(cmd, shell=True)
            # update SLURM config
            r = ranges(head)
            slurm_config = ','.join(['%03d-%03d' % (e[0], e[1]) if isinstance(e, tuple) else '%03d' % (e, ) for e in r])
            if slurm_config:
                slurm_config = 'c[' + slurm_config + ']'
            print slurm_config
 
        output = check_output("makehosts", shell=True)
        output = check_output("makedns", shell=True)
        print output

if __name__ == '__main__':
    FastShell().cmdloop()
        


