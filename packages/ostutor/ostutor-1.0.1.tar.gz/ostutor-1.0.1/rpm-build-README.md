**RPM BUILD README**

```shell
# 由于Openeuler的rpm源不完善，也没有较完善的第三方源，导致许多python依赖无法安装
# 并且不同Openeuler中python版本互不相同，并且python与许多系统级别的程序绑定，不可随意更换版本，即无法通过指定pip包路径来安装依赖
# 遂此rpm打包仅提供打包示范
# 实际使用可以直接使用whl包：pip install ostutor
```

# ostutor 0.1

## 版本概述：
此版本目的仅为简单运行成功

## 构建说明
### 预下载

```shell
sudo dnf install rpm-build rpmdevtools python3-devel
```

### 构建命令
```shell
# 测试平台：openEuler-Standard-22.03-LTS-SP3
cd ../.. # 上上个文件夹,即项目根目录
rpmdev-setuptree #创建RPM构建目录结构（会创建在$HOME）
tar czvf tool.tar.gz tool/
mv tool.tar.gz ~/rpmbuild/SOURCES/
rpmbuild -ba ./tool/ostutor.spec
sudo rpm -ivh ~/rpmbuild/RPMS/noarch/ostutor-x.noarch.rpm
# sudo dnf install ~/rpmbuild/RPMS/noarch/ostutor-0.3.1-1.noarch.rpm
```

### 运行
```shell
[sztu@openeuler tool]$ rpm -qi ostutor
Name        : ostutor
Version     : 0.3.1
Release     : 1
Architecture: noarch
Install Date: 2024年07月24日 星期三 19时29分05秒
Group       : Unspecified
Size        : 139387507
License     : Mulan PSL v1
Signature   : (none)
Source RPM  : ostutor-0.3.1-1.src.rpm
Build Date  : 2024年07月24日 星期三 19时25分29秒
Build Host  : openeuler
URL         : https://gitlab.eduxiji.net/T202414655993206/project2210132-239674
Summary     : A tool that returns relevant commands and help information based on user-provided keywords.
Description :
The goal of the App is to develop a new tool that, after receiving a few keywords given by the user, returns possibly relevant commands and other further relevant help information.

[sztu@openeuler tool]$ dnf info ostutor
OS                                                            30 kB/s | 3.8 kB     00:00    
everything                                                   3.0 kB/s | 3.8 kB     00:01    
EPOL                                                          24 kB/s | 3.0 kB     00:00    
debuginfo                                                     35 kB/s | 3.8 kB     00:00    
source                                                        35 kB/s | 3.8 kB     00:00    
update                                                        36 kB/s | 3.5 kB     00:00    
update-source                                                1.0 MB/s | 761 kB     00:00    
Installed Packages
Name         : ostutor
Version      : 0.3.1
Release      : 1
Architecture : noarch
Size         : 133 M
Source       : ostutor-0.3.1-1.src.rpm
Repository   : @System
From repo    : @commandline
Summary      : A tool that returns relevant commands and help information based on
             : user-provided keywords.
URL          : https://gitlab.eduxiji.net/T202414655993206/project2210132-239674
License      : Mulan PSL v1
Description  : The goal of the App is to develop a new tool that, after receiving a few
             : keywords given by the user, returns possibly relevant commands and other
             : further relevant help information.

[sztu@openeuler tool]$ ostutor
Usage: ostutor [OPTIONS] COMMAND [ARGS]...

  OSTutor - OpenEuler Application Assistant.

Options:
  --help  Show this message and exit.

Commands:
  cli       Command line retrieval.
  dataexp
  dataimp   Import the specified json file to the database.
  install   Do not differentially download the rpm package from the...
  lrefresh  Refresh the knowledge base locally.
  nodata    Search for local instructions without data.
  rpmsexp   Export the local RPM list to the current directory.
  terminal  Open the terminal interface.
  ui        Start user interface mode.
```

# ostutor 更新模板
## 版本概述：
## 代码改动：
## 文件说明
## 改进方向

# 上传