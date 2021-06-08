import cefpython3
import subprocess
import os
import shutil
import tinyWinToast


class PyinstallerCefpython:
    def __init__(self):
        self.no_suffix_script_name = "server"
        # cefpython3的包目录
        self.cef_dir = os.path.dirname(cefpython3.__file__)
        self.tinyWinToast_dir = os.path.dirname(tinyWinToast.__file__)
        # 获取cefpython3包下examples目录下的hello_world.py
        self.script_file = "server.py"

    def delete_before_generates(self):
        """删除之前打包生成的文件"""
        print("*******正在删除之前打包的生成文件....")
        try:
            shutil.rmtree("./dist")
            shutil.rmtree("./build")
            os.remove("{}.spec".format(self.no_suffix_script_name))
        except Exception as e:
            pass
        print("*******删除成功！")

    def script_to_exe(self):
        # 相当于执行打包命令： Pyinstaller hello_world.py
        print("*******开始打包cefpython3应用：", self.script_file)
        subprocess.run(
            "pyinstaller --version-file=version_info.txt --icon=favicon.ico --noconsole --hidden-import json {}".format(self.script_file))

    def copytree(self, src, dst, ignores_suffix_list=None):
        print("********正在复制将{}目录下的文件复制到{}文件夹下....".format(src, dst))
        os.makedirs(dst, exist_ok=True)
        names = [os.path.join(src, name) for name in os.listdir(src)]
        for name in names:
            exclude = False
            for suffix in ignores_suffix_list:
                if name.endswith(suffix):
                    exclude = True
                    continue
            if not exclude:
                if os.path.isdir(name):
                    new_dst = os.path.join(dst, os.path.basename(name))
                    shutil.copytree(
                        name, new_dst, ignore=shutil.ignore_patterns(*ignores_suffix_list))
                else:
                    shutil.copy(name, dst)

    def solve_dependence(self):
        print("*******解决依赖：复制依赖文件到执行文件的目录下....")
        self.copytree(self.cef_dir, "./dist/{}".format(self.no_suffix_script_name),
                      [".txt", ".py", ".log", "examples", ".pyd", "__"])
        # self.copytree(self.tinyWinToast_dir, "./dist/{}".format(self.no_suffix_script_name),
        #               [".txt", ".py", ".log", "examples", ".pyd", "__"])
        self.copytree('static', "./dist/{}/static".format(self.no_suffix_script_name),
                      [".txt", ".py", ".log", "examples", ".pyd", "__"])
        self.copytree('config', "./dist/{}/config".format(self.no_suffix_script_name),
                      [".txt", ".py", ".log", "examples", ".pyd", "__"])

    def exec_application(self):
        print("*******执行成功打包的应用....")
        subprocess.run("./dist/{0}/{0}.exe".format(self.no_suffix_script_name), stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def run(self):
        self.delete_before_generates()
        self.script_to_exe()
        self.solve_dependence()
        self.exec_application()


if __name__ == "__main__":
    PyinstallerCefpython().run()
