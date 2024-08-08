import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=%s' % 'MyFlaskApp',
    '--onefile',
    '--windowed',
    'app.py',
    '--log-level=DEBUG'
])