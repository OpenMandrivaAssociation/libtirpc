%define	major	1
%define	libname	%mklibname tirpc %{major}
%define	devname	%mklibname tirpc -d
%define	static	%mklibname -d -s tirpc

Summary:	Transport Independent RPC Library
Name:		libtirpc
Version:	0.2.2
Release:	3
License:	GPL
Group:		System/Libraries
URL:		http://sourceforge.net/projects/libtirpc
Source0:	http://downloads.sourceforge.net/libtirpc/%{name}-%{version}.tar.bz2
Patch0:		01-remove-des-crypt.diff
BuildRequires:	pkgconfig
BuildRequires:	gssglue-devel
BuildRequires:	autoconf automake libtool

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

%package -n	%{libname}
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
%patch0 -p1
autoreconf -fi

%build
export CFLAGS="%{optflags} -fPIC"
%configure2_5x	--enable-shared \
		--enable-static \
		--enable-gss
%make all

%install
%makeinstall_std
install -m 755 -d %{buildroot}%{_sysconfdir}
install -m 644 doc/etc_netconfig %{buildroot}%{_sysconfdir}/netconfig

%files
%config(noreplace) %{_sysconfdir}/netconfig

%files -n %{libname}
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libtirpc.so.%{major}*

%files -n %{devname}
%{_libdir}/libtirpc.so
%{_libdir}/pkgconfig/libtirpc.pc
%{_includedir}/tirpc
%{_mandir}/man3/*
%{_mandir}/man5/*

%files -n %{static}
%{_libdir}/libtirpc.a
