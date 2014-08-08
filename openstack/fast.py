#############################################################################
# ClusterVision FastShell
# Author: hans.then@clustervision.com
#
# This file contains the Fast Shell program.
# TODO: split the check_output commands into a separate API for xCAT. 
# The current design has difficulty handling empty lines, trailing newlines etc
# Also, maybe in the future we could manipulate the xCAT database directly.
#
#############################################################################
import cmd
from common import *
from collections import defaultdict

class FastShell(cmd.Cmd):
    intro = "Welcome to the fast cloud shell.	Type help of ? to list commands.\n"
    prompt = "(fast) "
   
    def do_clusters(self, arg):
        "List clusters"
        print check_output("lsdef -t network -w domain!='' -i domain |" + 
                            "grep domain | awk -F= '{print $2}'", shell=True),

    def do_nodes(self, arg):
        "List nodes"
        print check_output("nodels compute", shell=True),

    def do_containers(self, arg):
        """Return all the nodes in thix xCAT environment"""
        cmd = 'nodels %s | grep -P "^c\d+$"' % arg
        output = check_output(cmd, shell=True)
        print output,

    def do_hwinv(self, arg):
        """Group nodes according to their resource classes"""
        groups = defaultdict(list)
        nodes, headers = table("hwinv")
        for node in nodes:
            if not node:
                continue
            #['node001', 'Intel(R) Atom(TM) CPU C2750 @ 2.40GHz', '8', '32232MB', 'sda:126GB', '', '']
            name, cpu, cores, mem, disk, disabled, comment = node
            groups[(cpu, cores, mem, disk)].append(name)
        for group, nodes in groups.items():
            print group, nodes

    def do_categories(self, args):
        """Show all defined categories"""
        output=check_output("lsdef -t group | grep ^hw- | awk '{print $1}'", 
                             shell=True)
        print output,

    def do_partition(self, args):
        """Partition a cluster into virtual clusters"""
        args = args.split()
        if args and args[0].startswith('hw-'):
            to_be_parted = args[0]
            args = args[1:]
        else:
            to_be_parted = 'compute'
        groups = [int(group) for group in args]
        if not groups:
            print "You have not specified how to partition"
            print "These are the partitions you have: "
            output=check_output("lsdef -t group | grep ^vc- |" + 
                                "awk '{print $1}'", shell=True)
            for line in output.strip().split('\n'):
                print line, ':'
                print check_output("lsdef -t group %s -i members | " % line + 
                                   "grep members", shell=True),
            return
        nodes = check_output("nodels %s" % to_be_parted, shell=True).split()
        nodes = [int(node[4:]) for node in nodes]
        clusters = check_output("lsdef -t network -w domain!='' -i domain |" + 
                                "grep domain | awk -F= '{print $2}'", shell=True)
        clusters = clusters.split()
        # Fixme: raising errors will stop the shell
        # we should simply report an error.
        if sum(groups) > len(nodes):
            raise ValueError("You have allocated more nodes (%d) " +
                             "than are in the system (%d)" 
                              % (sum(groups), len(nodes)))
        if len(groups) > len(clusters):
            raise ValueError("You have allocated more clusters (%d) " + 
                             "than are in the system (%d)" 
                              % (len(groups), len(nodes)))
        for cluster, size in zip(clusters, groups):
            head, nodes = nodes[:size], nodes[size:]
            # update xCAT config
            for node in head:
                cmd = 'nodech c%03d groups=%s' % (node, cluster)
                output = check_output(cmd, shell=True)
        # update SLURM config
        for cluster in clusters:
            head = check_output("lsdef -t group %s -i members | " % cluster +
                                 "grep members", shell=True).strip()

            if not head:
                 continue
            head = head.split('=')[1]
            head = [int(node[1:]) for node in head.split(',') if len(node)]
            # Here I should be able to split nodes based on further characteristics.
            cores, groups, categories = collect_partitions(head)
            
            def format_range(r):
                r = ranges(r)
                s = ','.join(['%03d-%03d' % (e[0], e[1]) \
                       if isinstance(e, tuple) else '%03d' % (e, ) \
                          for e in r])
                return 'c[' + s + ']' if s else ''

            for c in cores:
                cores[c] = format_range(cores[c])
            for g in groups:
                groups[g] = format_range(groups[g])
            for c in categories:
                categories[c] = format_range(categories[c])
            compute = format_range(head)

            print "#", cores, groups, categories
            # Without with, I know
            slurm_conf = open("/cluster/%s/etc/slurm-nodes.conf" % \
                               cluster, "w")
            print >> slurm_conf, render('slurm-nodes.conf', 
                                          {"cores": cores, 
                                           "groups": groups,
                                           "categories": categories,
                                           "compute": compute})
 
        print "Updating DNS, this may take some time . . ."
        output = check_output("makehosts", shell=True)
        output = check_output("makedns", shell=True)
        print "Done"

def collect_partitions(int_filter):
    """Collect hardware partitions for the slurm configuration"""
    groups = defaultdict(list)
    core_dict = defaultdict(list)
    cat_dict = defaultdict(list)
    nodes, headers = table("hwinv")
    for node in nodes:
        if not node:
            continue
        #['node001', 'Intel(R) Atom(TM) CPU C2750 @ 2.40GHz', '8', '32232MB', 'sda:126GB', '', '']
        name, cpu, cores, mem, disk, disabled, comment = node
        id = int(name[4:])
        if id not in int_filter: continue
        groups[(cpu, cores, mem, disk)].append(id)
        core_dict[cores].append(id)
    categories=check_output("lsdef -t group | grep ^hw- | awk '{print $1}'",
                             shell=True).split()
    for category in categories:
        head = check_output("lsdef -t group %s -i members | " % category +
                            "grep members", shell=True).strip()
        if not head:
            continue
        head = head.split('=')[1]
        head = head.split(',')
        for node in head:
            id = int(node[4:])
            if id not in int_filter: continue
            cat_dict[category].append(id)

    return core_dict, groups, cat_dict

if __name__ == '__main__':
    FastShell().cmdloop()
        


