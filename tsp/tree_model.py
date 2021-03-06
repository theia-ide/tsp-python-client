# The MIT License (MIT)
#
# Copyright (C) 2020 - Ericsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from tsp.data_type import DataType
from datetime import timedelta
from datetime import datetime
from decimal import Decimal
from tabulate import tabulate
import pandas as pd


class TreeModel(object):

    def __init__(self, entries, descriptors=None):
        self._descriptors = descriptors
        self._root = TreeItem(None)
        self._root.set_trace("TODO")
        id_map = {}
        id_map[-1] = self._root

        for entry in entries:
            elem = TreeItem(entry)
            id_map[entry.id] = elem

            parent = id_map[entry.parent_id]
            if (entry.parent_id in id_map.keys() and elem not in parent.get_children()):
                parent.add_child(elem)
                elem.set_parent(parent)

    def print(self):
        data = []
        if (self._descriptors is not None):
            headers = []
            for descriptor in self._descriptors:
                headers.append(descriptor.text)
            for child in self._root.get_children():
                data = child.print(data, 0)
            df = {}
            if (len(headers) == len(data)):
                df = pd.DataFrame(data, columns=headers)
            else:
                df = pd.DataFrame(data)
            print(tabulate(df.values, headers, tablefmt="fancy_grid"))
        else:
            for child in self._root.get_children():
                child.print(data, 0)


class TreeItem(object):

    def __init__(self, entry=None):
        self._entry = entry
        self._parent = None
        self._children = []
        self._trace = None
        self._indent = 2

    def set_parent(self, parent):
        self._parent = parent

    def get_parent(self):
        return self._parent

    def set_entry(self, entry):
        self._entry = entry

    def get_entry(self):
        return self._entry

    def set_trace(self, trace):
        self._trace = trace

    def add_child(self, child):
        self._children.append(child)

    def get_children(self):
        return self._children

    def print(self, data, depth=0):
        row = []
        if self._entry is not None:
            labels = self._entry.labels
            prefix = ""
            if depth > 0:
                prefix = "|____"
            if len(labels) == 1:
                if(depth > 0):
                    print("  ", end="")
                for x in range((int)(depth / self._indent) - 1):
                    print("| ", end="")
                other = ""
                others = self._entry.others
                # TODO print TimeGraphEntry specific fields
                for k in others:
                    other = ('{0} ({1}, {2})'.format(other, k, others.get(k)))
                print("{0}{1} ({1}, {2}) {3} {4}".format(prefix, self._entry.labels[0], self._entry.id, self._entry.parent_id, other))
            else:
                label_str = ""
                if(depth > 0):
                    label_str = label_str + "  "
                for x in range((int)(depth / self._indent) - 1):
                    label_str = label_str + "| "
                i = 0
                label_str = label_str + prefix
                for label in labels:
                    if (i == 0):
                        row.append(label_str + label)
                    else:
                        row.append(label)
                    i = i + 1
            data.append(row)
        for child in self.get_children():
            child.print(data, depth + self._indent)
        return data
