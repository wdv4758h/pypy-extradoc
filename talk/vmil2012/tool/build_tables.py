from __future__ import division
import csv
import django
from django.template import Template, Context
import optparse
from os import path
import sys

#


def main(csvfile, template, texfile):
    with open(csvfile, 'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        lines = [l for l in reader]

    head = ['Benchmark',
            'number of operations before optimization',
            '\\% guards before optimization',
            'number of operations after optimization',
            '\\% guards after optimization',]

    table = []
    # collect data
    for bench in lines:
        keys = 'numeric guard set get rest new'.split()
        ops_bo = sum(int(bench['%s before' % s]) for s in keys)
        ops_ao = sum(int(bench['%s after' % s]) for s in keys)
        res = [
                bench['bench'],
                ops_bo,
                "%.2f (%s)" % (int(bench['guard before']) / ops_bo * 100, bench['guard before']),
                ops_ao,
                "%.2f (%s)" % (int(bench['guard after']) / ops_ao * 100, bench['guard after']),
              ]
        table.append(res)
    output = render_table(template, head, table)
    # Write the output to a file
    with open(texfile, 'w') as out_f:
        out_f.write(output)


def render_table(ttempl, head, table):
    # This line is required for Django configuration
    django.conf.settings.configure()
    # open and read template
    with open(ttempl) as f:
        t = Template(f.read())
    c = Context({"head": head, "table": table})
    return t.render(c)


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="%prog csvfile template.tex output.tex")
    options, args = parser.parse_args()
    if len(args) < 3:
        parser.print_help()
        sys.exit(2)
    else:
        main(args[0], args[1], args[2])

