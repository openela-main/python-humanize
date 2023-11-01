%if 0%{?fedora} > 12 || 0%{?rhel} > 7
%global with_python3 1
%endif

%if 0%{?el6} 
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_version: %global python2_version 2.6}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

# Tests are available in head version but not in release 0.5
# enable them at next release.
%global with_checks 0

Name:           python-humanize
Version:        0.5.1
Release:        13%{?dist}
Summary:        Turns dates in to human readable format, e.g '3 minutes ago'

License:        MIT
URL:            https://github.com/jmoiron/humanize
Source0:        https://pypi.python.org/packages/source/h/humanize/humanize-%{version}.tar.gz

BuildArch:      noarch
%if %{with python2}
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
%endif # with python2
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-tools
%endif


%global _description\
This modest package contains various common humanization utilities, like turning\
a number into a fuzzy human readable duration ('3 minutes ago') or into a human\
readable size or throughput.\


%description %_description

%if %{with python2}
%package -n python2-humanize
Summary: %summary
%{?python_provide:%python_provide python2-humanize}

%description -n python2-humanize %_description
%endif # with python2

%if 0%{?with_python3}
%package -n python3-humanize
Summary:        Turns dates in to human readable format, e.g '3 minutes ago'
%{?python_provide:%python_provide python3-humanize}

%description -n python3-humanize
This modest package contains various common humanization utilities, like turning
a number into a fuzzy human readable duration ('3 minutes ago') or into a human
readable size or throughput.
%endif

%prep
%setup -q -n humanize-%{version}

# Remove shebangs from libs.
for lib in humanize/time.py humanize/filesize.py humanize/number.py; do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new && mv $lib.new $lib
done

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%if 0%{?with_python3}
pushd %{py3dir}
# LANG required so README.rst can be parsed.
LANG=en_US.UTF-8 %py3_build
popd
%endif

%if %{with python2}
%py2_build
%endif # with python2

%install
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %py3_install
%find_lang humanize
popd
%endif

%if %{with python2}
%py2_install
%endif # with python2
%if ! 0%{?el6}
%find_lang humanize
%else
touch humanize.lang
%endif

# Remove python3 lang files
%if 0%{?with_python3}
sed -i 's|^.*%{python3_sitelib}.*||' humanize.lang
%endif

%check
%if 0%{?with_checks}
%if %{with python2}
%{__python2} setup.py test
%endif # with python2
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py test
popd
%endif
%endif

%if %{with python2}
%files -n python2-humanize -f humanize.lang
%license LICENCE
%doc README.rst
%dir %{python2_sitelib}/humanize
%{python2_sitelib}/humanize/*.py*
%{python2_sitelib}/humanize-%{version}-py%{python2_version}.egg-info
%if ! 0%{?el6}
%exclude %{_usr}/lib/python*/site-packages/humanize/locale/*/LC_MESSAGES/*.po
%else
%{python2_sitelib}/humanize/locale
%endif
%endif # with python2

%if 0%{?with_python3}
%files -n python3-humanize -f %{py3dir}/humanize.lang
%license LICENCE
%doc README.rst
%dir %{python3_sitelib}/humanize
%{python3_sitelib}/humanize/*.py
%{python3_sitelib}/humanize/__pycache__
%{python3_sitelib}/humanize-%{version}-py%{python3_version}.egg-info
%exclude %{_usr}/lib/python*/site-packages/humanize/locale/*/LC_MESSAGES/*.po
%endif

%changelog
* Fri Jun 08 2018 Charalampos Stratakis <cstratak@redhat.com> - 0.5.1-13
- Conditionalize the python2 subpackage

* Fri Jun 08 2018 Charalampos Stratakis <cstratak@redhat.com> - 0.5.1-12
- Conditionalize the python2 subpackage

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 07 2017 Merlin Mathesius <mmathesi@redhat.com> - 0.5.1-10
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.1-9
- Python 2 binary package renamed to python2-humanize
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.5.1-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 0.5.1-3
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 1 2015 Steve Traylen <steve.traylen@cern.ch> 0.5.1-1
- New 0.5.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed May 14 2014 Steve Traylen <steve.traylen@cern.ch> 0.5-4
- lang fixes for .el6 target.

* Wed Apr 23 2014 Steve Traylen <steve.traylen@cern.ch> 0.5-3
- Use __python2 rather than __python throughout. - rhbz#1088882

* Tue Apr 22 2014 Steve Traylen <steve.traylen@cern.ch> 0.5-2
- Add python3 package - rhbz#1088882.

* Thu Apr 17 2014 Steve Traylen <steve.traylen@cern.ch> 0.5-1
- First release

