# config.py
from src.batch_heic_jpg import HeicToJpgApp
from src.desktop_clock import ColorSettingDialog
from src.network_tool import NetworkInfoApp
from src.pic_conversion import PicConversionApp
from src.batch_file_renamer import RenameFileApp
from src.batch_create_folder import CreateFolderApp
from src.stick_note import StickyNoteApp
from src.password_generator import PasswordGeneratorApp
from src.file_comparator import FileComparatorApp
from src.file_generator import FileGeneratorApp
from src.file_encryptor import FileEncryptorApp
from src.rsa_key_generator import RSAKeyGeneratorApp
from src.hash_calculator import HashCalculatorApp
from src.port_killer import PortKillerApp
from src.port_scanner import PortScannerApp
from src.const.fs_constants import FsConstants

app_instance_config = [
    {"key": "desktop_clock", "icon": FsConstants.BUTTON_TIME_ICON, "title": FsConstants.DESKTOP_CLOCK_WINDOW_TITLE,
     "class": ColorSettingDialog},
    {"key": "stick_note", "icon": FsConstants.BUTTON_STICK_NOTE_ICON, "title": FsConstants.STICK_NOTE_WINDOW_TITLE,
     "class": StickyNoteApp},
    {"key": "password_generator", "icon": FsConstants.BUTTON_PASSWORD_ICON, "title": FsConstants.PASSWORD_GENERATOR_TITLE,
     "class": PasswordGeneratorApp},
    {"key": "create_folder", "icon": FsConstants.BUTTON_FOLDER_ICON, "title": FsConstants.CREATE_FOLDER_WINDOW_TITLE,
     "class": CreateFolderApp},
    {"key": "rename_file", "icon": FsConstants.BUTTON_FILE_ICON, "title": FsConstants.FILE_RENAMER_WINDOW_TITLE,
     "class": RenameFileApp},
    {"key": "heic_to_jpg", "icon": FsConstants.BUTTON_HEIC_ICON, "title": FsConstants.HEIC_JPG_BUTTON_TITLE,
     "class": HeicToJpgApp},
    {"key": "pic_conversion", "icon": FsConstants.BUTTON_PIC_ICON, "title": FsConstants.PIC_CONVERSION_WINDOW_TITLE,
     "class": PicConversionApp},
    {"key": "file_generator", "icon": FsConstants.BUTTON_FILE_GENERATOR_ICON, "title": FsConstants.FILE_GENERATOR_WINDOW_TITLE,
     "class": FileGeneratorApp},
    {"key": "file_comparator", "icon": FsConstants.BUTTON_FILE_COMPARATOR_ICON, "title": FsConstants.FILE_COMPARATOR_WINDOW_TITLE,
     "class": FileComparatorApp},
    {"key": "file_encryptor", "icon": FsConstants.BUTTON_FILE_ENCRYPTOR_ICON, "title": FsConstants.FILE_ENCRYPTOR_WINDOW_TITLE,
     "class": FileEncryptorApp},
    {"key": "rsa_key_generator", "icon": FsConstants.BUTTON_RSA_KEY_GENERATOR_ICON,
     "title": FsConstants.RSA_KEY_GENERATOR_WINDOW_TITLE,
     "class": RSAKeyGeneratorApp},
    {"key": "hash_calculator", "icon": FsConstants.BUTTON_HASH_CALCULATOR_ICON,
     "title": FsConstants.HASH_CALCULATOR_WINDOW_TITLE,
     "class": HashCalculatorApp},
    {"key": "port_killer", "icon": FsConstants.BUTTON_PORT_KILLER_ICON,
     "title": FsConstants.PORT_KILLER_WINDOW_TITLE,
     "class": PortKillerApp},
    {"key": "network_tool", "icon": FsConstants.BUTTON_NETWORK_TOOL_ICON,
         "title": FsConstants.NETWORK_TOOL_WINDOW_TITLE,
         "class": NetworkInfoApp},
]
