%define major 3
%define libname %mklibname tirpc %{major}
%define devname %mklibname tirpc -d
%define static %mklibname -d -s tirpc

%bcond_without gss

Summary:	Transport Independent RPC Library
Name:		libtirpc
Version:	1.3.2
Release:	1
License:	SISSL and BSD
Group:		System/Libraries
Url:		http://sourceforge.net/projects/libtirpc
Source0:	http://downloads.sourceforge.net/libtirpc/%{name}-%{version}.tar.bz2
Patch2:		libtirpc-0.2.3-types.h.patch
Patch5:		libtirpc-0008-Add-rpcgen-program-from-nfs-utils-sources.patch
Patch6:		libtirpc-0.2.3-update-rpcgen-from-glibc.patch
Patch7:		rpcgen-compile.patch
Patch8:		libtirpc-0.3.0-sizeof.patch
# disabled as it breaks nfs etc.
#Patch8:	tirpc-xdr-update-from-glibc.patch
Patch12:	libtirpc-0010-Add-more-XDR-files-needed-to-build-rpcbind-on-top-of.patch

BuildRequires:	libtool
%if %{with gss}
BuildRequires:	krb5-devel
%else
BuildConflicts:	krb5-devel
%endif
BuildRequires:	pkgconfig(com_err)
BuildRequires:	autoconf
BuildRequires:	automake

%description
This package contains SunLib's implementation of transport-independent
RPC (TI-RPC) documentation.  This library forms a piece of the base of 
Open Network Computing (ONC), and is derived directly from the 
Solaris 2.3 source.

TI-RPC is an enhanced version of TS-RPC that requires the UNIX System V 
Transport Layer Interface (TLI) or an equivalent X/Open Transport Interface 
(XTI).  TI-RPC is on-the-wire compatible with the TS-RPC, which is supported 
by almost 70 vendors on all major operating systems.  TS-RPC source code 
(RPCSRC 4.0) remains available from several internet sites.

%package -n %{libname}
Summary:	Transport Independent RPC Library
Group:		System/Libraries
Requires:	%{name} >= %{EVRD}

%description -n %{libname}
This package contains the shared library for %{name}.

%package -n %{devname}
Summary:	Development files for the libtirpc library
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
Provides:	tirpc-devel = %{EVRD}
Conflicts:	glibc < 2.17-1.22064.3

%description -n %{devname}
This package includes header files and libraries necessary for developing
programs which use the tirpc library.

%package -n %{static}
Summary:	Static version of libtirpc library
Group:		Development/C
Requires:	%{devname} >= %{EVRD}
Provides:	tirpc-static-devel = %{EVRD}

%description -n %{static}
This package contains a static library version of the libtirpc library.

%prep
%autosetup -p1

autoreconf -fiv

%build
CONFIGURE_TOP="$PWD"
export CFLAGS="%{optflags} -fPIC"

%configure	\
	--libdir=/%{_lib} \
	--enable-shared \
	--enable-static \
%if %{with gss}
	--enable-gssapi
%else
	--disable-gssapi
%endif

%make_build all

%install
%make_install
install -m 755 -d %{buildroot}%{_sysconfdir}
install -m 644 doc/netconfig %{buildroot}%{_sysconfdir}/netconfig

install -d %{buildroot}%{_includedir}/{rpc,rpcsvc}/
cd %{buildroot}%{_includedir}/tirpc/rpc
for i in *.h; do
    ln -sf ../tirpc/rpc/$i %{buildroot}%{_includedir}/rpc/$i
done
cd ../rpcsvc
for i in *.h; do
    ln -sf ../tirpc/rpcsvc/$i %{buildroot}%{_includedir}/rpcsvc/$i
done
cd %{buildroot}%{_includedir}
ln -s tirpc/netconfig.h .

install -d %{buildroot}%{_libdir}
mv %{buildroot}/%{_lib}/libtirpc.a %{buildroot}%{_libdir}
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}
rm %{buildroot}/%{_lib}/libtirpc.so
ln -srf %{buildroot}/%{_lib}/libtirpc.so.%{major}.* %{buildroot}%{_libdir}/libtirpc.so

%files
%config(noreplace) %{_sysconfdir}/netconfig
%config(noreplace) %{_sysconfdir}/bindresvport.blacklist

%files -n %{libname}
/%{_lib}/libtirpc.so.%{major}*

%files -n %{devname}
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/rpcgen
%{_libdir}/libtirpc.so
%{_libdir}/pkgconfig/libtirpc.pc
%{_includedir}/tirpc
%{_includedir}/netconfig.h
%{_includedir}/rpc/*
%{_includedir}/rpcsvc/*
%{_mandir}/man[135]/*

%files -n %{static}
%{_libdir}/libtirpc.a
