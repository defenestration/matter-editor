---
title: matter-editor
tags:
- readme
- tags
- hugo
- jekyll
- blah
---
# matter-editor
Yaml Front Matter Editor script for Markdown or other files. Quickly create a 'title' and 'tags' in your file. 

Designed for use with mkdocs, hugo or other html generators that work using markdown files.

Requires editfrontmatter pip package: `pip install editfrontmatter`

For bulk actions, copy to your PATH and use something like:

```
for f in **/*.md; do echo $f; matter-editor.py --file "$f" mytag1 mytag2;  done
```
