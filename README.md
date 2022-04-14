# emby-metadata

## 安装模块

```shell
pip install beautifulsoup4
pip install tqdm
pip install cfscrape
pip install pysocks
```

## BeautifulSoup

- 文档 https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

## Flask

- 安装flask

```shell
C:\Python310\python.exe -m pip install --upgrade pip
pip install flask
```

- 新建app.py

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"
```

- index.html

```html

```

- 运行

```shell
C:\Python310\python.exe -m flask run
```

- 访问

Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)
