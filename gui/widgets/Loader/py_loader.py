from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer, Property, QPropertyAnimation, QPoint
from PySide6.QtGui import QPainter, QColor, QPen

# class CircularLoader(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setFixedSize(100, 100)
#         self._angle = 0
#         self._text = "Processing..."
        
#         # Create the rotation animation
#         self.animation = QPropertyAnimation(self, b"rotation")
#         self.animation.setDuration(1000)  # 1 second per rotation
#         self.animation.setStartValue(0)
#         self.animation.setEndValue(360)
#         self.animation.setLoopCount(-1)  # Infinite loop
        
#         # Layout for the text label
#         layout = QVBoxLayout()
#         self.label = QLabel(self._text)
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.label)
#         layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
#         self.setLayout(layout)

#     def get_rotation(self):
#         return self._angle

#     def set_rotation(self, angle):
#         self._angle = angle
#         self.update()

#     rotation = Property(float, get_rotation, set_rotation)

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)

#         # Calculate center point
#         center = QPoint(self.width() // 2, self.height() // 2 - 10)
#         radius = min(self.width(), self.height()) // 3

#         # Create gradient pen
#         pen = QPen(QColor(0, 120, 212))  # Blue color
#         pen.setWidth(4)
#         painter.setPen(pen)

#         # Draw arc
#         painter.translate(center)
#         painter.rotate(self._angle)
#         painter.drawArc(-radius, -radius, radius * 2, radius * 2, 0, 300 * 16)  # 300 degrees * 16 (Qt's angle system)

#     def start(self):
#         self.show()
#         self.animation.start()

#     def stop(self):
#         self.animation.stop()
#         self.hide()

#     def setText(self, text):
#         self._text = text
#         self.label.setText(text)

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer, Property, QPropertyAnimation, QPoint, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QPen

class CircularLoader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(120, 120)
        self._angle = 0
        self._opacity = 1.0
        self._text = "Loading..."
        
        # Rotation Animation
        self.rotation_animation = QPropertyAnimation(self, b"rotation")
        self.rotation_animation.setDuration(800)
        self.rotation_animation.setStartValue(0)
        self.rotation_animation.setEndValue(360)
        self.rotation_animation.setLoopCount(-1)
        self.rotation_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Opacity Animation
        self.opacity_animation = QPropertyAnimation(self, b"opacity")
        self.opacity_animation.setDuration(1000)
        self.opacity_animation.setStartValue(1.0)
        self.opacity_animation.setEndValue(0.3)
        self.opacity_animation.setLoopCount(-1)
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Layout for the text label
        layout = QVBoxLayout()
        self.label = QLabel(self._text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.setLayout(layout)

    def get_rotation(self):
        return self._angle

    def set_rotation(self, angle):
        self._angle = angle
        self.update()

    rotation = Property(float, get_rotation, set_rotation)

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, opacity):
        self._opacity = opacity
        self.update()

    opacity = Property(float, get_opacity, set_opacity)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Apply opacity
        painter.setOpacity(self._opacity)

        # Center point and radius calculation
        center = QPoint(self.width() // 2, self.height() // 2 - 10)
        radius = min(self.width(), self.height()) // 3

        # Gradient pen
        pen = QPen(QColor(0, 120, 212))
        pen.setWidth(6)
        painter.setPen(pen)

        # Draw rotating arc
        painter.translate(center)
        painter.rotate(self._angle)
        painter.drawArc(-radius, -radius, radius * 2, radius * 2, 0, 300 * 16)

    def start(self):
        self.show()
        self.rotation_animation.start()
        self.opacity_animation.start()

    def stop(self):
        self.rotation_animation.stop()
        self.opacity_animation.stop()
        self.hide()

    def setText(self, text):
        self._text = text
        self.label.setText(text)







# class LoadingLabel(QLabel):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._opacity = 1.0

#     @Property(float)
#     def opacity(self):
#         return self._opacity

#     @opacity.setter
#     def opacity(self, value):
#         self._opacity = value
#         self.setStyleSheet(f"""
#             QLabel {{
#                 color: #2196F3;
#                 font-size: 14px;
#                 font-weight: bold;
#                 background-color: rgba(255, 255, 255, {value});
#                 border-radius: 10px;
#                 padding: 10px;
#             }}
#         """)