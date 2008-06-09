%define	major 1
%define libname %mklibname tirpc %{major}
%define develname %mklibname tirpc -d

Summary:	Transport Independent RPC Library
Name:		libtirpc
Version:	0.1.7
Release:	%mkrel 6
License:	GPL
Group:		System/Libraries
URL:		http://nfsv4.bullopensource.org/
Source0:	http://nfsv4.bullopensource.org/tarballs/tirpc/%{name}-%{version}.tar.bz2
Patch1:		libtirpc-0.1.7-netconfig.patch
Patch2:		libtirpc-0.1.7-gssapi.patch
Patch3:		libtirpc-0.1.7-svcauthnone.patch
Patch4:		libtirpc-0.1.7-ppc64.patch
Patch5:		libtirpc-0.1.7-svcauthdestroy.patch
Patch6:		libtirpc-0.1.7-xdr_bufferoverlow.patch
Patch7:		libtirpc-0.1.7-bindresvport_ports.patch
Patch8:		libtirpc-0.1.7-svc-run.patch
Patch9:		libtirpc-0.1.7-clnt_raw-mutex.patch
Patch10:	libtirpc-0.1.7-snprintf.patch
Patch11:	libtirpc-0.1.7-bindresvport-ntohs.patch
Patch12:	libtirpc-0.1.7-dgcall-iprecverr.patch
Patch13:	libtirpc-0.1.7-svc-rtaddr.patch
Patch100:	libtirpc-0.1.7-compile.patch
Patch101:	libtirpc-gssglue.diff
BuildRequires:	autoconf2.5
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	gssglue-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

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
Requires:	%{libname} = %{version}-%{release}
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
%patch1	-p1
%patch2	-p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch100 -p1
%patch101 -p0

%build
rm -rf autom4te.cache configure Makefile stamp-h1 
rm -rf src/Makefile src/.deps
rm -rf Makefile.in aclocal.m4 config.log config.h
rm -rf depcomp missing install-sh config.status
libtoolize --copy --force; aclocal; autoheader; automake --gnu --add-missing -c; autoconf

export CFLAGS="%{optflags} -fPIC"

%configure2_5x \
    --enable-gss

%make all

%install
rm -rf %{buildroot}

install -d %{buildroot}/etc

%makeinstall_std

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/netconfig
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(0644,root,root,0755)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%dir %{_includedir}/tirpc
%dir %{_includedir}/tirpc/misc
%dir %{_includedir}/tirpc/rpc
%dir %{_includedir}/tirpc/rpcsvc
%{_includedir}/tirpc/fpmath.h
%{_includedir}/tirpc/getpeereid.h
%{_includedir}/tirpc/libc_private.h
%{_includedir}/tirpc/misc/event.h
%{_includedir}/tirpc/misc/queue.h
%{_includedir}/tirpc/misc/socket.h
%{_includedir}/tirpc/namespace.h
%{_includedir}/tirpc/netconfig.h
%{_includedir}/tirpc/nss_tls.h
%{_includedir}/tirpc/reentrant.h
%{_includedir}/tirpc/rpc/auth.h
%{_includedir}/tirpc/rpc/auth_des.h
%{_includedir}/tirpc/rpc/auth_gss.h
%{_includedir}/tirpc/rpc/auth_kerb.h
%{_includedir}/tirpc/rpc/auth_unix.h
%{_includedir}/tirpc/rpc/clnt.h
%{_includedir}/tirpc/rpc/clnt_soc.h
%{_includedir}/tirpc/rpc/clnt_stat.h
%{_includedir}/tirpc/rpc/des.h
%{_includedir}/tirpc/rpc/des_crypt.h
%{_includedir}/tirpc/rpc/nettype.h
%{_includedir}/tirpc/rpc/pmap_clnt.h
%{_includedir}/tirpc/rpc/pmap_prot.h
%{_includedir}/tirpc/rpc/pmap_rmt.h
%{_includedir}/tirpc/rpc/raw.h
%{_includedir}/tirpc/rpc/rpc.h
%{_includedir}/tirpc/rpc/rpc_com.h
%{_includedir}/tirpc/rpc/rpc_msg.h
%{_includedir}/tirpc/rpc/rpcb_clnt.h
%{_includedir}/tirpc/rpc/rpcb_prot.h
%{_includedir}/tirpc/rpc/rpcb_prot.x
%{_includedir}/tirpc/rpc/rpcent.h
%{_includedir}/tirpc/rpc/svc.h
%{_includedir}/tirpc/rpc/svc_auth.h
%{_includedir}/tirpc/rpc/svc_dg.h
%{_includedir}/tirpc/rpc/svc_soc.h
%{_includedir}/tirpc/rpc/types.h
%{_includedir}/tirpc/rpc/xdr.h
%{_includedir}/tirpc/rpcsvc/crypt.h
%{_includedir}/tirpc/rpcsvc/crypt.x
%{_includedir}/tirpc/spinlock.h
%{_includedir}/tirpc/un-namespace.h
