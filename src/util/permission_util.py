import os
import sys

from PySide6.QtWidgets import QMessageBox

from src.util.common_util import CommonUtil


def is_admin():
    """
    检查当前程序是否以管理员身份运行
    """
    if CommonUtil.check_win_os():
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    elif CommonUtil.check_mac_os() or CommonUtil.check_linux_os():
        return os.geteuid() == 0
    return False


def run_as_admin():
    """
    以管理员权限重新运行程序
    """
    if CommonUtil.check_win_os():
        import ctypes
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)
    elif CommonUtil.check_mac_os():
        from PySide6.QtCore import QProcess
        process = QProcess()
        script = f'do shell script "{sys.executable} {" ".join(sys.argv)}" with administrator privileges'
        process.start("osascript", ["-e", script])
        process.waitForFinished()
        sys.exit(0)
    elif CommonUtil.check_linux_os():
        os.execvp("sudo", ["sudo", sys.executable] + sys.argv)

def check_admin():
    # 检查管理员权限
    if not is_admin():
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("权限不足")
        msg_box.setText("此程序需要以管理员权限运行。是否重新以管理员权限启动？")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            run_as_admin()
        #else:
            #sys.exit(0)

