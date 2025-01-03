from src.app_signer_tool import AppSignerTool
from src.desktop_clock import ColorSettingDialog
from src.fast_sender import FastSenderApp
from src.file_tool import FileToolApp
from src.image_tool import ImageToolApp
from src.ip_info_tool import IpInfoToolApp
from src.create_folder import CreateFolderApp
from src.rename_tool import RenameToolApp
from src.stick_note import StickyNoteApp
from src.password_generator import PasswordGeneratorApp
from src.rsa_key_generator import RSAKeyGeneratorApp
from src.hash_calculator import HashCalculatorApp

from src.const.fs_constants import FsConstants

app_instance_config = [
        {
            "key": "desktop_clock",
            "icon": FsConstants.APP_ICON_DESKTOP_CLOCK,
            "title": FsConstants.APP_TITLE_DESKTOP_CLOCK,
            "class": ColorSettingDialog
        },
        {
            "key": "stick_note",
            "icon": FsConstants.APP_ICON_STICK_NOTE,
            "title": FsConstants.APP_TITLE_STICK_NOTE,
            "class": StickyNoteApp
        },
        {
            "key": "password_generator",
            "icon": FsConstants.APP_ICON_PASSWORD_GENERATOR,
            "title": FsConstants.APP_TITLE_PASSWORD_GENERATOR,
            "class": PasswordGeneratorApp
        },
        {
            "key": "rsa_key_generator",
            "icon": FsConstants.APP_ICON_RSA_GENERATOR,
            "title": FsConstants.APP_TITLE_RSA_GENERATOR,
            "class": RSAKeyGeneratorApp
        },
        {
            "key": "rename_tool",
            "icon": FsConstants.APP_ICON_RENAMER_TOOL,
            "title": FsConstants.APP_TITLE_RENAMER_TOOL,
            "class": RenameToolApp
        },
        {
            "key": "image_tool",
            "icon": FsConstants.APP_ICON_IMAGE_TOOL,
            "title": FsConstants.APP_TITLE_IMAGE_TOOL,
            "class": ImageToolApp
        },
        {
            "key": "file_tool",
            "icon": FsConstants.APP_ICON_FILE_TOOL,
            "title": FsConstants.APP_TITLE_FILE_TOOL,
            "class": FileToolApp
        },
        {
            "key": "create_folder",
            "icon": FsConstants.APP_ICON_CREATE_FOLDER,
            "title": FsConstants.APP_TITLE_CREATE_FOLDER,
            "class": CreateFolderApp
        },
        {
            "key": "hash_calculator",
            "icon": FsConstants.APP_ICON_HASH_CALCULATOR,
            "title": FsConstants.APP_TITLE_HASH_CALCULATOR,
            "class": HashCalculatorApp
        },
        {
            "key": "ip_info_tool",
            "icon": FsConstants.APP_ICON_IP_TOOL,
            "title": FsConstants.APP_TITLE_IP_TOOL,
            "class": IpInfoToolApp
        },
        {
            "key": "app_signer_tool",
            "icon": FsConstants.APP_ICON_APP_SIGNER,
            "title": FsConstants.APP_TITLE_APP_SIGNER,
            "class": AppSignerTool
        },
        {
            "key": "fast_sender",
            "icon": FsConstants.APP_ICON_FAST_SENDER,
            "title": FsConstants.APP_TITLE_FAST_SENDER,
            "class": FastSenderApp
        },
]
