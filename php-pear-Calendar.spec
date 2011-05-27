%define		_class		Calendar
%define		upstream_name	%{_class}

Name:		php-pear-%{upstream_name}
Version:	0.5.4
Release:	%mkrel 5
Summary:	Building calendar data structures (irrespective of output)
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/Calendar/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tgz
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	php-pear
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Calendar provides an API for building calendar data structures. Using
the simple iterator and it's "query" API, a user interface can easily be
built on top of the calendar data structure, at the same time easily
connecting it to some kind of underlying data store, where "event"
information is being held.

It provides different calculation "engines" the default being based on
Unix timestamps (offering fastest performance) with an alternative using
PEAR::Date which extends the calendar past the limitations of Unix
timestamps. Other engines should be implementable for other types of
calendar (e.g. a Chinese Calendar based on lunar cycles).

%prep
%setup -q -c
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%doc %{upstream_name}-%{version}/docs/*
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml
