# 由于Openeuler的rpm源不完善，也没有较完善的第三方源，导致许多python依赖无法安装
# 并且不同Openeuler中python版本互不相同，并且python与许多系统级别的程序绑定，不可随意更换版本，即无法通过指定pip包路径来安装依赖
# 遂此rpm打包仅提供打包示范
# 实际使用可以直接使用whl包：pip install ostutor

# The method of packaging documents.
# Please add a document declaration in the install and files lines. Here are some examples:
# tips:To prevent incorrect reading during rpm packaging, the dollar sign was used instead of the percent sign.
# -----start-----
# $install
# mkdir -p ${buildroot}${_docdir}/${name}
# mkdir -p ${buildroot}${_docdir}/command_doc/${name}
# install -m 0644 ostutor.txt ${buildroot}${_docdir}/command_doc/${name}/
# install -m 0644 rpm-build-README.md ${buildroot}${_docdir}/${name}/
# 
# %files
# $doc ${_docdir}/${name}/command.txt
# $doc {_docdir}/command_doc/${name}/rpm-README.md
# -----end-----

Name:           ostutor
Version:        0.1
Release:        1%{?dist}
Summary:        A terminal application for searching rpm commands

License:        Mulan PSL v1
URL:            https://gitlab.eduxiji.net/T202414655993206/project2210132-239674
Source0:        tool.tar.gz

BuildArch:      noarch
BuildRequires:  python3
Requires:       python3

%description
The goal of the App is to develop a new tool that, after receiving a few keywords given by the user, returns possibly relevant commands and other further relevant help information.

%prep
%setup -q -n tool

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_docdir}/%{name}
mkdir -p %{buildroot}%{_docdir}/command_doc/%{name}
install -m 0644 ostutor.txt %{buildroot}%{_docdir}/command_doc/%{name}/
install -m 0644 rpm-build-README.md %{buildroot}%{_docdir}/%{name}/

# 创建入口脚本
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/usr/bin/env python3
import sys
import os

sys.path.append('/usr/local/python3/lib/python3.9/site-packages')

# 添加包含 OSTutor 的目录到 Python 路径
sys.path.insert(0, '/usr/share/ostutor')

if __name__ == "__main__":
    print("Running successfully!")

#from OSTutor.src import cmd
#
#if __name__ == "__main__":
#    cmd()
EOF

# 复制代码去标准安装目录
chmod +x %{buildroot}%{_bindir}/ostutor
# cp -r OSTutor %{buildroot}%{_datadir}/ostutor

# 使用pip安装依赖项
# pip install --root %{buildroot} -r OSTutor/requirements.txt

%files
%{_bindir}/ostutor
%{_datadir}/ostutor
%doc %{_docdir}/command_doc/%{name}/ostutor.txt
%doc %{_docdir}/%{name}/rpm-build-README.md

%changelog
* Mon Jul 22 2024 Name <email@example.com> - 0.1-1
- Initial package