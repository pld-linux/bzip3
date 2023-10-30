#
# Conditional build:
%bcond_without	static_libs	# static libraries

Summary:	A better and stronger spiritual successor to BZip2
Summary(pl.UTF-8):	Lepszy i silniejszy duchowy następca BZip2
Name:		bzip3
Version:	1.3.2
Release:	0.1
License:	LGPL-3+
Group:		Applications/Archiving
Source0:	https://github.com/kspalaiologos/bzip3/releases/download/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	3ddde8f8553fbc73c2eef6b8587052ae
URL:		https://github.com/kspalaiologos/bzip3
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.6
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.213
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A better, faster and stronger spiritual successor to BZip2. Features
higher compression ratios and better performance thanks to a order-0
context mixing entropy coder, a fast Burrows-Wheeler transform code
making use of suffix arrays and a RLE with Lempel Ziv+Prediction pass
based on LZ77-style string matching and PPM-style context modeling.

%description -l pl.UTF-8
Lepszy, szybszy i silniejszy duchowy następca BZip2. Charakteryzuje
się wyższymi współczynnikami kompresji i lepszą wydajnością dzięki
koderowi entropii mieszania kontekstu rzędu 0, szybkiemu kodowi
transformacji Burrowsa-Wheelera wykorzystującemu tablice sufiksów oraz
RLE z przejściem Lempel Ziv + Prediction opartym na dopasowywaniu
ciągów w stylu LZ77 i modelowaniu kontekstu w stylu PPM.

%package libs
Summary:	libbzip3 library
Summary(pl.UTF-8):	Biblioteka libbzip3
Group:		Libraries

%description libs
Libbzip3 library.

%description libs -l pl.UTF-8
Biblioteka libbzip3.

%package devel
Summary:	libbzip3 library header files
Summary(pl.UTF-8):	Pliki nagłówkowe do libbzip3
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Libbzip3 library header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe do libbzip3.

%package static
Summary:	Static libbzip3 library
Summary(pl.UTF-8):	Biblioteka statyczna libbzip3
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbzip3 library.

%description static -l pl.UTF-8
Biblioteka statyczna libbzip3.

%prep
%setup -q
%{__sed} -i '1s,%{_bindir}/env sh$,%{__sh},' \
	./{bz3most,bz3more,bz3cat,bz3less,bz3grep}

%build
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc libsais-LICENSE NEWS PORTING.md README.md
%attr(755,root,root) %{_bindir}/bunzip3
%attr(755,root,root) %{_bindir}/bz3cat
%attr(755,root,root) %{_bindir}/bz3grep
%attr(755,root,root) %{_bindir}/bzip3
%attr(755,root,root) %{_bindir}/bz3less
%attr(755,root,root) %{_bindir}/bz3more
%attr(755,root,root) %{_bindir}/bz3most
%{_mandir}/man1/bunzip3.1*
%{_mandir}/man1/bz3cat.1*
%{_mandir}/man1/bz3grep.1*
%{_mandir}/man1/bz3less.1*
%{_mandir}/man1/bz3more.1*
%{_mandir}/man1/bz3most.1*
%{_mandir}/man1/bzip3.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_libdir}/libbzip3.so.*.*.*
%attr(755,root,root) %ghost /%{_libdir}/libbzip3.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbzip3.so
%{_libdir}/libbzip3.la
%{_includedir}/libbz3.h
%{_pkgconfigdir}/bzip3.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbzip3.a
%endif
