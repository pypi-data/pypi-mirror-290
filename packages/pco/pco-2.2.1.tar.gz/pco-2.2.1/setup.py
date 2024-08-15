from setuptools import setup
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
from setuptools.command.develop import develop
import shutil
import glob
import sys
import platform
import os
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


# if sys.platform.startswith('win32'):
#     if platform.machine().lower().startswith('amd64'):
#         run_path = r'runtime/win_x64/bin'
#     else:
#         raise SystemError("pco.python is not supported for 32bit windows platforms architecture")
# elif sys.platform.startswith('linux'):
#     if platform.machine().lower().startswith("x86_64"):
#         run_path = r'runtime/lnx_amd64/lib'
#     elif platform.machine().lower().startswith("aarch64"):
#         run_path = r'runtime/lnx_arm64/lib'
#     else:
#         raise SystemError("pco.python is not supported for linux platform " + platform.machine())
# else:
#     raise SystemError("Package not supported on platform " + sys.platform)

run_path_win_x64 = r'runtime/win_x64/bin'
run_path_lnx_amd64 = r'runtime/lnx_amd64/lib'
run_path_lnx_arm64 = r'runtime/lnx_arm64/lib'

win_dlls = glob.glob(path.abspath(path.join(run_path_win_x64, 'pco_f*.dll')))
win_dlls += [
    path.abspath(path.join(run_path_win_x64, 'pco_recorder.dll')),
    path.abspath(path.join(run_path_win_x64, 'pco_conv.dll')),
    path.abspath(path.join(run_path_win_x64, 'sc2_cam.dll')),
    path.abspath(path.join(run_path_win_x64, 'sc2_clhs.dll')),
    path.abspath(path.join(run_path_win_x64, 'sc2_genicam.dll')),
    path.abspath(path.join(run_path_win_x64, 'sc2_gige.dll')),
    path.abspath(path.join(run_path_win_x64, 'sc2_cl_me4.dll'))
]

linux_so_amd64 = {}  # major copies
for f in glob.glob(path.abspath(path.join(run_path_lnx_amd64, "lib*.so.*.*.*.*"))):
    linux_so_amd64.update({f: path.basename(f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')])})
for f in glob.glob(path.abspath(path.join(run_path_lnx_amd64, "libOpenCL.so.*.*.*"))):
    linux_so_amd64.update({f: path.basename(f[:f[:f.rfind('.')].rfind('.')])})

# .so
for f in glob.glob(path.abspath(path.join(run_path_lnx_amd64, "libpco_f*.so.*.*.*.*"))):
    if path.basename(f[:f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')].rfind('.')]) == 'libpco_file.so':
        continue
    linux_so_amd64.update({f: path.basename(f[:f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')].rfind('.')])})

linux_so_arm64 = {}  # major copies
for f in glob.glob(path.abspath(path.join(run_path_lnx_arm64, "lib*.so.*.*.*.*"))):
    linux_so_arm64.update({f: path.basename(f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')])})
for f in glob.glob(path.abspath(path.join(run_path_lnx_arm64, "libOpenCL.so.*.*.*"))):
    linux_so_arm64.update({f: path.basename(f[:f[:f.rfind('.')].rfind('.')])})

# .so
for f in glob.glob(path.abspath(path.join(run_path_lnx_arm64, "libpco_f*.so.*.*.*.*"))):
    if path.basename(f[:f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')].rfind('.')]) == 'libpco_file.so':
        continue
    linux_so_arm64.update({f: path.basename(f[:f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')].rfind('.')])})


package_list = [
    './LICENSE.txt',
    './license.pdf',
    './license_3rdParty.pdf']

package_list += [path.join('pco', 'win_x64', path.basename(i)) for i in win_dlls]
package_list += [path.join('pco', 'lnx_amd64', linux_so_amd64[i]) for i in linux_so_amd64]
package_list += [path.join('pco', 'lnx_arm64', linux_so_arm64[i]) for i in linux_so_arm64]

# if sys.platform.startswith('win32'):
#     if platform.machine().lower().startswith('amd64'):

#     else:
#         raise SystemError("pco.python is not supported for 32bit windows platforms architecture")
# elif sys.platform.startswith('linux'):
#     if platform.machine().lower().startswith("x86_64"):

#     elif platform.machine().lower().startswith("aarch64"):

#     else:
#         raise SystemError("pco.python is not supported for linux platform " + platform.machine())


class RuntimeInstall(install):
    """Install setup to copy shared libraries"""

    def run(self):
        install.run(self)

        # copy windows dll
        if not path.exists(path.join(path.abspath(self.root), 'pco', 'win_x64')):
            os.mkdir(path.join(path.abspath(self.root), 'pco', 'win_x64'))
        dest_path = path.join(path.abspath(self.root), 'pco', 'win_x64')
        for file in win_dlls:
            shutil.copy(file, dest_path)
        shutil.copytree(path.abspath(path.join(run_path_win_x64, 'genicam')), path.abspath(path.join(dest_path, 'genicam')), dirs_exist_ok=True)

        # copy linux amd64
        if not path.exists(path.join(path.abspath(self.root), 'pco', 'lnx_amd64')):
            os.mkdir(path.join(path.abspath(self.root), 'pco', 'lnx_amd64'))
        dest_path = path.join(path.abspath(self.root), 'pco', 'lnx_amd64')
        for full_lib in linux_so_amd64:
            shutil.copy(full_lib, path.abspath(path.join(dest_path, linux_so_amd64[full_lib])))
        shutil.copytree(path.abspath(path.join(run_path_lnx_amd64, 'genicam')), path.abspath(path.join(dest_path, 'genicam')), dirs_exist_ok=True)

        # copy linux arm64
        if not path.exists(path.join(path.abspath(self.root), 'pco', 'lnx_arm64')):
            os.mkdir(path.join(path.abspath(self.root), 'pco', 'lnx_arm64'))
        dest_path = path.join(path.abspath(self.root), 'pco', 'lnx_arm64')
        for full_lib in linux_so_arm64:
            shutil.copy(full_lib, path.abspath(path.join(dest_path, linux_so_arm64[full_lib])))      
        shutil.copytree(path.abspath(path.join(run_path_lnx_arm64, 'genicam')), path.abspath(path.join(dest_path, 'genicam')), dirs_exist_ok=True)  




class RuntimeDevelop(develop):
    """Install setup to copy shared libraries in local directory """

    def run(self):
        develop.run(self)

        if sys.platform.startswith('win32'):
            run_path = 'C:\\pco_runtime\\win_x64\\bin'
            dest_path = path.join(path.abspath(this_directory), 'pco', 'win_x64')
        elif sys.platform.startswith('linux'):
            if platform.machine().lower().startswith("x86_64"):
                run_path = '/opt/pco/pco_runtime/lnx_amd64/lib'

                dest_path = path.join(path.abspath(this_directory), 'pco', 'lnx_amd64')
            elif platform.machine().lower().startswith("aarch64"):
                run_path = '/opt/pco/pco_runtime/lnx_arm64/lib'
                dest_path = path.join(path.abspath(this_directory), 'pco', 'lnx_arm64')
            else:
                raise SystemError("pco.python is not supported for linux platform " + platform.machine())
        else:
            raise SystemError("Package not supported on platform " + sys.platform)

        if not os.path.exists(dest_path):
            os.mkdir(dest_path)

        if sys.platform.startswith('win32'):
            win_dlls = []
            win_dlls = glob.glob(path.abspath(path.join(run_path, 'pco_f*.dll')))
            win_dlls += [
                path.abspath(path.join(run_path, 'pco_recorder.dll')),
                path.abspath(path.join(run_path, 'pco_conv.dll')),
                path.abspath(path.join(run_path, 'sc2_cam.dll')),
                path.abspath(path.join(run_path, 'sc2_clhs.dll')),
                path.abspath(path.join(run_path, 'sc2_genicam.dll')),
                path.abspath(path.join(run_path, 'sc2_gige.dll')),
                path.abspath(path.join(run_path, 'sc2_cl_me4.dll'))
            ]

            for file in win_dlls:
                shutil.copy(file, dest_path)
            shutil.copytree(path.abspath(path.join(run_path, 'genicam')), path.abspath(path.join(dest_path, 'genicam')), dirs_exist_ok=True)
        elif sys.platform.startswith('linux'):
            # .so.<major>
            linux_so = {}
            for f in glob.glob(path.abspath(path.join(run_path, "lib*.so.*.*.*.*"))):
                linux_so.update({f: path.basename(f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')])})
            for f in glob.glob(path.abspath(path.join(run_path, "libOpenCL.so.*.*.*"))):
                linux_so.update({f: path.basename(f[:f[:f.rfind('.')].rfind('.')])})

            # .so
            for f in glob.glob(path.abspath(path.join(run_path, "libpco_f*.so.*.*.*.*"))):
                if path.basename(f[:f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')].rfind('.')]) == 'libpco_file.so':
                    continue
                linux_so.update({f: path.basename(f[:f[:f[:f[:f.rfind('.')].rfind('.')].rfind('.')].rfind('.')])})

            for full_lib in linux_so:
                shutil.copy(full_lib, path.abspath(path.join(dest_path, linux_so[full_lib])))

                # .so.<major>.<minor>.<patch>
                # shutil.copy(full_lib, dest_path)
            shutil.copytree(path.abspath(path.join(run_path, 'genicam')), path.abspath(path.join(dest_path, 'genicam')), dirs_exist_ok=True)
        else:
            raise SystemError("Package not supported on platform " + sys.platform)
       

# this ensures that the version is always named after the tag
version = '2.2.1.dev1'
try:
    version = os.environ['CI_COMMIT_TAG']
except KeyError:
    pass

setup(
    name='pco',
    packages=['pco'],
    version = version,
    license='MIT',

    description='This class provides methods for using pco cameras.',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    author='Excelitas PCO GmbH',
    author_email='support.pco@excelitas.com',
    url='https://www.excelitas.com/de/product/pco-software-development-kits/',

    keywords=[
        'pco',
        'camera',
        'flim',
        'scmos',
        'microscopy'
    ],

    install_requires=[
        'numpy>=1.20'
    ],
    package_data={
        'pco': package_list,
    },

    cmdclass={'install': RuntimeInstall,
              'develop': RuntimeDevelop},

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 8',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',

        'Topic :: Scientific/Engineering'
    ]
)
