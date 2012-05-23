%define	major 1
%define libname %mklibname tirpc %{major}
%define develname %mklibname tirpc -d

Summary:	Transport Independent RPC Library
Name:		libtirpc
Version:	0.2.2
Release:	2
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
Requires:	%{name} >= %{version}-%{release}

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

%package -n	%{develname}
Summary:	Development files for the libtirpc library
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	tirpc-devel = %{version}-%{release}
Obsoletes:	%{mklibname tirpc 1 -d}

%description -n	%{develname}
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


%prep
%setup -q
%patch0 -p1
autoreconf -fi

%build
export CFLAGS="%{optflags} -fPIC"
%configure2_5x \
    --enable-gss
%make all

%install
rm -rf %{buildroot}


%makeinstall_std
install -m 755 -d %{buildroot}%{_sysconfdir}
install -m 644 doc/etc_netconfig %{buildroot}%{_sysconfdir}/netconfig

# remove the .la file, it makes libtool reorder args when linking nfs-utils:
# http://lists.gnu.org/archive/html/libtool/2010-03/msg00023.html 
# cleanups
rm -f %{buildroot}%{_libdir}/*.*a

%files
%config(noreplace) %{_sysconfdir}/netconfig

%files -n %{libname}
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/libtirpc.pc
%{_includedir}/tirpc
%{_mandir}/man3/*
%{_mandir}/man5/*
