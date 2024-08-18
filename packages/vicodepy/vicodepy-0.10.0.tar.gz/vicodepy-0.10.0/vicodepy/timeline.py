# ViCodePy - A video coder for Experimental Psychology
#
# Copyright (C) 2024 Esteban Milleret
# Copyright (C) 2024 Rafael Laboissière
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtCore import (
    Qt,
    QPointF,
)
from PySide6.QtGui import (
    QColor,
    QFontMetrics,
)
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGraphicsRectItem,
    QGraphicsItem,
    QLineEdit,
    QMenu,
    QMessageBox,
)

from .event import ChangeEvent, ChooseEvent
from .textedit import TextEdit


class Timeline(QGraphicsRectItem):
    FIXED_HEIGHT: float = 60.0

    def __init__(self, name: str, time_pane=None):
        super().__init__()
        self.name = name
        self.time_pane = time_pane
        self.annotations = []
        self.events = None
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptHoverEvents(True)
        self.label = TimelineLabel(self.name, self)
        self._select = False
        self.description = None

    @property
    def select(self):
        return self._select

    @select.setter
    def select(self, select):
        if select != self._select:
            self._select = select

    def addToScene(self):
        """Add the timeline to the scene"""
        # Set Y of the timeline based on the timescale height and the timeline
        # lines heights present on the scene
        self.setPos(
            0,
            self.time_pane.time_pane_scale.rect().height()
            + (len(self.time_pane.timelines) - 1) * self.FIXED_HEIGHT,
        )

        # Set the right rect based on the scene width and the height constant
        self.setRect(
            0,
            0,
            self.time_pane.scene.width(),
            self.FIXED_HEIGHT,
        )

        # Add line to the scene
        self.time_pane.scene.addItem(self)

    def add_event(self, event):
        """Add an event to the timeline"""
        self.events.add_event(event)
        self.events.sort(key=lambda x: x.name.lower())

    def remove_event(self, event):
        """Remove a event from the timeline"""
        self.events.remove(event)

    def get_event_by_name(self, name):
        return next((x for x in self.events if x.name == name), None)

    def add_annotation(self, annotation):
        """Add an annotation to the timeline"""
        self.annotations.append(annotation)
        self.annotations.sort(key=lambda x: x.start_time)
        self.time_pane.data_needs_save = True

    def remove_annotation(self, annotation):
        """Remove an annotation from the timeline"""
        self.annotations.remove(annotation)

    def update_rect_width(self, new_width: float):
        """Update the width of the timeline"""
        rect = self.rect()
        rect.setWidth(new_width)
        rect_label = self.label.rect()
        rect_label.setWidth(new_width)
        self.label.setRect(rect_label)
        self.setRect(rect)

    def on_remove(self):
        if self.annotations:
            answer = QMessageBox.question(
                self.time_pane,
                "Confirmation",
                "There are annotations present. "
                "Do you want to remove this timeline?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if answer == QMessageBox.StandardButton.Yes:
                while self.annotations:
                    self.annotations[0].remove()
        # The following does not yet work, since there is no provision for
        # adjusting the positions of the timelines inside the time pane.
        # self.time_pane.scene.removeItem(self)
        # if self in self.time_pane.timelines:
        #     self.time_pane.timelines.remove(self)
        # del self

    # FIXME: Move into class TimelineLabel
    def edit_properties(self):
        dialog = QDialog(self.time_pane)
        dialog.setWindowTitle("Timeline properties")

        layout = QFormLayout(self.time_pane)
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.label.text)
        self.name_edit.returnPressed.connect(dialog.accept)
        layout.addRow("Name: ", self.name_edit)
        layout.addRow("Description:", None)
        self.description_edit = TextEdit(self, self.description)
        layout.addRow(self.description_edit)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self.time_pane,
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)

        dialog.exec()
        if dialog.result() == dialog.DialogCode.Accepted:
            self.label.text = self.name_edit.text()
            self.description = self.description_edit.toPlainText()
            self.label.setToolTip(self.description)

    def update_annotations(self):
        for annotation in self.annotations:
            annotation.update_style()

    def edit_events(self):
        while True:
            events_dialog = ChooseEvent(self.event_collection, self.time_pane)
            events_dialog.exec()
            if events_dialog.result() == QMessageBox.DialogCode.Accepted:
                e = events_dialog.get_chosen()
                ChangeEvent(e, self.time_pane).exec()
                self.update_annotations()
            if events_dialog.result() == QMessageBox.DialogCode.Rejected:
                break

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            menu = QMenu()
            menu.addAction("Add new timeline").triggered.connect(
                self.time_pane.handle_timeline
            )
            menu.addAction(
                "Delete timeline (not yet fully implemented)"
            ).triggered.connect(self.on_remove)
            menu.addAction("Edit timeline properties").triggered.connect(
                self.edit_properties
            )
            menu.addAction("Edit events").triggered.connect(self.edit_events)
            menu.exec(event.screenPos())
        else:
            super().mousePressEvent(event)
        return


class TimelineLabel(QGraphicsRectItem):
    FIXED_HEIGHT = 20

    def __init__(self, text: str, parent: Timeline = None):
        super().__init__(parent)
        self.text = text
        rect = self.parentItem().rect()
        rect.setHeight(self.FIXED_HEIGHT)
        self.setRect(rect)
        self.parent = parent

    def paint(self, painter, option, widget=...):
        # Draw the rectangle
        self.draw_rect(painter)

        # Draw the text
        self.draw_text(painter)

    def draw_rect(self, painter):
        """Draw the timeline label rectangle"""
        # Set Pen and Brush for rectangle
        if self.parent.select:
            color = QColor(40, 40, 40)
        else:
            color = QColor(200, 200, 200)
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawRect(self.rect())

    def draw_text(self, painter):
        """Draw the timeline label text"""
        if self.parent.select:
            color = QColor(200, 200, 200)
        else:
            color = QColor(150, 150, 150)
        painter.setPen(color)
        painter.setBrush(color)

        font = painter.font()
        fm = QFontMetrics(font)

        text_width = fm.boundingRect(self.text).width()
        text_height = fm.boundingRect(self.text).height()
        # Get timeline polygon based on the viewport
        timeline_in_viewport_pos = self.parentItem().time_pane.view.mapToScene(
            self.rect().toRect()
        )

        bounding_rect = timeline_in_viewport_pos.boundingRect()

        # Get the viewport rect
        viewport_rect = self.parentItem().time_pane.view.viewport().rect()

        # Calcul the x position for the text
        x_alignCenter = bounding_rect.x() + viewport_rect.width() / 2

        text_position = QPointF(x_alignCenter - text_width / 2, text_height - 3)

        painter.drawText(text_position, self.text)

    def set_text(self, text):
        self.text = text
