from src.app_signer_tool import AppSignerTool
from src.desktop_clock import ColorSettingDialog
from src.file_tool import FileToolApp
from src.image_tool import ImageToolApp
from src.ip_info_tool import IpInfoToolApp
from src.rename_tool import RenameFileApp
from src.batch_create_folder import CreateFolderApp
from src.stick_note import StickyNoteApp
from src.password_generator import PasswordGeneratorApp
from src.rsa_key_generator import RSAKeyGeneratorApp
from src.hash_calculator import HashCalculatorApp

from src.const.fs_constants import FsConstants

app_instance_config = [
    {"key": "desktop_clock", "icon": FsConstants.BUTTON_TIME_ICON, "title": FsConstants.DESKTOP_CLOCK_WINDOW_TITLE,
     "class": ColorSettingDialog},
    {"key": "stick_note", "icon": FsConstants.BUTTON_STICK_NOTE_ICON, "title": FsConstants.STICK_NOTE_WINDOW_TITLE,
     "class": StickyNoteApp},
    {"key": "password_generator", "icon": FsConstants.BUTTON_PASSWORD_ICON, "title": FsConstants.PASSWORD_GENERATOR_TITLE,
     "class": PasswordGeneratorApp},
    {"key": "rsa_key_generator", "icon": FsConstants.BUTTON_RSA_KEY_GENERATOR_ICON,
     "title": FsConstants.RSA_KEY_GENERATOR_WINDOW_TITLE,
     "class": RSAKeyGeneratorApp},
    {"key": "rename_file", "icon": FsConstants.BUTTON_FILE_ICON, "title": FsConstants.FILE_RENAMER_WINDOW_TITLE,
     "class": RenameFileApp},
    {"key": "image_tool", "icon": FsConstants.BUTTON_HEIC_ICON, "title": FsConstants.IMAGE_TOOL_BUTTON_TITLE,
     "class": ImageToolApp},
    {"key": "file_tool", "icon": FsConstants.BUTTON_FILE_GENERATOR_ICON, "title": FsConstants.FILE_TOOL_WINDOW_TITLE,
     "class": FileToolApp},
    {"key": "create_folder", "icon": FsConstants.BUTTON_FOLDER_ICON, "title": FsConstants.CREATE_FOLDER_WINDOW_TITLE,
     "class": CreateFolderApp},
    {"key": "hash_calculator", "icon": FsConstants.BUTTON_HASH_CALCULATOR_ICON,
     "title": FsConstants.HASH_CALCULATOR_WINDOW_TITLE,
     "class": HashCalculatorApp},
    {"key": "ip_info_tool", "icon": FsConstants.BUTTON_NETWORK_TOOL_ICON,
         "title": FsConstants.NETWORK_TOOL_WINDOW_TITLE,
         "class": IpInfoToolApp},
    {"key": "app_signer_tool", "icon": FsConstants.BUTTON_APP_SIGNER_ICON,
     "title": FsConstants.APP_SIGNER_TOOL_WINDOW_TITLE,
     "class": AppSignerTool},
]
