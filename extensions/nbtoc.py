# nbtoc - ipython extension
#
# Print a table of contents for IPython notebook file (.ipynb)
# Put this file to ~/.ipython/extensions
#
# Usage:
#   %load_ext nbtoc
#   %print_toc welcome.ipynb
#
# Author: Cho-Yi Chen (ntu.joey@gmail.com)
import sys
import json
import IPython
from IPython.core.magic import magics_class, line_magic, Magics
from IPython.core.display import HTML

@magics_class
class nbtoc(Magics):
    @line_magic
    def print_toc(self, line):
        """Print a table of contents for an ipynb.
        
        Usage:
            %print_toc <ipynb>[, MAX]
        
        Arguments:
            <ipynb>: The ipynb file to read.
            MAX: How deep the header level to print.
        """
        if "," in line:
            PATH, MAX = line.split(",", 1)
            MAX = int(MAX)
        else:
            PATH = line
            MAX = 2  # default

        f = json.load(open(PATH))
        self.out = []
        for cell in f["cells"]:
            if cell['cell_type'] == 'markdown':
                if cell['source'][0].startswith("#"):
                    self.out.append(self.get_heading(cell['source'][0], max=MAX))
        #print "\n".join(self.out)
        return self


    def _repr_html_(self):
        # from markdown
        # return markdown.markdown("\n".join(self.out))
        # from a list of elements [lv, str, url]
        html = ""
        old_lv = 1
        html += "<ol>"
        for h in self.out:
            lv, s, url = h
            if lv > old_lv:
                html += "<ol>"
            if lv < old_lv:
                html += "</ol>"
            html += '<li><a href="#%s">%s</a></li>' % (url, s)
            old_lv = lv
        html += "</ol>"
        return html

    def get_heading(self, s, min=1, max=2):
        if s.startswith("####"):
            lv = 4
        elif s.startswith("###"):
            lv = 3
        elif s.startswith("##"):
            lv = 2
        elif s.startswith("#"):
            lv = 1
        else:
            lv = 0
        if min <= lv <= max:
            s = s.lstrip("#").strip()
            # to markdown
            #return "%s* [%s](#%s)" % (' ' * (lv-1)*2, s, s.replace(' ', '-'))
            # to a list of elements
            return [lv, s, s.replace(' ', '-')]

def load_ipython_extension(ipython):
    ipython.register_magics(nbtoc)

