from qtutil import *
from experiment.curvemodel import HermiteCurve, HermiteKey
from experiment.delegates import UndoableSelectionView
from experiment.enums import ELoopMode
from experiment.model import Clip, Shot, Event
from experiment.widgets import CurveList, ShotManager, CurveView, EventTimeline


if __name__ == '__main__':
    a = QApplication([])

    undoStack = QUndoStack()
    undoView = QUndoView(undoStack)

    clip0 = Clip('Clip 0', ELoopMode('Clamp'))
    clip0.curves.appendRow(HermiteCurve('uOrigin.x', [HermiteKey(0.0, 0.0, 0.0, 0.0), HermiteKey(1.0, 1.0, 1.0, 1.0)]).items)
    clip0.curves.appendRow(HermiteCurve('uFlash', [HermiteKey(0.0, 1.0, 1.0, 1.0), HermiteKey(1.0, 0.0, 0.0, 0.0)]).items)

    clip1 = Clip('Clip 1', ELoopMode('Loop'))
    clip1.curves.appendRow(HermiteCurve('uOrigin.x', [HermiteKey(2.0, 0.0, 0.0, 0.0), HermiteKey(3.0, 1.0, 0.0, 0.0)]).items)
    clip1.curves.appendRow(HermiteCurve('uOrigin.y', [HermiteKey(0.0, 0.0, 1.0, 1.0), HermiteKey(1.0, 1.0, 1.0, 1.0)]).items)

    clipManager = UndoableSelectionView(undoStack)
    clipManager.model().appendRow(clip0.items)
    clipManager.model().appendRow(clip1.items)

    curveList = CurveList(clipManager, undoStack)

    curveView = CurveView(curveList, undoStack)

    shotManager = ShotManager()
    shotManager.model().appendRow(Shot('New Shot', 'Scene 1', clip0, 0.0, 4.0, 1.0, 0.0).items)
    shotManager.model().appendRow(Event('New event', clip0, 0.0, 1.0, 1.0, 0.0).items)
    shotManager.model().appendRow(Event('New event', clip1, 1.0, 2.0, 0.5, 0.0).items)
    shotManager.model().appendRow(Event('New event', clip0, 2.0, 4.0, 0.25, 0.0).items)

    eventTimeline = EventTimeline(shotManager.model())

    mainContainer = QSplitter(Qt.Vertical)
    mainContainer.addWidget(undoView)
    mainContainer.addWidget(clipManager)
    mainContainer.addWidget(curveList)
    mainContainer.addWidget(curveView)
    mainContainer.addWidget(shotManager)
    mainContainer.addWidget(eventTimeline)

    mainWindow = QMainWindow()
    mainWindow.setCentralWidget(mainContainer)
    mainWindow.show()
    # makes sure qt cleans up & python stops after closing the main window; https://stackoverflow.com/questions/39304366/qobjectstarttimer-qtimer-can-only-be-used-with-threads-started-with-qthread
    mainWindow.setAttribute(Qt.WA_DeleteOnClose)

    a.exec_()
