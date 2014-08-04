import subprocess
from itertools import groupby, count
from operator import itemgetter
import csv
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('/root/fast/openstack/templates'))

def check_output(*popenargs, **kwargs):
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    return output

def as_ints(nodes):
    return [int(node[4:]) for node in nodes]

def ranges(data):
    ranges = []
    for key, group in groupby(enumerate(data), lambda (index, item): index - item):
        group = map(itemgetter(1), group)
        if len(group) > 1:
            ranges.append((group[0], group[-1]))
        else:
            ranges.append(group[0])
    return ranges

def table(table_name):
    output = check_output(["tabdump", table_name])
    output = output.split('\n')
    # first row is column headers
    headers = output[0].lstrip('#').split(',')
    return csv.reader(output[1:]), headers

def render(name, context):
    template = env.get_template(name)
    return template.render(context)
