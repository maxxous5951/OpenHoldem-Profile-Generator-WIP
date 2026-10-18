"""Interface PyQt6 générée automatiquement à partir du schéma de paramètres."""
from __future__ import annotations

import json
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QFileDialog, QFormLayout, QHBoxLayout,
                             QLabel, QLineEdit, QMainWindow, QMessageBox, QPlainTextEdit, QPushButton, QScrollArea,
                             QSpinBox, QSplitter, QTabWidget, QVBoxLayout, QWidget)

from .. import generator, presets, validator
from ..params import GROUPS, SCHEMA, coerce

DARK = """
QWidget { background:#14131B; color:#EDEBF5; font-size:13px; }
QLineEdit,QPlainTextEdit,QComboBox,QSpinBox,QDoubleSpinBox { background:#1E1D2A; border:1px solid #3F3D56; border-radius:4px; padding:4px; }
QPushButton { background:#0a522c; border:none; border-radius:4px; padding:7px 14px; font-weight:bold; }
QPushButton:hover { background:#13804a; }
QTabBar::tab { background:#1E1D2A; padding:7px 12px; margin-right:2px; }
QTabBar::tab:selected { background:#0a522c; }
QToolTip { background:#1E1D2A; color:#EDEBF5; border:1px solid #3F3D56; }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenHoldem Profile Generator 2")
        self.resize(1280, 820)
        self.widgets: dict[str, QWidget] = {}

        top = QWidget()
        tl = QHBoxLayout(top)
        tl.setContentsMargins(0, 0, 0, 0)
        self.style_box = QComboBox()
        self.style_box.addItems(list(presets.STYLES))
        self.format_box = QComboBox()
        self.format_box.addItems(list(presets.FORMATS))
        apply_btn = QPushButton("Appliquer le preset")
        apply_btn.clicked.connect(self.apply_preset)
        tl.addWidget(QLabel("Style :"))
        tl.addWidget(self.style_box)
        tl.addWidget(QLabel("Format :"))
        tl.addWidget(self.format_box)
        tl.addWidget(apply_btn)
        tl.addStretch(1)
        for text, fn in (("Charger config…", self.load_config), ("Sauver config…", self.save_config),
                         ("Générer", self.generate), ("Enregistrer .ohf…", self.save_ohf)):
            b = QPushButton(text)
            b.clicked.connect(fn)
            tl.addWidget(b)

        tabs = QTabWidget()
        for group in GROUPS:
            page = QWidget()
            form = QFormLayout(page)
            for p in [x for x in SCHEMA if x.group == group]:
                w = self._make_widget(p)
                w.setToolTip(p.help or p.label)
                self.widgets[p.key] = w
                form.addRow(p.label, w)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(page)
            tabs.addTab(scroll, group)

        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.status = QLabel("Prêt.")
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.addWidget(QLabel("Aperçu du profil"))
        rl.addWidget(self.preview)
        rl.addWidget(self.status)
        split = QSplitter(Qt.Orientation.Horizontal)
        split.addWidget(tabs)
        split.addWidget(right)
        split.setStretchFactor(0, 2)
        split.setStretchFactor(1, 3)

        central = QWidget()
        cl = QVBoxLayout(central)
        cl.addWidget(top)
        cl.addWidget(split)
        self.setCentralWidget(central)
        self.apply_preset()

    # ------------------------------------------------------------------ widgets
    def _make_widget(self, p):
        if p.kind == "bool":
            w = QCheckBox()
        elif p.kind == "choice":
            w = QComboBox()
            w.addItems(list(p.choices))
        elif p.kind == "str":
            w = QLineEdit()
        elif p.kind == "int":
            w = QSpinBox()
            w.setRange(int(p.lo), int(p.hi))
            w.setSingleStep(int(p.step))
        else:
            w = QDoubleSpinBox()
            w.setRange(p.lo, p.hi)
            w.setSingleStep(p.step)
            w.setDecimals(2)
        return w

    def set_value(self, key, value):
        w = self.widgets[key]
        if isinstance(w, QCheckBox):
            w.setChecked(bool(value))
        elif isinstance(w, QComboBox):
            w.setCurrentText(str(value))
        elif isinstance(w, QLineEdit):
            w.setText(str(value))
        else:
            w.setValue(value)

    def get_value(self, key):
        w = self.widgets[key]
        if isinstance(w, QCheckBox):
            return w.isChecked()
        if isinstance(w, QComboBox):
            return w.currentText()
        if isinstance(w, QLineEdit):
            return w.text()
        return w.value()

    def config(self) -> dict:
        return {k: coerce(k, self.get_value(k)) for k in self.widgets}

    def set_config(self, cfg: dict):
        for k, v in cfg.items():
            if k in self.widgets:
                self.set_value(k, v)

    # ------------------------------------------------------------------ actions
    def apply_preset(self):
        self.set_config(presets.build(self.style_box.currentText(), self.format_box.currentText()))
        self.status.setText("Preset appliqué.")

    def generate(self):
        try:
            text = generator.generate(self.config())
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Erreur de génération", str(exc))
            return None
        self.preview.setPlainText(text)
        issues = validator.validate(text)
        errs = validator.errors(issues)
        if errs:
            self.status.setText(f"⚠ {len(errs)} erreur(s) : {errs[0]}")
        else:
            self.status.setText(f"✔ Profil valide — {len(text.splitlines())} lignes, {len(issues)} avertissement(s)")
        return text

    def save_ohf(self):
        text = self.preview.toPlainText() or self.generate()
        if not text:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le profil", "profile.ohf", "OpenHoldem (*.ohf);;Tous (*)")
        if path:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            self.status.setText(f"Enregistré : {path}")

    def save_config(self):
        path, _ = QFileDialog.getSaveFileName(self, "Sauver la configuration", "config.json", "JSON (*.json)")
        if path:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(self.config(), fh, indent=2, ensure_ascii=False)

    def load_config(self):
        path, _ = QFileDialog.getOpenFileName(self, "Charger une configuration", "", "JSON (*.json)")
        if path:
            try:
                with open(path, encoding="utf-8") as fh:
                    self.set_config(json.load(fh))
            except Exception as exc:  # noqa: BLE001
                QMessageBox.critical(self, "Erreur", str(exc))


def run() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    app.setStyleSheet(DARK)
    w = MainWindow()
    w.show()
    return app.exec()
