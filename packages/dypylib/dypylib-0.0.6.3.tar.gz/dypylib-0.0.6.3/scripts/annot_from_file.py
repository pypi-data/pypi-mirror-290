#!/usr/bin/env python3

'''
Add informations which are retrived from dbfile to infile.
'''

import sys
from dypylib.bio.base import DictFile


def extend_lst(lst, obj):
    """ Do not split string when extend.
        Why have to use this function: DictFile object return list
          when multiple element is chosen, while str when only one
          element is chosen.
    """
    if isinstance(obj, str):
        obj = [obj]
    return lst.extend(obj)


def mapper(infile, outfile, dbdata, sep, has_header=True, keycol=0, null=[""],
           value_header=None, omit_col=None):

    # for output
    if not isinstance(null, list):
        null = [null]

    if has_header:
        header = infile.readline().rstrip("\n")
        # When infile and db file has header at the same time,
        #   output both header.
        # When header of db file is not exist, value_header can be appended.
        if dbdata.has_header:
            header_lst = dbdata.header_lst
            # Delete omit column
            if omit_col:
                for i in sorted(set(omit_col), reverse=True):
                    header_lst.pop(i)
            outfile.write(header + sep + sep.join(header_lst) + "\n")
        elif value_header:
            outfile.write(header + sep + value_header + "\n")
        else:
            outfile.write(header + "\n")

    for eachline in infile:
        line_array = eachline.strip("\n").split(sep)
        values = dbdata.get(line_array[keycol], null * dbdata.valueLength())
        if omit_col:
            for i in sorted(set(omit_col), reverse=True):
                values.pop(i)
        extend_lst(line_array, values)
        outfile.write(sep.join(line_array) + "\n")


def parse_value_col(value_col):

    if value_col is None:
        return value_col
    return list(map(int, value_col.split(",")))


def main(argv):

    import argparse

    parser = argparse.ArgumentParser(
        description="Add information to file1 accoding \
                     to key-value lines in file2.")
    parser.add_argument('file1', nargs='?',
                        help="file to be add information, \"-\" for stdin ")
    parser.add_argument('file2', nargs='?', help="dbfile, \"-\" for stdin")
    parser.add_argument('-o', '--outfile', nargs='?', help="output file",
                        default=sys.stdout, type=argparse.FileType('w'))
    parser.add_argument('-s1', '--sep1', nargs='?', default="\t")
    parser.add_argument('-s2', '--sep2', nargs='?', default="\t")
    parser.add_argument('-k1', '--keycol1', nargs='?', default=0, type=int)
    parser.add_argument('-k2', '--keycol2', nargs='?', default=0, type=int)
    parser.add_argument('-v', '--valuecol', nargs='?', default=None,
                        help="Format: 0,3,5,10. Whole line will be chose when \
                              not set this option")
    parser.add_argument('--omit-val-col', nargs='?', default=None,
                        help="Format: 0,3,5,10. Value column to be ommited. \
                        Conflict with --valuecol.")
    parser.add_argument('-p', '--place_holder', nargs='?', default="",
                        help="Set a place holder. For example \"-\" or \"NA\".")
    parser.add_argument('-vf', '--value_header', nargs='?', default=None,
                        help="Additional value header. Useful only when n1 set \
                              True and value length equals 1.")
    parser.add_argument('-n1', '--has_header1', action='store_true',
                        help="if file1 has header,set this option.")
    parser.add_argument('-n2', '--has_header2',
                        action='store_true', help='same with n1 but for file2')
    args = parser.parse_args(argv[1:])

    sep1 = args.sep1
    sep2 = args.sep2
    keycol1 = args.keycol1  # key column which define filter limits
    keycol2 = args.keycol2
    has_header1 = args.has_header1
    has_header2 = args.has_header2
    valuecol = parse_value_col(args.valuecol)
    omit_col = parse_value_col(args.omit_val_col)

    if args.file1 == '-' and args.file2 == '-':
        raise KeyError("You can not set file1 and file2 to \"-\" at the same time!")
    if args.file1 == '-':
        file1 = sys.stdin
    else:
        file1 = open(args.file1)
    if args.file2 == '-':
        file2 = sys.stdin
    else:
        file2 = open(args.file2)
    outfile = args.outfile

    if not (args.valuecol is None or args.omit_val_col is None):
        raise KeyError("You can not set valuecol and omit-val-col at the same \
time!")
        sys.exit(1)

    dbdata = DictFile(args.file2, keypos=keycol2, delimiter=sep2,
                      has_header=has_header2, valuepos=valuecol)
    mapper(file1, args.outfile, dbdata, sep1, has_header1, keycol1,
           null=args.place_holder, value_header=args.value_header,
           omit_col=omit_col)


if __name__ == '__main__':

    main(sys.argv)
