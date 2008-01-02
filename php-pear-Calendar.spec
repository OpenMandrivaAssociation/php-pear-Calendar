%define		_class		Calendar
%define		_status		beta
%define		_pearname	%{_class}

Summary:	%{_pearname} - building calendar data structures (irrespective of output)
Name:		php-pear-%{_pearname}
Version:	0.5.3
Release:	%mkrel 1
License:	PHP License
Group:		Development/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tar.bz2
URL:		http://pear.php.net/package/Calendar/
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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

In PEAR status of this package is: %{_status}.

%prep

%setup -q -c

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/pear/%{_class}/{Decorator,Engine,Month,Table}

install %{_pearname}-%{version}/*.php %{buildroot}%{_datadir}/pear/%{_class}
install %{_pearname}-%{version}/Decorator/*.php %{buildroot}%{_datadir}/pear/%{_class}/Decorator
install %{_pearname}-%{version}/Engine/*.php %{buildroot}%{_datadir}/pear/%{_class}/Engine
install %{_pearname}-%{version}/Month/*.php %{buildroot}%{_datadir}/pear/%{_class}/Month
install %{_pearname}-%{version}/Table/*.php %{buildroot}%{_datadir}/pear/%{_class}/Table

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_pearname}-%{version}/docs/*
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{_pearname}.xml


