%define	major 1
%define libname %mklibname tirpc %{major}
%define develname %mklibname tirpc -d

Summary:	Transport Independent RPC Library
Name:		libtirpc
Version:	0.2.2
Release:	%mkrel 3
License:	GPL
Group:		System/Libraries
URL:		http://sourceforge.net/projects/libtirpc
Source0:	http://downloads.sourceforge.net/libtirpc/%{name}-%{version}.tar.bz2
Patch0:     01-remove-des-crypt.diff
BuildRequires:	pkgconfig
BuildRequires:	gssglue-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

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
Requires:   %{name} = %{version}-%{release}

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
%patch0 -p1

%build
export CFLAGS="%{optflags} -fPIC"
autoreconf -fi
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
rm -f %{buildroot}%{_libdir}/*.la

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/netconfig

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/libtirpc.pc
%{_includedir}/tirpc
%{_mandir}/man3/*
%{_mandir}/man5/*


%changelog
* Wed Jun 15 2011 Guillaume Rousse <guillomovitch@mandriva.org> 0.2.2-1mdv2011.0
+ Revision: 685284
- new version

* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.1-4
+ Revision: 660286
- mass rebuild

* Thu Nov 25 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.1-3mdv2011.0
+ Revision: 601062
- rebuild

* Mon Mar 29 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.2.1-2mdv2010.1
+ Revision: 528925
- remove .la file, it breaks gssd by altering nfs-utils linking arguments order

* Fri Dec 04 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.2.1-1mdv2010.1
+ Revision: 473560
- update to new version 0.2.1

* Mon Jun 08 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.2.0-4mdv2010.0
+ Revision: 384078
- oops

* Mon Jun 08 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.2.0-3mdv2010.0
+ Revision: 384077
- move configuration file in its own package

* Mon Jun 08 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.2.0-2mdv2010.0
+ Revision: 383877
- fix missing configuration file

* Sun Jun 07 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.2.0-1mdv2010.0
+ Revision: 383548
- new version

* Thu Dec 11 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.1.10-1mdv2009.1
+ Revision: 312870
- update to new version 0.1.10

* Fri Sep 05 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.1.9-1mdv2009.0
+ Revision: 281207
- new version
  drop all patches, merged upstream
  spec cleanup

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.1.7-7mdv2009.0
+ Revision: 223012
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-6mdv2008.1
+ Revision: 179005
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Sep 06 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-4mdv2008.0
+ Revision: 80802
- bump release (again)
- bump release
- sync with libtirpc-0.1.7-10.fc8.src.rpm
- added P101 to make it build against libgssglue instead
- new devel naming

* Tue Apr 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-1mdv2008.0
+ Revision: 14044
- Import libtirpc



* Tue Apr 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.7-1mdv2007.1
- initial Mandriva package

* Mon Mar 26 2007 Steve Dickson <steved@redhat.com> 0.1.7-5
- Fixed Unowned Directory RPM problem (bz 233873)

* Mon Aug 28 2006 Steve Dickson <steved@redhat.com> 0.1.7-4
- Fixed undefined symbol (bz 204296)

* Mon Aug 14 2006 Steve Dickson <steved@redhat.com> 0.1.7-3
- Added in svc_auth_none needed by the GSSAPI code.
- Added compile define for ppc64 archs

* Fri Aug 11 2006 Steve Dickson <steved@redhat.com> 0.1.7-2
- Uncommented tcp6 and udp6 in the default /etc/netconfig file.
- Added hooks to used the libgssapi library.

* Fri Aug  4 2006 Steve Dickson <steved@redhat.com> 0.1.7-1
- Initial commit
