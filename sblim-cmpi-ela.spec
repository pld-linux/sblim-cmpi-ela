# TODO: PLDify init script, register service; register .mof
Summary:	SBLIM CMPI provider for Linux Event Log analysis
Summary(pl.UTF-8):	Dostawca danych SBLIM CMPI do analizy linuksowego logu zdarzeń
Name:		sblim-cmpi-ela
Version:	0.7.5
Release:	0.1
License:	CPL
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.gz
# Source0-md5:	9564ca88da1e40b535ae429efe968de4
URL:		http://sblim.sourceforge.net/
BuildRequires:	sblim-cmpi-base-devel
BuildRequires:	sblim-cmpi-devel
Requires:	sblim-cmpi-base
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SBLIM CMPI provider for Linux Event Log analysis.

%description -l pl.UTF-8
Dostawca danych SBLIM CMPI do analizy linuksowego logu zdarzeń.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC -D_COMPILE_UNIX -Wall -I. -Iparser -I\$(CIMOMINC) -DCMPI_VERSION=90" \
	CIMOMINC=%{_includedir}/cmpi \
	LDFLAGS="%{rpmldflags} -fPIC -shared -Lparser -lpthread -ldl" \
	LIBDIR=%{_libdir} \
	PEGASUS= \
	STANDALONE=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/cmpi,%{_datadir}/%{name},/etc/rc.d/init.d}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	CIMOMMOF=$RPM_BUILD_ROOT%{_datadir}/%{name} \
	DAEMONSCRIPTDIR=/etc/rc.d/init.d \
	LIBDIR=%{_libdir} \
	PEGASUS= \
	STANDALONE=1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/sig_ela_daemon.sh
%attr(755,root,root) %{_sbindir}/ela_daemon
%attr(755,root,root) %{_libdir}/libparseelareport.so
%attr(755,root,root) %{_libdir}/cmpi/libelaindicationprovider.so
%attr(754,root,root) /etc/rc.d/init.d/elad
%dir %{_datadir}/sblim-cmpi-ela
%{_datadir}/sblim-cmpi-ela/Ela_Indication.mof
%{_datadir}/sblim-cmpi-ela/Ela_IndicationR.mof
