%define _disable_ld_no_undefined 1

%define major 1
%define libname %mklibname tirpc %{major}
%define devname %mklibname tirpc -d
%define static %mklibname -d -s tirpc
%define beta %nil

%bcond_without uclibc

Summary:	Transport Independent RPC Library
Name:		libtirpc
Version:	0.2.3
License:	SISSL and BSD
Group:		System/Libraries
Url:		http://sourceforge.net/projects/libtirpc
%if "%{beta}" == ""
Release:	4
Source0:	http://downloads.sourceforge.net/libtirpc/%{name}-%{version}.tar.bz2
%else
Release:	0.%{beta}.1
# Packaged from git://git.infradead.org/~steved/libtirpc.git w/ git archive
Source0:	%{name}-%{version}-%{beta}.tar.xz
%endif
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
Patch9:		segfault_fix.patch
BuildRequires:	libtool
BuildRequires:	pkgconfig(libgssglue)
BuildRequires:	krb5-devel
%if %{with uclibc}
BuildRequires: uClibc-devel >= 0.9.33.2-15
%endif

%track
prog %{name} = {
	url = http://sourceforge.net/projects/libtirpc/files/libtirpc/
	version = %{version}
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
This package contains the shared library for %{name}.


%if %{with uclibc}
%package -n uclibc-%{libname}
Summary:	Transport Independent RPC Library (uClibc build)
Group:		System/Libraries

%description -n uclibc-%{libname}
This package contains the uClibc shared library for %{name}.
%endif

%package -n	%{devname}
Summary:	Development files for the libtirpc library
Group:		Development/C
Requires:	%{libname} >= %{EVRD}
Provides:	tirpc-devel = %{EVRD}
Conflicts:	glibc < 6:2.17-1.22064.3

%description -n	%{devname}
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
autoreconf -fi

install -m644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} tirpc/rpcsvc/
install -m644 %{SOURCE15} %{SOURCE16} tirpc/rpc/

%build
export CFLAGS="%{optflags} -fPIC"

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
CONFIGURE_TOP="$PWD"

%uclibc_configure \
--enable-shared \
--enable-static \
--enable-gss

%make all
popd
%endif

mkdir -p system
pushd system
CONFIGURE_TOP="$PWD"

%configure2_5x	\
	--enable-shared \
	--enable-static \
	--enable-gss

%make all
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
%endif

%makeinstall_std -C system
install -m 755 -d %{buildroot}%{_sysconfdir}
install -m 644 doc/etc_netconfig %{buildroot}%{_sysconfdir}/netconfig
install -m644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{buildroot}%{_includedir}/tirpc/rpcsvc/
install -m644 %{SOURCE15} %{SOURCE16} %{buildroot}%{_includedir}/tirpc/rpc/

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

%files
%config(noreplace) %{_sysconfdir}/netconfig

%files -n %{libname}

%{_libdir}/libtirpc.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/libtirpc.so.%{major}*
%endif

%files -n %{devname}
%doc AUTHORS ChangeLog COPYING NEWS README
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
