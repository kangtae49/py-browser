```sh
uv init py_browser
cd py_browser

uv venv
uv pip install wxpython
uv pip install pyinstaller
```

<http://github.com/new>

```sh
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/kangtae49/py-browser.git
git push -u origin main
```

```sh
uv run py_browser.py
```

```sh
.venv\Script\activate.bat
pyinstaller --onefile --windowed --add-data "resources;resources" --add-binary ".venv/Lib/site-packages/wx/WebView2Loader.dll;." --name py_browser.exe main.py
```