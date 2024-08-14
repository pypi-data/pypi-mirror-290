import subprocess
import traceback
from loguru import logger



class AndroidControlException(Exception):...
class DeviceOutOfControl(AndroidControlException):...
class InstallException(AndroidControlException):...


class _ShellMixin:
    def __init__(self):
        self.device = None
        
    def _exec(self, cmd:str, timeout=None):
        try:
            logger.info(f'{self} EXEC "{cmd}"')
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=timeout)
            if result.stderr:
                logger.info(f'{self} EXEC "{cmd}" failed:{result.stderr}')
                return result.stderr.decode('utf-8')
        except Exception as e:
            logger.critical(f'=========== {self} adb run cmd {cmd} exception info begin '.rjust(50, "="))
            logger.critical(f'{traceback.format_exc()}')
            logger.critical(f'=========== {self} adb run cmd {cmd} exception info end '.rjust(50, "="))
            raise AndroidControlException(f"{self} adb run command {cmd} exception, msg: {e}")
        if "device offline" in result.stdout.decode("utf8"):
            raise AndroidControlException(f"{self} adb run command {cmd} exception, msg: device offline.")
        logger.debug(f"{self} EXEC {cmd} success, result:{result.stdout}.")
        return result.stdout.decode("utf-8").strip()
    
    def _under_control(self):
        if self._exec('adb devices').find(self.device) < 0:
            raise DeviceOutOfControl('{self} not found on controller')
        
    def _install(self, apk_abs):
        if not self._exec(f"adb -s {self.device} install -t {apk_abs}", timeout=120).endswith("Success"):
            raise InstallException(f"{self} install -t {apk_abs} failed.")


class AndroidApkInstaller(_ShellMixin):
    
    def __init__(self, sn):
        self.device = sn 
    
    def install(self, apk):
        self._install(apk_abs=apk)



if __name__ == "__main__":
    d1 = AndroidApkInstaller(sn="xxxxxx")
    d1.install("xxx.apk")