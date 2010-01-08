Name:		filesystem
Version:	2.1.9
Release:	%mkrel 9
Summary:	The basic directory layout for a Linux system
License:	Public Domain
Group:		System/Base
URL:		http://www.mandrivalinux.com/
Buildroot:	%{_tmppath}/%{name}-%{version}

%description
The filesystem package is one of the basic packages that is installed on
a Mandriva Linux system.  Filesystem  contains the basic directory layout
for a Linux operating system, including the correct permissions for the
directories.

%install
mkdir %{buildroot}

cd %{buildroot}

mkdir -p mnt media bin boot 
mkdir -p opt proc root sbin sys tmp
mkdir -p home initrd 
mkdir -p lib/modules

mkdir -p %{buildroot}%{_sysconfdir}/{profile.d,skel,security,ssl,sysconfig,default}
mkdir -p %{_lib}

mkdir -p %{buildroot}%{_prefix}/{etc,src,lib}
mkdir -p %{buildroot}/{%{_bindir},%{_libdir},%{_includedir},%{_sbindir},%{_datadir}}
mkdir -p %{buildroot}/%{_datadir}/{misc,pixmaps,applications,dict,doc,empty,fonts}
mkdir -p %{buildroot}/%{_datadir}/color/{icc,cmms,settings}

# man
mkdir -p %{buildroot}/%{_mandir}/man{1,2,3,4,5,6,7,8,9,n}
mkdir -p %{buildroot}/%{_infodir}
# games
mkdir -p %{buildroot}/{%{_gamesbindir},%{_gamesdatadir}}
mkdir -p %{buildroot}/{%{_libdir},%{_prefix}/lib}/games

mkdir -p %{buildroot}/%{_libdir}/gcc-lib
mkdir -p %{buildroot}/%{_prefix}/lib/gcc-lib

mkdir -p usr/local/{bin,doc,etc,games,lib,%{_lib},sbin,src,libexec,include}
mkdir -p usr/local/share/{man/man{1,2,3,4,5,6,7,8,9,n},info}

mkdir -p var/{local,log,nis,preserve,run,lib,empty}
mkdir -p var/spool/{mail,lpd}
mkdir -p var/lib/{games,misc}
mkdir -p var/{tmp,db,cache/man,opt,games,yp}
mkdir -p var/lock/subsys

ln -snf ../var/tmp usr/tmp
ln -snf spool/mail var/mail

%clean
rm -rf %{buildroot}

%files
%defattr(0755,root,root)
/bin
/boot
/etc
/home
/initrd
/lib
%if %{_lib} != lib
/%{_lib}
%endif
%dir /media
%dir /mnt
%dir /opt
/proc
/sys
%attr(750,root,root) /root
/sbin
%attr(1777,root,root) /tmp
%{_prefix}
%dir /var
/var/db
/var/lib
/var/local
/var/empty
%dir %attr(775,root,uucp) /var/lock
/var/lock/subsys
/var/cache
/var/log
/var/mail
/var/nis
/var/opt
/var/preserve
/var/run
%dir /var/spool
%attr(0755,root,daemon) %dir /var/spool/lpd
%attr(775,root,mail) /var/spool/mail
%attr(1777,root,root) /var/tmp
/var/yp



