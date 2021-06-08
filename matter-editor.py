#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from editfrontmatter import EditFrontMatter
import os
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="""
Add/edit yaml frontmatter title and tags to file. Adds tags in lowercase, and avoids adding duplicate flags. 
Basic usage: matter-editor.py --file FILE tag1 [tag2] [tagN..]
""")
parser.add_argument('--file', dest="file", type=str  ) 
parser.add_argument('--title', dest="title", type=str , default="", help="Force the title for a file, otherwise we try to automatically set it from the first line # tag or file name.") 
parser.add_argument('tags', metavar='tag', nargs='*',  help="tags for file", default=[] )
parser.add_argument('--overwrite-tags', dest="overwrite_tags", action="store_true", help="If file has existing tags, overwrite them (default behavior is to merge tags).")
args = parser.parse_args()
# print( args.tags ) 
# print( args.file ) 
# title = Path(args.file).with_suffix('')

# initialize `template_str` with jinja2 template file content
template_str = """
title: "{{ title }}"
{% if tags -%}
tags: {{ tags|lower }}
{% endif -%}
"""

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def main():

    # if file has no metadata thing, add an empty header
    title = Path(args.file).stem

    # print( os.path.abspath(args.file) )
    f = open(args.file, "r")
    # print( "runlines" )
    # print(f.readlines())
    lines = f.readlines()
    # print( lines[0] )
    if lines[0] != '---\n':
        # check for title at first #
        if lines[0].startswith('# '): 
            # use this as title
            title = lines[0][2:].rstrip()
        line_prepender(args.file, '---\n---\n' )

    # print(title)

    # instantiate the processor
    proc = EditFrontMatter(file_path=args.file, template_str=template_str)
    
    # set fields to delete from yaml
    # proc.keys_toDelete = ['deleteme']

    # print("fmatter tags")
    fmatter = proc.fmatter or {}
    # if an existing title is found, use that.
    if 'title' in fmatter:
        title = fmatter["title"]

    # force title specified with flag
    if args.title:
        title = args.title 

    # print( fmatter)
    tags = args.tags
    if 'tags' in fmatter:
        if args.overwrite_tags:
            tags = args.tags
        else: 
            # remove duplicate tags too
            tags = list(set(args.tags + fmatter['tags'] ))
    # print('tags:')
    # print(tags)
    

    # todo: delete tags if none given?
    if not tags and args.overwrite_tags:
        proc.keys_toDelete = ['tags']
        str_tags = "<deleted>"
        process = {'title': title}

    else:
        str_tags = ','.join(tags) 
        process = {'title': title, 'tags': tags }

    # populate variables and run processor
    proc.run(process)

    # dump file
    # print(proc.dumpFileData())
    proc.writeFile(args.file)
    print( f"Wrote {args.file} with title: '{title}' and tags: {str_tags}" )
if __name__ == '__main__':
   main()

