

#### 使用 env

##### 创建 激活 运行 安装

sudo apt install python3.10

python3 -m pip install virtualenv

virtualenv -p /usr/bin/python3.10 .venv

source .venv/bin/activate

        pip install numpy

        安装project
        pip install -e .

        运行测试
        python test_c.py



#### 20240123 错误

src/dknovautils/dkipy.py:24: error: Skipping analyzing "IPython.core.getipython": module is installed, but missing library stubs or py.typed marker  [import-untyped]

        from IPython.core.getipython import get_ipython # type: ignore[import-untyped]


#### 20240124 upload error

WARNING  Error during upload. Retry with the --verbose option for more details.
ERROR    HTTPError: 403 Forbidden from https://upload.pypi.org/legacy/
         Username/Password authentication is no longer supported. Migrate to API Tokens or Trusted Publishers
         instead. See https://pypi.org/help/#apitoken and https://pypi.org/help/#trusted-publishers

You can create a token for an entire PyPI account, in which case, the token will work for all projects associated with that account. Alternatively, you can limit a token's scope to a specific project. 

To use an API token:
    Set your username to __token__
    Set your password to the token value, including the pypi- prefix

账户操作
        激活 Two factor authentication (2FA)
        Two-factor authentication (2FA) makes your account more secure by requiring two things in order to log in: something you know and something you own. 
        Two-factor authentication is required on your PyPI account. 

        https://freeotp.github.io/
        https://github.com/freeotp/freeotp-android
        https://f-droid.org/packages/org.fedorahosted.freeotp/
                下载apk文件
                org.fedorahosted.freeotp_44.apk

                设备是 红米手机


                FreeOTP is a two-factor authentication application for systems utilizing one-time password protocols. Tokens can be added easily by scanning a QR code. If you need to generate a QR code, try our QR code generator.        

                Token backups
                        recover from data loss
                        transfer tokens to a new device
                        backups are encrypted using a strong password provided by the user
                                i use pwd:zh
                pypi recovery codes
                        PyPI recovery codes
                        e954a3f23b21e27c
                        25bd14b40edbc1e6
                        daa2ef2e167d42de
                        d3be4f0c7d4d1ca8
                        757328cd704c5c88
                        9123e5c667e89ff1
                        a54fe5161c23151d   

                Add Pypi Token
                        token name: upload

pypi-AgEIcHlwaS5vcmcCJDRmNzYzNWVlLWVhYzctNGMzMS04MTRiLWVlNDdmMTg4YTYzMAACKlszLCI3ZWFmOTQxZC1kODEwLTRiNWEtODUxNC1lZDc0OTNmMjg3NjkiXQAABiCbA0t1hG72XDZctuLR26BJO3Qg5-phTFZhIwAwkIENnQ

pypi-AgEIcHlwaS5vcmcCJGY2ZGQzYTA3LTg0YjItNGRmYS1iYzlmLTg2MjZkMmRjYTgzZgACKlszLCI3ZWFmOTQxZC1kODEwLTRiNWEtODUxNC1lZDc0OTNmMjg3NjkiXQAABiAp4Ypqsifho-FNPbs9hj5FaVuu95clV0dZ4u6U_Rj5Rw













