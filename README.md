# emby-metadata

## 安装依赖

```shell
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

> BeautifulSoup: html解析，[文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/) 

> tqdm: 进度条

## 运行flask

### Terminal运行

```shell
python -m flask run --port=5001
```

### 配置Flask服务 Configuration

- Target type: Custom
- Target: app.py
- Application: app
- Additional options: --port=5001
- FLASK_ENV: development
- Environment
    - Python interpreter: Project Default
    - Add content roots to PYTHONPATH
    - Add source roots to PYTHONPATH

## 访问app

[http://127.0.0.1:5001](http://127.0.0.1:5001)

## FAQ

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

- 以一种访问权限不允许的方式做了一个访问套接字的尝试。

```shell
# 端口被占用，查找占用5000端口的应用PID，然后在服务中找到PID对应的程序
> netstat -ano|findstr 5000
  TCP    127.0.0.1:5000         0.0.0.0:0              LISTENING       5544
  TCP    [::1]:5000             [::]:0                 LISTENING       5544
```

> 5000: 被igccservice Intel(R) Graphics Command Center Service占用
> 6000: 禁止使用

- 下载提示 `certificate verify failed: unable to get local issuer certificate`

```shell
pip install pyopenssl
```
