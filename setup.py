from cx_Freeze import setup, Executable

executables = [Executable('project.py',
                          targetName='hospital.exe',
                          base='Win32GUI',
                          icon='icon.ico')]

includes = ['PyQt5', 'sys', 'pymorphy2', "sqlite3", "datetime"]

zip_include_packages = ['PyQt5', 'sys', 'pymorphy2', "sqlite3", "datetime"]

include_files = ['appointment.py',
                 'certain_doctor.py',
                 'choice.py',
                 'database.py',
                 "doc.py",
                 "final_patients.py",
                 "help.png",
                 "info_for_doc.py",
                 "login.py",
                 "my_appointments.py",
                 "password_check.py",
                 "patients.py",
                 "phone_check.py",
                 "project.db",
                 "project.ui",
                 "registration.py"]

options = {
    'build_exe': {
        'include_msvcr': True,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',
        'include_files': include_files,
    }
}

setup(name='project',
      version='1.0.0',
      description='Project',
      executables=executables,
      options=options)
