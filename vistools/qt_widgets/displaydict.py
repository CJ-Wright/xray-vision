from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import six
from PyQt4 import QtCore, QtGui
import sys

_defaults = {
    "expanded" : False,
}

class DisplayDict(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle('Display dictionary example')
        self._display_dict = RecursiveTreeWidget()
        self.setCentralWidget(self._display_dict)

    def set_tree(self, tree):
        self._display_dict.fill_widget(tree)


class RecursiveTreeWidget(QtGui.QTreeWidget):
    """
    Widget that recursively adds a list, dictionary or nested dictionary to
    as a tree widget

    Notes
    -----
    fill_item and fill_widget were taken from:
    http://stackoverflow.com/questions/21805047/qtreewidget-to-mirror-python-dictionary
    """
    def __init__(self):
        QtGui.QTreeWidget.__init__(self)
        self.itemClicked.connect(self.who_am_i)

    def fill_item(self, node, obj, node_name=None):
        node.setExpanded(_defaults["expanded"])
        if isinstance(obj, dict):
            # the object is a dictionary
            for k, v in sorted(six.iteritems(obj)):
                dict_child = QtGui.QTreeWidgetItem()
                dict_child.setText(0, unicode(k))
                self.add_child(node, dict_child)
                self.fill_item(dict_child, v)
        elif isinstance(obj, list):
            for v in obj:
                list_child = QtGui.QTreeWidgetItem()
                self.add_child(node, list_child)
                if type(v) is dict:
                    list_child.setText(0, '[dict]')
                    self.fill_item(list_child, v)
                elif type(v) is list:
                    list_child.setText(0, '[list]')
                    self.fill_item(list_child, v)
                else:
                    list_child.setText(0, unicode(v))
                list_child.setExpanded(_defaults["expanded"])
        else:
            child = QtGui.QTreeWidgetItem()
            if node_name is None:
                node_name = obj
            child.setText(0, unicode(node_name))
            self.add_child(node, child)

    def add_child(self, node, child):
        """
        Add a leaf to the tree at the 'node' position

        Parameters
        ----------
        node : QtGui.QTreeWidgetItem()
        child : QtGui.QTreeWidgetItem()
        """
        node.addChild(child)

    def find_root(self, node):
        """
        find the node whose parent is the invisible root item

        Parameters
        ----------
        node : QtGui.QTreeWidgetItem
            The node whose top level parent you wish to find

        Returns
        -------
        path_to_node : list
            list of keys
        dict_idx : int
            Index of the currently selected search result
        """
        path_to_node = []
        # get the parent node to track the two levels independently
        parent = node.parent()
        while parent != self.invisibleRootItem():
            path_to_node.insert(0, node.text(0))
            # move up the tree
            node = parent
            parent = parent.parent()

        # find the index of the search result
        dict_idx = parent.indexOfChild(node)

        return path_to_node, dict_idx

    def who_am_i(self, obj):
        print(obj.text(0))

    def fill_widget(self, obj):
        """
        Throw the 'object' at the recursive tree fill class 'fill_item()'

        Parameters
        ----------
        obj  : list, dict or obj
        """
        self.clear()
        self.fill_item(self.invisibleRootItem(), obj)


if __name__ == "__main__":
    from metadataStore.userapi.commands import search

    def gen_tree():
        query = {"owner" : "edill", "contents" : True}
        return search(**query)

    app = QtGui.QApplication(sys.argv)
    dd = DisplayDict()
    dd.set_tree(gen_tree())
    dd.show()
    sys.exit(app.exec_())
