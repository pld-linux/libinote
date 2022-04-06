Summary:	Library to preprocess a text aimed to text-to-speech engine
Summary(pl.UTF-8):	Biblioteka do przetwarzania tekstu przeznaczonego do syntezy mowy
Name:		libinote
Version:	1.1.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/Oralux/libinote/tags
Source0:	https://github.com/Oralux/libinote/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7a707f8b9946260697d8adb7f350fddf
URL:		https://github.com/Oralux/libinote
BuildRequires:	gcc >= 6:4.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libinote library preprocesses a text aimed to a text-to-speech
engine:
- input: raw text or enriched with SSML tags or ECI annotations,
- output: type-length-value format.

%description -l pl.UTF-8
Biblioteka libinote przetwarza tekst przeznaczony dla silników syntezy
mowy:
- wejście: czysty tekst lub wzbogacony znacznikami SSML lub ECI
- wyjście: format type-length-value (typ-długość-wartość)

%package devel
Summary:	Header files for libinote library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libinote
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libinote library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libinote.

%package static
Summary:	Static libinote library
Summary(pl.UTF-8):	Statyczna biblioteka libinote
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libinote library.

%description static -l pl.UTF-8
Statyczna biblioteka libinote.

%prep
%setup -q

%build
install -d lib
DDIR=$(pwd)
cd src/libinote
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__make} \
	CC="%{__cc}"

%{__cc} -shared -o libinote.so.0.0.0 -Wl,-soname,libinote.so.0 %{rpmldflags} %{rpmcflags} lib.o debug.o
ln -sf libinote.so.0.0.0 libinote.so.0
ln -sf libinote.so.0.0.0 libinote.so
ln -sf ../src/libinote/libinote.so ${DDIR}/lib/libinote.so

cd ../test
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__make} text2tlv tlv2text \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	DESTDIR=$DDIR

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

install src/test/{text2tlv,tlv2text} $RPM_BUILD_ROOT%{_bindir}
cp -a src/libinote/libinote.* $RPM_BUILD_ROOT%{_libdir}
cp -p src/api/inote.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE-LGPL-2.1+ LICENSE-MIT README.org
%attr(755,root,root) %{_bindir}/text2tlv
%attr(755,root,root) %{_bindir}/tlv2text
%attr(755,root,root) %{_libdir}/libinote.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libinote.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libinote.so
%{_includedir}/inote.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libinote.a
