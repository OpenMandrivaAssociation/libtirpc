%define major	1
%define libname	%mklibname tirpc %{major}
%define devname	%mklibname tirpc -d
%define static	%mklibname -d -s tirpc

Summary:	Transport Independent RPC Library
Name:		libtirpc
Version:	0.2.3
Release:	3
Source0:	http://downloads.sourceforge.net/libtirpc/%{name}-%{version}.tar.bz2
# Related headers that were removed from glibc
Source10:	nis.h
Source11:	nis_tags.h
Source12:	nislib.h
Source13:	yp_prot.h
Source14:	ypclnt.h
Source15:	key_prot.h
Source16:	rpc_des.h
Patch0:		libtirpc-0.2.3-add-missing-bits-from-glibc.patch
Patch1:		libtirpc-0.2.2-automake-1.13.patch
Patch2:		libtirpc-0.2.3-types.h.patch
Patch5:		libtirpc-0008-Add-rpcgen-program-from-nfs-utils-sources.patch
Patch6:		libtirpc-0.2.3-update-rpcgen-from-glibc.patch
Patch7:		rpcgen-compile.patch
Patch8:		tirpc-xdr-update-from-glibc.patch
Patch9:		libtirpc-0.2.4-rc1.patch
License:	SISSL and BSD
Group:		System/Libraries
URL:		http://sourceforge.net/projects/libtirpc
BuildRequires:	pkgconfig
BuildRequires:	gssglue-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool

%track
prog %name = {
	url = http://sourceforge.net/projects/libtirpc/files/libtirpc/
	version = %version
	regex = "Download libtirpc-(__VER__)\.tar\.bz2"
}

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

%description -n	%{libname}
This package contains SunLib's implementation of transport-independent
RPC (TI-RPC) documentation.  This library forms a piece of the base of 
Open Network Computing (ONC), and is derived directly from the 
Solaris 2.3 source.

TI-RPC is an enhanced version of TS-RPC that requires the UNIX System V 
Transport Layer Interface (TLI) or an equivalent X/Open Transport Interface 
(XTI).  TI-RPC is on-the-wire compatible with the TS-RPC, which is supported 
by almost 70 vendors on all major operating systems.  TS-RPC source code 
(RPCSRC 4.0) remains available from several internet sites.

%package -n	%{devname}
Summary:	Development files for the libtirpc library
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
Provides:	tirpc-devel = %{EVRD}
Obsoletes:	%{mklibname tirpc 1 -d}
Conflicts:	glibc < 6:2.17-1.22064.3

%description -n	%{devname}
This package contains SunLib's implementation of transport-independent
RPC (TI-RPC) documentation.  This library forms a piece of the base of 
Open Network Computing (ONC), and is derived directly from the 
Solaris 2.3 source.

TI-RPC is an enhanced version of TS-RPC that requires the UNIX System V 
Transport Layer Interface (TLI) or an equivalent X/Open Transport Interface 
(XTI).  TI-RPC is on-the-wire compatible with the TS-RPC, which is supported 
by almost 70 vendors on all major operating systems.  TS-RPC source code 
(RPCSRC 4.0) remains available from several internet sites.

This package includes header files and libraries necessary for developing
programs which use the tirpc library.

%package -n	%{static}
Summary:	Static version of libtirpc library
Group:		Development/C
Requires:	%{devname} >= %{EVRD}
Provides:	tirpc-static-devel = %{EVRD}

%description -n	%{static}
This package contains a static library version of the libtirpc library.

%prep
%setup -q
%apply_patches

libtoolize --force
aclocal
autoheader
automake -a
autoconf

mkdir -p glibc-headers/rpc glibc-headers/rpcsvc
install -c -m 644 %SOURCE10 %SOURCE11 %SOURCE12 %SOURCE13 %SOURCE14 glibc-headers/rpcsvc/
install -c -m 644 %SOURCE15 %SOURCE16 glibc-headers/rpc/

%build
export CFLAGS="%{optflags} -fPIC -I`pwd`/glibc-headers -I`pwd`/tirpc"
%configure2_5x	\
	--enable-shared \
	--enable-static \
	--enable-gss

%make all

%install
%makeinstall_std
install -m 755 -d %{buildroot}%{_sysconfdir}
install -m 644 doc/etc_netconfig %{buildroot}%{_sysconfdir}/netconfig
cp -a glibc-headers/* %{buildroot}%{_includedir}
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

%files
%config(noreplace) %{_sysconfdir}/netconfig

%files -n %{libname}
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libtirpc.so.%{major}*

%files -n %{devname}
%{_bindir}/rpcgen
%_libdir/libtirpc.so
%_libdir/pkgconfig/libtirpc.pc
%{_includedir}/tirpc
%{_includedir}/netconfig.h
%{_includedir}/rpc/*
%{_includedir}/rpcsvc/*
%{_mandir}/man[135]/*

%files -n %{static}
%{_libdir}/libtirpc.a
