# emby-metadata

### 安装模块

```shell
python.exe -m pip install --upgrade pip
pip install beautifulsoup4
pip install tqdm
pip install cfscrape
pip install pysocks
```

### BeautifulSoup

- 文档 https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

### Flask

- 安装flask

```shell
python.exe -m pip install --upgrade pip
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
D:\PycharmProjects\emby-metadata\venv\Scripts\python.exe -m flask run
```

- 访问

Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)

### FAQ

- 无法加载文件 \venv\Scripts\activate.ps1，因为在此系统上禁止运行脚本。

```shell
Windows PowerShell
版权所有 (C) Microsoft Corporation。保留所有权利。

尝试新的跨平台 PowerShell https://aka.ms/pscore6

PS C:\WINDOWS\system32> get-ExecutionPolicy
Restricted
PS C:\WINDOWS\system32> set-ExecutionPolicy RemoteSigned

执行策略更改
执行策略可帮助你防止执行不信任的脚本。更改执行策略可能会产生安全风险，如 https:/go.microsoft.com/fwlink/?LinkID=135170
中的 about_Execution_Policies 帮助主题所述。是否要更改执行策略?
[Y] 是(Y)  [A] 全是(A)  [N] 否(N)  [L] 全否(L)  [S] 暂停(S)  [?] 帮助 (默认值为“N”): y
PS C:\WINDOWS\system32> get-ExecutionPolicy
RemoteSigned
PS C:\WINDOWS\system32>
```
