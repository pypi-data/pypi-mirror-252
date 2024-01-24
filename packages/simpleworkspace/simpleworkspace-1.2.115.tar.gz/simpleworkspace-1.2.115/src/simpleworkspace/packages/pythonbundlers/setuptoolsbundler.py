# import subprocess
# import sys
# import os
# import simpleworkspace.loader as sw
# import toml
# import TwineCredentials
# import unittest 
# from simpleworkspace.utility.module import ModuleInfo
# from simpleworkspace.utility.time import StopWatch
# from typing import Callable
# from simpleworkspace.logproviders import StdoutLogger
# from logging import Logger

# class SetupToolsBundler:
#     def __init__(self):
#         mainModule = ModuleInfo(sys.modules['__main__'])
#         self.entryPath = mainModule.pathInfo.AbsolutePath
#         self.logger = StdoutLogger.CreateBasicHandler()

#     def UseLogger(self, logger:Logger):
#         pass
#     def Command(self, args:list[str], title=None):
#         if(title is None):
#             title = f'{args}'
#         print(f'\nExecuting Command: {title}')
#         with StopWatch() as sw1:
#             subprocess.run(args)
#         print(f' - Command finished in {sw1.GetElapsedSeconds(decimalPrecision=1)} seconds\n')

#     def _CleanUp(self):
#         if(os.path.isdir(self.entryPath + '/dist')):
#             sw.io.directory.RemoveTree(self.entryPath + "/dist")

#     def Pipe_Init(self):
#         self._CleanUp() #clean leftovers from previous runs

#     def Pipe_RunTests(self):
#         ### unittests ###
#         test_loader = unittest.TestLoader()
#         test_suite = test_loader.discover(self.entryPath + "/tests/")
#         test_runner = unittest.TextTestRunner(verbosity=2)
#         result = test_runner.run(test_suite)
#         print(result)
#         if(result.failures or result.errors): #something went bad
#             raise Exception("Unittests failed!")

#     def Pipe_IncrementPackageVersion(self):
#         ### increment module version ###
#         pyProjectData = toml.load("./pyproject.toml")
#         versionInfo = pyProjectData["project"]["version"].split(".")
#         versionInfo[2] = str(int(versionInfo[2]) + 1)
#         pyProjectData["project"]["version"] = ".".join(versionInfo)
#         sw.io.file.Create("./pyproject.toml", toml.dumps(pyProjectData))

#     def Pipe_Build(self):
#         ### build package ###
#         self.Command([sys.executable, '-m', 'build', '.'])

#     def Pipe_Publish(self):
#         ### upload to pypi ###
#         self.Command(
#             [sys.executable, "-m",
#                 "twine", "upload",
#                 "-u", TwineCredentials.username, 
#                 "-p", TwineCredentials.token,
#                 "dist/*"
#             ], 
#             title='Upload To PyPi')
        
#     def Pipe_Install(self):
#         ### install on computer as editable/dev mode ###
#         self.Command([sys.executable, "-m", 
#                 "pip", "install", "--editable", "."])

#     def Pipe_Finish(self):
#         self._CleanUp()

#     def Run(self):
#         sw_run = StopWatch()
#         sw_run.Start()
#         self.Pipe_Init()
#         self.Pipe_RunTests()
#         self.Pipe_IncrementPackageVersion()
#         self.Pipe_Build()
#         self.Pipe_Install()
#         self.Pipe_Publish()
#         self.Pipe_Finish()
#         print(f"Installer finished! Elapsed: {sw_run.GetElapsedSeconds(decimalPrecision=1)} seconds")

# installer = SetupToolsBundler()
# installer.Run()