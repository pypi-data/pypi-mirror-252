import sys as _sys
import os as _os
import simpleworkspace.loader as _sw
from simpleworkspace.utility.time import StopWatch as _StopWatch

class SetupToolsBundler:
    def __init__(self):
        from simpleworkspace.utility.module import ModuleInfo
        mainModule = ModuleInfo(_sys.modules['__main__'])
        self.entryPath = mainModule.pathInfo.Parent.AbsolutePath
        self.stopwatch = _StopWatch()

    def Command(self, args:list[str], title=None):
        import subprocess
        if(title is None):
            title = f'{args}'
        print(f"Executing command {title}...")
        with _StopWatch() as sw1:
            result = subprocess.run(args)
            if(result.returncode != 0): #something went bad
                raise RuntimeError(f"command failed... stdout: {result.stdout}; stderr: {result.stderr};")
        print(f' - Command finished in {sw1.GetElapsedSeconds(2)} seconds...')

    def _CleanUp(self):
        if(_os.path.isdir(f'{self.entryPath}/dist')):
            _sw.io.directory.RemoveTree(f'{self.entryPath}/dist')

    def Pipe_Init(self):
        self.stopwatch.Start()
        self._CleanUp() #clean leftovers from previous runs

    def Pipe_RunTests(self, testpath='tests/'):
        import unittest 
        print("Running unittests...")
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover(_os.path.join(self.entryPath, testpath))
        test_runner = unittest.TextTestRunner(verbosity=2)
        result = test_runner.run(test_suite)
        if(result.failures or result.errors): #something went bad
            raise Exception("Unittests failed!")

    def Pipe_IncrementPackageVersion(self):
        import toml
        def BumpMinorVersion(versionString):
            versionInfo = versionString.split(".")
            versionInfo[2] = str(int(versionInfo[2]) + 1)
            newVersion = ".".join(versionInfo)
            return newVersion
        
        ### increment module version ###
        pyProjectData = toml.load(f"{self.entryPath}/pyproject.toml")
        currentVersion = pyProjectData["project"]["version"]
        newVersion = BumpMinorVersion(currentVersion)
        pyProjectData["project"]["version"] = newVersion
        _sw.io.file.Create(f"{self.entryPath}/pyproject.toml", toml.dumps(pyProjectData))
        print(f"Incremented package version from {currentVersion} -> {newVersion}...")

    def Pipe_Build(self):
        ### build package ###
        self.Command([_sys.executable, '-m', 'build', self.entryPath])

    def Pipe_Install(self, developmentMode=False):
        ### install on computer as editable/dev mode ###
        if(developmentMode):
            self.Command([_sys.executable, "-m", "pip", "install", "--editable", self.entryPath])
        else:
            self.Command([_sys.executable, "-m", "pip", "install", self.entryPath])

    def Pipe_Publish(self, username:str, token:str):
        ### upload to pypi ###
        self.Command(
            [_sys.executable, "-m",
                "twine", "upload",
                "-u", username, 
                "-p", token,
                f"{self.entryPath}/dist/*"
            ], 
            title='Upload To PyPi')

    def Pipe_Finish(self):
        self._CleanUp()
        print(f"Installer finished! Elapsed: {self.stopwatch.GetElapsedSeconds(decimalPrecision=1)} seconds")


