import cefpython3
import subprocess
import os
import shutil
import tinyWinToast
import posixpath


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
        shutil.rmtree("./dist")
        shutil.rmtree("./build")
        os.remove("{}.spec".format(self.no_suffix_script_name))
        print("*******删除成功！")

    def script_to_exe(self):
        # 相当于执行打包命令： Pyinstaller hello_world.py
        print("*******开始打包cefpython3应用：", self.script_file)
        subprocess.run(
            [
                "Pyinstaller",
                "--icon", "favicon.ico",
                "--version-file", "version_info.txt",
                "--hidden-import", "json",
                "-D",
                "-w",
                # "--add-data", ".\\static\\*;.\\static",
                # "--add-data", ".\\config\\*;.\\config",
                # "--add-data", "{}\\*;.".format(self.cef_dir),
                self.script_file
            ]
        )

    def copy(self, src, dst, ignores_suffix_list=None):
        print("********正在复制将{}目录下的文件复制到{}文件夹下....".format(src, dst))
        if not os.path.exists(dst):  # 如不存在目标目录则创建
            os.makedirs(dst)
        files = os.listdir(src)  # 获取文件夹中文件和目录列表
        os.sep = '/'
        for f in files:
            exclude = False
            for suffix in ignores_suffix_list:
                if f.endswith(suffix):
                    exclude = True
                    break
            abs_src_file = posixpath.join(src, f)
            abs_dst_file = posixpath.join(dst, f)
            if exclude:
                print('exclude '+abs_dst_file)
            else:
                if os.path.isdir(abs_src_file):  # 判断是否是文件夹
                    self.copy(
                        abs_src_file,
                        abs_dst_file,
                        ignores_suffix_list)  # 递归调用本函数
                else:
                    try:
                        shutil.copy(abs_src_file, abs_dst_file)  # 拷贝文件
                    except Exception as e:
                        print(e)
                    print('copied  '+abs_dst_file)

    def solve_dependence(self):
        print("*******解决依赖：复制依赖文件到执行文件的目录下....")
        self.copy(self.cef_dir, "./dist/{}".format(self.no_suffix_script_name),
                  [".txt", ".py", ".log", "examples", ".pyd", "__"])
        self.copy('static', "./dist/{}/static".format(self.no_suffix_script_name),
                  [".txt", ".py", ".log", "examples", ".pyd", "__"])
        self.copy('config', "./dist/{}/config".format(self.no_suffix_script_name),
                  [".txt", ".py", ".log", "examples", ".pyd", "__"])
        pass

    def exec_application(self):
        print("*******执行成功打包的应用....")
        subprocess.run("./dist/{0}/{0}.exe".format(self.no_suffix_script_name),
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

    def run(self):
        self.delete_before_generates()
        self.script_to_exe()
        self.solve_dependence()
        self.exec_application()


if __name__ == "__main__":
    PyinstallerCefpython().run()
    # PyinstallerCefpython().solve_dependence()
