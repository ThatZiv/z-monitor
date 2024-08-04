import pyautogui as pag
import os
import subprocess
def alert(text: str, title: str = "z", type: str = "alert"):
    if os.name == "nt":
        notifStr = f"""
        [void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

        $objNotifyIcon = New-Object System.Windows.Forms.NotifyIcon

        $objNotifyIcon.Icon = [System.Drawing.SystemIcons]::Information
        $objNotifyIcon.BalloonTipIcon = "Info"
        $objNotifyIcon.BalloonTipText = "{text}"
        $objNotifyIcon.BalloonTipTitle = "{title}"
        $objNotifyIcon.Visible = $True

        $objNotifyIcon.ShowBalloonTip(10000)
        Start-Sleep 500
        """
        subprocess.run(["powershell", "-Command", notifStr])

    pag.alert(text, title)
