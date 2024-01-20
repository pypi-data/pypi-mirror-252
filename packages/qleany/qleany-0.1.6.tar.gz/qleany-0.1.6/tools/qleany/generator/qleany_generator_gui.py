from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QTreeView,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QMenu,
    QHBoxLayout,
    QWidget,
    QGroupBox,
    QMessageBox,
    QCheckBox,
    QListView,
    QTextEdit,
    QSizePolicy,
    QLabel,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
)
from PySide6.QtCore import (
    Qt,
    QAbstractItemModel,
    QModelIndex,
    QCoreApplication,
    QSettings,
    QFileSystemWatcher,
    QTimer,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
import sys
import os
import yaml
import shutil
from pathlib import Path

full_path = Path(__file__).resolve().parent
full_path = f"{full_path}"
# add the current directory to the path so that we can import the generated files
sys.path.append(full_path)

# set the current directory to the generator directory
os.chdir(full_path)

import entities_generator
import dto_generator
import repositories_generator
import cqrs_generator
import controller_generator
import application_generator
import qml_generator
import entity_relationship_viewer
import presenter_generator

# this little application is a GUI for the generator

# This little application is a GUI for the generator. It allows you to select which file to generate in the middle view.
# It also allows you to preview the files in the "preview" folder by the python script before generating them properly.
# This GUI uses the qleany.yaml file placed at the root of your project and you can cherry-pick which files to generate.
# The states of the checkboxes are saved in the settings.yaml file.
# The qleany.yaml file is not modified by this UI.
# The manifest_temp.yaml file is a modified copy of the qleany.yaml file, but exists only for argument passing to the generator scripts.
# Any modification of the qleany.yaml file will be reflected in the UI.


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.settings = QSettings()

        self.manifest_file = self.settings.value("last_selected_manifest_path", "")
        self.temp_manifest_file = "temp/manifest_temp.yaml"
        self.settings_file = "temp/settings.yaml"

        # qleany file watcher
        self.watcher = QFileSystemWatcher([self.manifest_file])
        self.watcher.fileChanged.connect(self.on_manifest_file_changed)

        self.timer = QTimer()
        self.timer.setInterval(1000)  # check every second
        self.timer.timeout.connect(self.check_manifest_file)

        self.uncrustify_config_file = "../uncrustify.cfg"

        # geometry

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Qleany, the Qt Clean Architecture Generator")

        # UI
        self.manifest_refreshed_displayed = False
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        self.manifest_file_layout = QHBoxLayout()
        # set entity relationship window launch button

        self.entity_relationship_window_button = QPushButton(
            "Entity Relationship Viewer"
        )
        self.entity_relationship_window_button.clicked.connect(
            self.open_entity_relationship_window
        )
        self.manifest_file_layout.addWidget(self.entity_relationship_window_button)

        # set qleany.yml selector

        self.manifest_file_label = QLabel("Qleany YAML file:")
        self.manifest_file_layout.addWidget(self.manifest_file_label)
        self.manifest_file_text = QLabel(self.manifest_file)
        self.manifest_file_layout.addWidget(self.manifest_file_text)
        self.manifest_file_button = QPushButton("Select")
        self.manifest_file_button.clicked.connect(self.select_qleany_manifest_file)
        self.manifest_file_layout.addWidget(self.manifest_file_button)
        self.central_layout.addLayout(self.manifest_file_layout)
        self.central_layout.setStretch(0, 0)

        # set splitter for views
        self.splitter = QSplitter()
        self.central_layout.addWidget(self.splitter)
        self.central_layout.setStretch(1, 1)

        self.tree = QTreeView(self.splitter)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_menu)

        self.file_list_view = CheckableFileListView(self.splitter)

        self.text_box = QPlainTextEdit(self.splitter)
        self.text_box.setReadOnly(True)

        self.tree.clicked.connect(self.on_tree_item_click)
        self.tree.setAlternatingRowColors(True)
        self.tree.setEditTriggers(QTreeView.NoEditTriggers)

        self.button_layout = QHBoxLayout()

        self.tools_group_box = QGroupBox()
        self.tools_group_box.setTitle("Tools")
        self.tools_layout = QVBoxLayout()
        self.tools_group_box.setLayout(self.tools_layout)

        # Expand All

        self.btn_expand_all = QPushButton("Expand All", self)
        self.btn_expand_all.clicked.connect(self.expand_all)
        self.tools_layout.addWidget(self.btn_expand_all)

        # Clear preview folder

        self.btn_clear_preview_folder = QPushButton("Clear Preview Folder", self)
        self.btn_clear_preview_folder.clicked.connect(self.clear_preview_folder)
        self.tools_layout.addWidget(self.btn_clear_preview_folder)

        # Refresh

        self.btn_refresh = QPushButton("Refresh", self)
        self.btn_refresh.clicked.connect(self.refresh)
        self.tools_layout.addWidget(self.btn_refresh)

        self.button_layout.addWidget(self.tools_group_box)

        # Generate Entities

        self.generate_entities_group_box = QGroupBox()
        self.generate_entities_group_box.setTitle("Generate Entities")
        self.generate_entities_layout = QVBoxLayout()
        self.generate_entities_group_box.setLayout(self.generate_entities_layout)

        self.btn_list_entities = QPushButton("List", self)
        self.btn_list_entities.clicked.connect(self.list_entities)
        self.generate_entities_layout.addWidget(self.btn_list_entities)

        self.btn_preview_entities = QPushButton("Preview", self)
        self.btn_preview_entities.clicked.connect(self.preview_entities)
        self.generate_entities_layout.addWidget(self.btn_preview_entities)

        self.btn_generate_entities = QPushButton("Generate", self)
        self.btn_generate_entities.clicked.connect(self.generate_entities)
        self.generate_entities_layout.addWidget(self.btn_generate_entities)

        self.button_layout.addWidget(self.generate_entities_group_box)

        # disable preview and generate buttons if list button is not clicked once
        self.btn_preview_entities.setEnabled(False)
        self.btn_generate_entities.setEnabled(False)

        def enable_entities_buttons():
            self.btn_preview_entities.setEnabled(True)
            self.btn_generate_entities.setEnabled(True)

        self.btn_list_entities.clicked.connect(enable_entities_buttons)

        # Generate DTOs

        self.generate_dtos_group_box = QGroupBox()
        self.generate_dtos_group_box.setTitle("Generate DTOs")
        self.generate_dtos_layout = QVBoxLayout()
        self.generate_dtos_group_box.setLayout(self.generate_dtos_layout)

        self.btn_list_dtos = QPushButton("List", self)
        self.btn_list_dtos.clicked.connect(self.list_dtos)
        self.generate_dtos_layout.addWidget(self.btn_list_dtos)

        self.btn_preview_dtos = QPushButton("Preview", self)
        self.btn_preview_dtos.clicked.connect(self.preview_dtos)
        self.generate_dtos_layout.addWidget(self.btn_preview_dtos)

        self.btn_generate_dtos = QPushButton("Generate", self)
        self.btn_generate_dtos.clicked.connect(self.generate_dtos)
        self.generate_dtos_layout.addWidget(self.btn_generate_dtos)

        self.button_layout.addWidget(self.generate_dtos_group_box)

        # disable preview and generate buttons if list button is not clicked once
        self.btn_preview_dtos.setEnabled(False)
        self.btn_generate_dtos.setEnabled(False)

        def enable_dtos_buttons():
            self.btn_preview_dtos.setEnabled(True)
            self.btn_generate_dtos.setEnabled(True)

        self.btn_list_dtos.clicked.connect(enable_dtos_buttons)

        # Generate Repositories

        self.generate_repositories_group_box = QGroupBox()
        self.generate_repositories_group_box.setTitle("Generate Repositories")
        self.generate_repositories_layout = QVBoxLayout()
        self.generate_repositories_group_box.setLayout(
            self.generate_repositories_layout
        )

        self.btn_list_repositories = QPushButton("List", self)
        self.btn_list_repositories.clicked.connect(self.list_repositories)
        self.generate_repositories_layout.addWidget(self.btn_list_repositories)

        self.btn_preview_repositories = QPushButton("Preview", self)
        self.btn_preview_repositories.clicked.connect(self.preview_repositories)
        self.generate_repositories_layout.addWidget(self.btn_preview_repositories)

        self.btn_generate_repositories = QPushButton("Generate", self)
        self.btn_generate_repositories.clicked.connect(self.generate_repositories)
        self.generate_repositories_layout.addWidget(self.btn_generate_repositories)

        self.button_layout.addWidget(self.generate_repositories_group_box)

        # disable preview and generate buttons if list button is not clicked once
        self.btn_preview_repositories.setEnabled(False)
        self.btn_generate_repositories.setEnabled(False)

        def enable_repositories_buttons():
            self.btn_preview_repositories.setEnabled(True)
            self.btn_generate_repositories.setEnabled(True)

        self.btn_list_repositories.clicked.connect(enable_repositories_buttons)

        # Generate CQRS

        self.generate_cqrs_group_box = QGroupBox()
        self.generate_cqrs_group_box.setTitle("Generate CQRS")
        self.generate_cqrs_layout = QVBoxLayout()
        self.generate_cqrs_group_box.setLayout(self.generate_cqrs_layout)

        self.btn_list_cqrs = QPushButton("List", self)
        self.btn_list_cqrs.clicked.connect(self.list_cqrs)
        self.generate_cqrs_layout.addWidget(self.btn_list_cqrs)

        self.btn_preview_cqrs = QPushButton("Preview", self)
        self.btn_preview_cqrs.clicked.connect(self.preview_cqrs)
        self.generate_cqrs_layout.addWidget(self.btn_preview_cqrs)

        self.btn_generate_cqrs = QPushButton("Generate", self)
        self.btn_generate_cqrs.clicked.connect(self.generate_cqrs)
        self.generate_cqrs_layout.addWidget(self.btn_generate_cqrs)

        self.button_layout.addWidget(self.generate_cqrs_group_box)

        # disable preview and generate buttons if list button is not clicked once
        self.btn_preview_cqrs.setEnabled(False)
        self.btn_generate_cqrs.setEnabled(False)

        def enable_cqrs_buttons():
            self.btn_preview_cqrs.setEnabled(True)
            self.btn_generate_cqrs.setEnabled(True)

        self.btn_list_cqrs.clicked.connect(enable_cqrs_buttons)

        # Generate application

        self.generate_application_group_box = QGroupBox()
        self.generate_application_group_box.setTitle("Generate Application")
        self.generate_application_layout = QVBoxLayout()
        self.generate_application_group_box.setLayout(self.generate_application_layout)

        self.btn_list_application = QPushButton("List", self)
        self.btn_list_application.clicked.connect(self.list_application)
        self.generate_application_layout.addWidget(self.btn_list_application)

        self.btn_preview_application = QPushButton("Preview", self)
        self.btn_preview_application.clicked.connect(self.preview_application)
        self.generate_application_layout.addWidget(self.btn_preview_application)

        self.btn_generate_application = QPushButton("Generate", self)
        self.btn_generate_application.clicked.connect(self.generate_application)
        self.generate_application_layout.addWidget(self.btn_generate_application)

        self.button_layout.addWidget(self.generate_application_group_box)

        # disable preview and generate buttons if list button is not clicked once
        self.btn_preview_application.setEnabled(False)
        self.btn_generate_application.setEnabled(False)

        def enable_application_buttons():
            self.btn_preview_application.setEnabled(True)
            self.btn_generate_application.setEnabled(True)

        self.btn_list_application.clicked.connect(enable_application_buttons)

        # Generate Controllers

        self.generate_controllers_group_box = QGroupBox()
        self.generate_controllers_group_box.setTitle("Generate Controllers")
        self.generate_controllers_layout = QVBoxLayout()
        self.generate_controllers_group_box.setLayout(self.generate_controllers_layout)

        self.btn_list_controllers = QPushButton("List", self)
        self.btn_list_controllers.clicked.connect(self.list_controllers)
        self.generate_controllers_layout.addWidget(self.btn_list_controllers)

        self.btn_preview_controllers = QPushButton("Preview", self)
        self.btn_preview_controllers.clicked.connect(self.preview_controllers)
        self.generate_controllers_layout.addWidget(self.btn_preview_controllers)

        self.btn_generate_controllers = QPushButton("Generate", self)
        self.btn_generate_controllers.clicked.connect(self.generate_controllers)
        self.generate_controllers_layout.addWidget(self.btn_generate_controllers)

        self.button_layout.addWidget(self.generate_controllers_group_box)

        # disable preview and generate buttons if list button is not clicked once
        self.btn_preview_controllers.setEnabled(False)
        self.btn_generate_controllers.setEnabled(False)

        def enable_controllers_buttons():
            self.btn_preview_controllers.setEnabled(True)
            self.btn_generate_controllers.setEnabled(True)

        self.btn_list_controllers.clicked.connect(enable_controllers_buttons)

        # Generate Presenters

        self.generate_presenters_group_box = QGroupBox()
        self.generate_presenters_group_box.setTitle("Generate Presenters")
        self.generate_presenters_layout = QVBoxLayout()
        self.generate_presenters_group_box.setLayout(self.generate_presenters_layout)

        self.btn_list_presenters = QPushButton("List", self)
        self.btn_list_presenters.clicked.connect(self.list_presenters)
        self.generate_presenters_layout.addWidget(self.btn_list_presenters)

        self.btn_preview_presenters = QPushButton("Preview", self)
        self.btn_preview_presenters.clicked.connect(self.preview_presenters)
        self.generate_presenters_layout.addWidget(self.btn_preview_presenters)

        self.btn_generate_presenters = QPushButton("Generate", self)
        self.btn_generate_presenters.clicked.connect(self.generate_presenters)
        self.generate_presenters_layout.addWidget(self.btn_generate_presenters)

        self.button_layout.addWidget(self.generate_presenters_group_box)

        # disable preview and generate buttons if list button is not clicked once
        self.btn_preview_presenters.setEnabled(False)
        self.btn_generate_presenters.setEnabled(False)

        def enable_presenters_buttons():
            self.btn_preview_presenters.setEnabled(True)
            self.btn_generate_presenters.setEnabled(True)

        self.btn_list_presenters.clicked.connect(enable_presenters_buttons)

        # Generate QML

        self.generate_qml_group_box = QGroupBox()
        self.generate_qml_group_box.setTitle("Generate QML")
        self.generate_qml_layout = QVBoxLayout()
        self.generate_qml_group_box.setLayout(self.generate_qml_layout)

        self.btn_list_qml = QPushButton("List", self)
        self.btn_list_qml.clicked.connect(self.list_qml)
        self.generate_qml_layout.addWidget(self.btn_list_qml)

        self.btn_preview_qml = QPushButton("Preview", self)
        self.btn_preview_qml.clicked.connect(self.preview_qml)
        self.generate_qml_layout.addWidget(self.btn_preview_qml)

        self.btn_generate_qml = QPushButton("Generate", self)
        self.btn_generate_qml.clicked.connect(self.generate_qml)
        self.generate_qml_layout.addWidget(self.btn_generate_qml)

        self.button_layout.addWidget(self.generate_qml_group_box)

        # disable preview and generate buttons if list button is not clicked once
        self.btn_preview_qml.setEnabled(False)
        self.btn_generate_qml.setEnabled(False)

        def enable_qml_buttons():
            self.btn_preview_qml.setEnabled(True)
            self.btn_generate_qml.setEnabled(True)

        self.btn_list_qml.clicked.connect(enable_qml_buttons)

        # generate all

        self.generate_all_group_box = QGroupBox()
        self.generate_all_layout = QVBoxLayout()
        self.generate_all_group_box.setLayout(self.generate_all_layout)

        self.btn_list_all = QPushButton("List All", self)
        self.btn_list_all.clicked.connect(self.list_all)
        self.generate_all_layout.addWidget(self.btn_list_all)

        self.btn_preview_all = QPushButton("Preview All", self)
        self.btn_preview_all.clicked.connect(self.preview_all)
        self.generate_all_layout.addWidget(self.btn_preview_all)

        self.btn_generate_all = QPushButton("Generate All", self)
        self.btn_generate_all.clicked.connect(self.generate_all)
        self.generate_all_layout.addWidget(self.btn_generate_all)

        self.button_layout.addWidget(self.generate_all_group_box)

        # disable preview and generate buttons if list button is not clicked once
        self.btn_preview_all.setEnabled(False)
        self.btn_generate_all.setEnabled(False)

        def enable_all_buttons():
            self.btn_preview_all.setEnabled(True)
            self.btn_generate_all.setEnabled(True)

        self.btn_list_all.clicked.connect(enable_all_buttons)

        # add to layout

        button_widget = QWidget()
        button_widget.setLayout(self.button_layout)
        self.central_layout.addWidget(button_widget)
        self.central_layout.setStretch(0, 1)

        # select qleany file
        if self.manifest_file == "":
            self.select_qleany_manifest_file()
        elif not Path(self.manifest_file).exists():
            self.select_qleany_manifest_file()
        # set root path str
        self.root_path = str(Path(self.manifest_file).parent.resolve())

        # create temp manifest file under temp folder
        self.last_manifest_mtime = os.path.getmtime(self.manifest_file)

        self.create_temp_manifest_file()

        self.load_data()
        self.load_settings()
        self.timer.start()

    def on_manifest_file_changed(self, path):
        if self.manifest_refreshed_displayed:
            self.refresh()
            return
        self.manifest_refreshed_displayed = True
        QMessageBox.information(
            None, "File Changed", f"The file {path} has been changed. Refreshing now..."
        )
        self.manifest_refreshed_displayed = False

    def check_manifest_file(self):
        new_mtime = os.path.getmtime(self.manifest_file)
        if new_mtime != self.last_manifest_mtime:
            self.on_manifest_file_changed(self.manifest_file)
            self.last_manifest_mtime = new_mtime

    def clear_preview_folder(self):
        preview_path = Path(__file__).resolve().parent / "preview"
        if preview_path.exists():
            shutil.rmtree(preview_path)
        os.mkdir(preview_path)

    def refresh(self):
        self.clear_preview_folder()
        self.create_temp_manifest_file()
        self.load_data()
        self.load_settings()

    def open_entity_relationship_window(self):
        self.relationship_viewer_window = (
            entity_relationship_viewer.EntityRelationshipWindow(self.manifest_file)
        )
        self.relationship_viewer_window.show()

    # all

    def list_all(self):
        list = []
        list.extend(
            entities_generator.get_files_to_be_generated(self.temp_manifest_file)
        )
        list.extend(dto_generator.get_files_to_be_generated(self.temp_manifest_file))
        list.extend(
            repositories_generator.get_files_to_be_generated(self.temp_manifest_file)
        )
        list.extend(cqrs_generator.get_files_to_be_generated(self.temp_manifest_file))
        list.extend(
            presenter_generator.get_files_to_be_generated(self.temp_manifest_file)
        )
        list.extend(
            controller_generator.get_files_to_be_generated(self.temp_manifest_file)
        )
        list.extend(
            application_generator.get_files_to_be_generated(self.temp_manifest_file)
        )
        self.text_box.setPlainText("All files:\n\n")
        self.text_box.appendPlainText("\n".join(list))
        self.file_list_view.list_files(list)

    def preview_all(self):
        self.clear_preview_folder()
        self.list_all()
        entities_generator.preview_entity_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        dto_generator.preview_dto_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        repositories_generator.preview_repository_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        cqrs_generator.preview_cqrs_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        presenter_generator.preview_presenter_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        controller_generator.preview_controller_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        application_generator.preview_application_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )

        self.text_box.setPlainText(
            f"Preview folder cleared beforehand. All files previewed at {Path(self.root_path,).resolve()}/qleany_preview/ folder"
        )

    def generate_all(self):
        file_list = []
        file_list.extend(
            entities_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        )
        file_list.extend(
            dto_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        )
        file_list.extend(
            repositories_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        )
        file_list.extend(
            cqrs_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        )
        file_list.extend(
            controller_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        )
        file_list.extend(
            presenter_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        )
        file_list.extend(
            application_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        )
        file_list.extend(
            qml_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        )

        if self.display_overwrite_confirmation(file_list):
            self.list_all()
            entities_generator.generate_entity_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            dto_generator.generate_dto_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            repositories_generator.generate_repository_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            cqrs_generator.generate_cqrs_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            controller_generator.generate_controller_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            application_generator.generate_application_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            qml_generator.generate_qml_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )

            self.text_box.setPlainText("All files generated")

    # entities functions

    def list_entities(self):
        list = entities_generator.get_files_to_be_generated(self.temp_manifest_file)
        self.text_box.clear()
        self.text_box.setPlainText("Entities:\n\n")
        self.text_box.appendPlainText("\n".join(list))
        self.file_list_view.list_files(list)

    def preview_entities(self):
        self.list_entities()
        entities_generator.preview_entity_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        self.text_box.clear()
        self.text_box.setPlainText(
            f'Preview folder NOT cleared beforehand. Do it if needed by clicking on "Clear Preview Folder" button.'
        )
        self.text_box.appendPlainText(
            f" Entities previewed at {Path(__file__).resolve().parent}/preview/ folder"
        )

    def generate_entities(self):
        self.list_entities()
        if self.display_overwrite_confirmation(
            entities_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        ):
            entities_generator.generate_entity_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            self.text_box.clear()
            self.text_box.setPlainText("Entities generated")

    # DTOs functions

    def list_dtos(self):
        list = dto_generator.get_files_to_be_generated(self.temp_manifest_file)
        self.text_box.clear()
        self.text_box.setPlainText("DTOs:\n\n")
        self.text_box.appendPlainText("\n".join(list))
        self.file_list_view.list_files(list)

    def preview_dtos(self):
        self.list_dtos()
        dto_generator.preview_dto_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        self.text_box.clear()
        self.text_box.setPlainText(
            f'Preview folder NOT cleared beforehand. Do it if needed by clicking on "Clear Preview Folder" button.'
        )
        self.text_box.appendPlainText(
            f" DTOs previewed at {Path(__file__).resolve().parent}/preview/ folder"
        )

    def generate_dtos(self):
        self.list_dtos()
        if self.display_overwrite_confirmation(
            dto_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        ):
            dto_generator.generate_dto_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            self.text_box.clear()
            self.text_box.setPlainText("DTOs generated")

    # Repositories functions

    def list_repositories(self):
        list = repositories_generator.get_files_to_be_generated(self.temp_manifest_file)
        self.text_box.clear()
        self.text_box.setPlainText("Repositories:\n\n")
        self.text_box.appendPlainText("\n".join(list))
        self.file_list_view.list_files(list)

    def preview_repositories(self):
        self.list_repositories()
        repositories_generator.preview_repository_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        self.text_box.clear()
        self.text_box.setPlainText(
            f'Preview folder NOT cleared beforehand. Do it if needed by clicking on "Clear Preview Folder" button.'
        )
        self.text_box.appendPlainText(
            f" Repositories previewed at {Path(__file__).resolve().parent}/qleany_preview/ folder"
        )

    def generate_repositories(self):
        self.list_repositories()
        if self.display_overwrite_confirmation(
            repositories_generator.get_files_to_be_generated(
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
            )
        ):
            repositories_generator.generate_repository_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            self.text_box.clear()
            self.text_box.setPlainText("Repositories generated")

    # CQRS functions

    def list_cqrs(self):
        list = cqrs_generator.get_files_to_be_generated(self.temp_manifest_file)
        self.text_box.setPlainText("CQRS:\n\n")
        self.text_box.appendPlainText("\n".join(list))
        self.file_list_view.list_files(list)

    def preview_cqrs(self):
        self.list_cqrs()
        cqrs_generator.preview_cqrs_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        self.text_box.clear()
        self.text_box.setPlainText(
            f'Preview folder NOT cleared beforehand. Do it if needed by clicking on "Clear Preview Folder" button.'
        )
        self.text_box.appendPlainText(
            f" CQRS files previewed at {Path(__file__).resolve().parent}/qleany_preview/ folder"
        )

    def generate_cqrs(self):
        self.list_cqrs()
        if self.display_overwrite_confirmation(
            cqrs_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        ):
            cqrs_generator.generate_cqrs_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            self.text_box.clear()
            self.text_box.setPlainText("CQRS generated")

    # Presenters functions

    def list_presenters(self):
        list = presenter_generator.get_files_to_be_generated(self.temp_manifest_file)
        self.text_box.clear()
        self.text_box.setPlainText("Presenters:\n\n")
        self.text_box.appendPlainText("\n".join(list))
        self.file_list_view.list_files(list)

    def preview_presenters(self):
        self.list_presenters()
        presenter_generator.preview_presenter_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        self.text_box.clear()
        self.text_box.setPlainText(
            f'Preview folder NOT cleared beforehand. Do it if needed by clicking on "Clear Preview Folder" button.'
        )
        self.text_box.appendPlainText(
            f" Presenters previewed at {Path(__file__).resolve().parent}/qleany_preview/ folder"
        )

    def generate_presenters(self):
        self.list_presenters()
        if self.display_overwrite_confirmation(
            presenter_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        ):
            presenter_generator.generate_presenter_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            self.text_box.clear()
            self.text_box.setPlainText("Presenters generated")

    # Controllers functions

    def list_controllers(self):
        list = controller_generator.get_files_to_be_generated(self.temp_manifest_file)
        self.text_box.clear()
        self.text_box.setPlainText("Controllers to be generated:\n\n")
        self.text_box.appendPlainText("\n".join(list))
        self.file_list_view.list_files(list)

    def preview_controllers(self):
        self.list_controllers()
        controller_generator.preview_controller_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        self.text_box.clear()
        self.text_box.setPlainText(
            f'Preview folder NOT cleared beforehand. Do it if needed by clicking on "Clear Preview Folder" button.'
        )
        self.text_box.appendPlainText(
            f" Controllers previewed at {Path(__file__).resolve().parent}/qleany_preview/ folder"
        )

    def generate_controllers(self):
        self.list_controllers()
        if self.display_overwrite_confirmation(
            controller_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        ):
            controller_generator.generate_controller_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            self.text_box.clear()
            self.text_box.setPlainText("Controllers generated")

    # Application functions

    def list_application(self):
        list = application_generator.get_files_to_be_generated(self.temp_manifest_file)
        self.text_box.clear()
        self.text_box.setPlainText("Application:\n\n")
        self.text_box.appendPlainText("\n".join(list))
        self.file_list_view.list_files(list)

    def preview_application(self):
        self.list_application()
        application_generator.preview_application_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        self.text_box.clear()
        self.text_box.setPlainText(
            f'Preview folder NOT cleared beforehand. Do it if needed by clicking on "Clear Preview Folder" button.'
        )
        self.text_box.appendPlainText(
            f" Application previewed at {Path(__file__).resolve().parent}/preview/ folder"
        )

    def generate_application(self):
        self.list_application()
        if self.display_overwrite_confirmation(
            application_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        ):
            application_generator.generate_application_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            self.text_box.clear()
            self.text_box.setPlainText("Application generated")

    # QML functions

    def list_qml(self):
        list = qml_generator.get_files_to_be_generated(self.temp_manifest_file)
        self.text_box.clear()
        self.text_box.setPlainText("QML:\n\n")
        self.text_box.appendPlainText("\n".join(list))
        self.file_list_view.list_files(list)

    def preview_qml(self):
        self.list_qml()
        qml_generator.preview_qml_files(
            self.root_path,
            self.temp_manifest_file,
            self.file_list_view.fetch_file_states(),
            self.uncrustify_config_file,
        )
        self.text_box.clear()
        self.text_box.setPlainText(
            f'Preview folder NOT cleared beforehand. Do it if needed by clicking on "Clear Preview Folder" button.'
        )
        self.text_box.appendPlainText(
            f" QML files previewed at {Path(__file__).resolve().parent}/qleany_preview/ folder"
        )

    def generate_qml(self):
        self.list_qml()
        if self.display_overwrite_confirmation(
            qml_generator.get_files_to_be_generated(
                self.temp_manifest_file, self.file_list_view.fetch_file_states()
            )
        ):
            qml_generator.generate_qml_files(
                self.root_path,
                self.temp_manifest_file,
                self.file_list_view.fetch_file_states(),
                self.uncrustify_config_file,
            )
            self.text_box.clear()
            self.text_box.setPlainText("QML generated")

    def display_overwrite_confirmation(self, files: list):
        # join self.root_path and file
        files = [os.path.join(self.root_path, file) for file in files]

        existing_files = [file for file in files if os.path.isfile(file)]

        # format the file list as a string for display
        fileList = "\n".join(existing_files)

        dialog = QDialog()
        layout = QVBoxLayout(dialog)
        if existing_files:  # if the list has something in it
            label = QLabel()
            label.setText(
                f"The following files exist and will be overwritten:\nAre you sure you want to continue?"
            )

            layout.addWidget(label)

            dialog.setWindowTitle("Overwrite Confirmation")

            # add the plain text edit to the dialog
            textEdit = QPlainTextEdit()
            textEdit.setReadOnly(True)
            textEdit.setPlainText(f"{fileList}\n")
            layout.addWidget(textEdit)
            dialog.resize(700, 300)
        else:
            label = QLabel()
            label.setText(f"Are you sure you want to continue?\n")

            layout.addWidget(label)

            label.setWindowTitle("Confirmation")

        # create Ok and Cancel buttons
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)
        layout.addWidget(buttonBox)

        returnValue = dialog.exec()
        if returnValue == QDialog.Accepted:
            return True
        else:
            return False

    # Expand all

    def expand_all(self):
        self.tree.expandAll()

    def create_temp_manifest_file(self):
        with open(self.manifest_file) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        # create temp folder if not exists
        Path(self.temp_manifest_file).parent.mkdir(parents=True, exist_ok=True)

        with open(self.temp_manifest_file, "w") as file:
            yaml.dump(data, file)

    def load_data(self):
        with open(self.temp_manifest_file) as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)

        self.model = self.create_model(self.data)
        self.tree.setModel(self.model)
        self.tree.model().itemChanged.connect(self.handleItemChanged)

        self.tree.setColumnWidth(0, 200)

    def create_model(self, data, parent=None):
        if parent is None:
            parent = QStandardItemModel()
            parent.setHorizontalHeaderLabels(["Key", "Value"])
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    item = QStandardItem(key)
                    self.create_model(value, item)
                    parent.appendRow([item, QStandardItem()])
                else:
                    key_item = QStandardItem(str(key))
                    value_item = QStandardItem(str(value))
                    parent.appendRow([key_item, value_item])
        elif isinstance(data, list):
            for i, value in enumerate(data):
                if isinstance(value, (dict, list)):
                    item = QStandardItem(str(i))
                    self.create_model(value, item)
                    parent.appendRow([item, QStandardItem()])
                else:
                    key_item = QStandardItem(str(i))
                    value_item = QStandardItem(str(value))
                    parent.appendRow([key_item, value_item])

        return parent

    def on_tree_item_click(self, index):
        # TODO: Generate the list of files based on item clicked and display in text_box
        # self.text_box.setPlainText("Generated files:")
        pass

    def on_check_item_changed(self, state, key):
        # Load the current state of the YAML file
        with open(self.temp_manifest_file) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        # Write the updated state back to the YAML file
        with open(self.temp_manifest_file, "w") as file:
            yaml.dump(data, file)

    def handleItemChanged(self, item):
        # This function will be called whenever a checkbox's state is changed
        if item.isCheckable():
            # We navigate up the tree to construct the keys
            keys = []
            index = item.index()
            while index.isValid():
                text = self.model.itemFromIndex(index).text()
                if not text:
                    text = self.model.itemFromIndex(index).data()
                keys.append(text)
                index = index.parent()
            keys = keys[
                ::-1
            ]  # reverse the keys and exclude the first one, which is the root node

            # Now that we have the keys, let's update the data and the yaml file
            data = self.data
            for key in keys[:-1]:
                if isinstance(data, list):
                    key = int(key)
                data = data[key]
            # The last key corresponds to the checkbox
            data[keys[-1]] = item.checkState() == Qt.Checked

            # Now we update the yaml file
            with open(self.temp_manifest_file, "w") as file:
                yaml.dump(self.data, file)

            self.save_settings()

    def get_generate_items(self, data, path=None):
        if path is None:
            path = []

        if isinstance(data, dict):
            for key, value in data.items():
                new_path = path + [key]
                yield from self.get_generate_items(value, new_path)
        elif isinstance(data, list):
            for index, value in enumerate(data):
                new_path = path + [index]
                yield from self.get_generate_items(value, new_path)

    def save_settings(self):
        # Extracts the "generate" items and their paths
        generate_items = list(self.get_generate_items(self.data))

        # clear the settings file
        with open(self.settings_file, "w") as file:
            file.write("")

        # create temp folder if not exists
        Path(self.settings_file).parent.mkdir(parents=True, exist_ok=True)

        # Saves the items to the settings file
        with open(self.settings_file, "w") as file:
            yaml.dump(generate_items, file)

    def load_settings(self):
        # Load the saved state from the settings file
        try:
            with open(self.settings_file, "r") as file:
                saved_generate_items = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            return

        # Apply the saved state to self.data

        for path, value in saved_generate_items:
            for key in path[:-1]:
                try:
                    item = self.data[key]
                except KeyError:
                    break
                except IndexError:
                    break

            self.data[path[-1]] = value

        # Update self.temp_manifest_file
        with open(self.temp_manifest_file, "w") as file:
            yaml.dump(self.data, file)

        # Update the tree view
        self.model = self.create_model(self.data)
        self.tree.setModel(self.model)
        self.tree.model().itemChanged.connect(self.handleItemChanged)

    def show_launch_dialog(self):
        title = "Welcome to Qleany, the Qt Clean Architecture generator GUI!"

        message = """
        Cute Clean Architecture generator GUI\n
        \n
        This little application is a GUI for the generator. It allows you to select which file to generate in the middle view.\n
        It also allows you to preview the files in the "preview" folder by the python script before generating them properly.\n
        This GUI uses the qleany.yaml file placed at the root of your project and you can cherry-pick which files to generate.\n
        The states of the checkboxes are saved in the settings.yaml file.\n
        The qleany.yaml file is not modified by this UI.\n
        The manifest_temp.yaml file is a modified copy of the qleany.yaml file, but exists only for argument passing to the generator scripts.\n
        Any modification of the qleany.yaml file will be reflected in the UI.\n
        """
        settings = QSettings()
        checkbox = QCheckBox("Do not show this message again.")
        checkbox.setChecked(not settings.value("show_dialog", True, bool))
        msgBox = QMessageBox(self)
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        msgBox.setCheckBox(checkbox)

        # Show the message box at the foreground of the main window
        msgBox.setWindowModality(Qt.WindowModal)

        msgBox.exec()

        # Save the user's preference
        settings.setValue("show_dialog", not checkbox.isChecked())

    def open_menu(self, position):
        indexes = self.tree.selectedIndexes()
        if indexes:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

            menu = QMenu()
            if level == 0:
                action = menu.addAction("Expand All")
                action.triggered.connect(self.expand_completely_item)
                # action = menu.addAction("Collapse All")
                # action.triggered.connect(self.collapse_completely_item)
            menu.exec_(self.tree.viewport().mapToGlobal(position))

    def expand_completely_item(self):
        selected = self.tree.selectionModel().selectedIndexes()[0]
        self.tree.expandRecursively(selected)

    # def collapse_completely_item(self):
    #     selected = self.tree.selectionModel().selectedIndexes()[0]
    #     self.tree.collapseRecursively(selected)

    def select_qleany_manifest_file(self):
        start_path = self.settings.value("last_selected_manifest_path", "")
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select qleany.yaml",
            start_path,
            "YAML Files (*.yml, *.yaml);;All Files (*)",
            options=options,
        )

        if file_name:
            self.settings.setValue("last_selected_manifest_path", file_name)
            self.manifest_file_text.setText(file_name)
            self.manifest_file = file_name
            self.root_path = str(Path(self.manifest_file).parent.resolve())
            self.create_temp_manifest_file()
            self.load_data()
            self.load_settings()
            self.list_all()


def main():
    full_path = Path(__file__).resolve().parent

    # add the current directory to the path so that we can import the generated files
    sys.path.append(full_path)

    # set the current directory to the generator directory
    os.chdir(full_path)

    app = QApplication(sys.argv)

    QCoreApplication.setOrganizationName("qleany-generator")
    QCoreApplication.setOrganizationDomain("qleany-generator.eu")
    QCoreApplication.setApplicationName("qleany-generator")

    window = MainWindow()
    # make the window stay on top
    window.show()

    # Load settings and show the launch dialog
    settings = QSettings()
    show_dialog = settings.value("show_dialog", True, bool)

    if show_dialog:
        window.show_launch_dialog()

    sys.exit(app.exec())


# List view with checkboxes


class CheckableFileListView(QWidget):
    def __init__(self, parent=None):
        super(CheckableFileListView, self).__init__(parent)
        self.settings = QSettings()

        self.fileListView = QListView(self)
        self.model = QStandardItemModel(self.fileListView)

        self.checkAllButton = QPushButton("Check All", self)
        self.checkAllButton.clicked.connect(self.check_all)

        self.uncheckAllButton = QPushButton("Uncheck All", self)
        self.uncheckAllButton.clicked.connect(self.uncheck_all)

        layout = QVBoxLayout(self)
        layout.addWidget(self.fileListView)
        layout.addWidget(self.checkAllButton)
        layout.addWidget(self.uncheckAllButton)

        self.fileListView.setModel(self.model)

    def list_files(self, file_paths):
        self.model.clear()

        for file_path in file_paths:
            item = QStandardItem(file_path)
            item.setCheckable(True)

            # Load saved check state, default to checked

            check_state_bool = self.settings.value(
                f"file_check_state/{file_path}", Qt.Checked, type=bool
            )
            if check_state_bool:
                check_state = Qt.Checked
            else:
                check_state = Qt.Unchecked

            item.setCheckState(check_state)

            self.model.appendRow(item)

        # Connect to the itemChanged signal
        self.model.itemChanged.connect(self.handle_item_changed)

    def handle_item_changed(self, item):
        # Save the check state of the item
        self.settings.setValue(
            f"file_check_state/{item.text()}", item.checkState() == Qt.Checked
        )

    def fetch_file_states(self):
        file_states = {}

        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            file_states[item.text()] = item.checkState() == Qt.Checked

        return file_states

    def get_selected_files(self):
        selected_files = []
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            if item.checkState() == Qt.Checked:
                selected_files.append(item.text())
        return selected_files

    def check_all(self):
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            item.setCheckState(Qt.Checked)

    def uncheck_all(self):
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            item.setCheckState(Qt.Unchecked)


# This is the entry point of the script

if __name__ == "__main__":
    full_path = Path(__file__).resolve().parent

    # add the current directory to the path so that we can import the generated files
    sys.path.append(full_path)

    # set the current directory to the generator directory
    os.chdir(full_path)

    main()
