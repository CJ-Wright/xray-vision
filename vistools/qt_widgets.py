from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import six

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

from . import images


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas  # noqa
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar  # noqa
from matplotlib.figure import Figure
from matplotlib.cm import datad


class Xsection_widget(FigureCanvas):
    def __init__(self, init_image, parent=None):
        self.fig = Figure((24, 24), tight_layout=True)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        self.xsection = images.xsection_viewer(self.fig, init_image)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

_CMAPS = datad.keys()
_CMAPS.sort()


class StackScanner(QtGui.QWidget):
    def __init__(self, stack, page_size=10, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout()

        self._stack = stack

        self._len = len(stack)
        self.xsection = Xsection_widget(stack[0])

        # set up slider
        self._slider = QtGui.QSlider(parent=self)
        self._slider.setRange(0, self._len - 1)
        self._slider.setTracking(True)
        self._slider.setSingleStep(1)
        self._slider.setPageStep(page_size)
        self._slider.valueChanged.connect(self.update_frame)
        self._slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        # and it's spin box
        self._spinbox = QtGui.QSpinBox(parent=self)
        self._spinbox.setRange(self._slider.minimum(), self._slider.maximum())
        self._spinbox.valueChanged.connect(self._slider.setValue)
        self._slider.valueChanged.connect(self._spinbox.setValue)
        self._slider.rangeChanged.connect(self._spinbox.setRange)
        # make slider layout
        slider_layout = QtGui.QHBoxLayout()
        slider_layout.addWidget(self._slider)
        slider_layout.addWidget(self._spinbox)

        # make cmap combo-box
        self._cm_cb = QtGui.QComboBox()
        self._cm_cb.setEditable(True)
        self._cm_cb.addItems(_CMAPS)
        #        self._cm_cb.currentIndexChanged.connect(self.update_cmap)
        self._cm_cb.setEditText('gray')
        self._cm_cb.editTextChanged.connect(self.update_cmap)

        self.mpl_toolbar = NavigationToolbar(self.xsection, self)
        # add toolbar
        layout.addWidget(self.mpl_toolbar)
        # add main widget
        layout.addWidget(self.xsection)
        # add slider layout
        layout.addLayout(slider_layout)
        # add cmap selector
        layout.addWidget(self._cm_cb)
        self.setLayout(layout)

    @QtCore.Slot(int)
    def update_frame(self, n):
        self.xsection.xsection.update_image(self._stack[n])

    @QtCore.Slot(str)
    def update_cmap(self, cmap_name):
        try:
            self.xsection.xsection.update_colormap(cmap_name)
        except ValueError:
            pass
