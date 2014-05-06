Name:		filesystem
Version:	2.1.9
Release:	22
Summary:	The basic directory layout for a Linux system
License:	Public Domain
Group:		System/Base
URL:		http://www.mandrivalinux.com/
Requires:	setup
Source0:	filesystem.rpmlintrc

%description
The filesystem package is one of the basic packages that is installed on
a %{distribution} system.  Filesystem  contains the basic directory layout
for a Linux operating system, including the correct permissions for the
directories.

%prep

%build

%install
mkdir -p %{buildroot}/%{_lib}
mkdir -p %{buildroot}%{_libdir}

mkdir -p %{buildroot}/{mnt,media,bin,boot,dev}
mkdir -p %{buildroot}/{opt,proc,root,run,sbin,srv,sys,tmp}
mkdir -p %{buildroot}/{home,initrd}
mkdir -p %{buildroot}/lib/modules


mkdir -p %{buildroot}%{_sysconfdir}/{profile.d,security,ssl,sysconfig,default,opt,xinetd.d}
mkdir -p %{_lib}

mkdir -p %{buildroot}%{_prefix}/{etc,src,lib}
mkdir -p %{buildroot}{%{_bindir},%{_libdir},%{_includedir},%{_sbindir},%{_datadir}}
mkdir -p %{buildroot}%{_datadir}/{misc,pixmaps,applications,desktop-directories,dict,doc,empty,fonts}
mkdir -p %{buildroot}%{_datadir}/color/{icc,cmms,settings}

# man
mkdir -p %{buildroot}%{_mandir}/man{1,2,3,4,5,6,7,8,9,n}
mkdir -p %{buildroot}%{_infodir}
# games
mkdir -p %{buildroot}{%{_gamesbindir},%{_gamesdatadir}}
mkdir -p %{buildroot}{%{_libdir},%{_prefix}/lib}/games

mkdir -p %{buildroot}%{_libdir}/gcc-lib
mkdir -p %{buildroot}%{_prefix}/lib/gcc-lib

mkdir -p %{buildroot}%{_prefix}/local/{bin,doc,etc,games,lib,%{_lib},sbin,src,libexec,include}
mkdir -p %{buildroot}%{_prefix}/local/share/{applications,desktop-directories}
mkdir -p %{buildroot}%{_prefix}/local/share/{man/man{1,2,3,4,5,6,7,8,9,n},info}
mkdir -p %{buildroot}%{_datadir}/ppd

mkdir -p %{buildroot}%{_var}/{adm,local,log,nis,preserve,run,lib,empty}
mkdir -p %{buildroot}%{_var}/spool/{lpd,mail,news,uucp}
mkdir -p %{buildroot}%{_localstatedir}/lib/{games,misc}
mkdir -p %{buildroot}%{_var}/{tmp,db,cache/man,opt,games,yp}
mkdir -p %{buildroot}%{_var}/lock/subsys

ln -snf ../%{_var}/tmp %{buildroot}%{_prefix}/tmp
ln -snf spool/mail %{buildroot}%{_var}/mail

%files
%defattr(0755,root,root)
/bin
/dev
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
/srv
/sys
%attr(750,root,root) /root
/sbin
%attr(1777,root,root) /tmp
%{_prefix}
%dir /var
%{_var}/adm
%{_var}/db
%{_localstatedir}/lib
%{_var}/local
%{_var}/empty
%dir %attr(775,root,uucp) /var/lock
%{_var}/lock/subsys
%{_var}/cache
%{_var}/log
%{_var}/mail
%{_var}/nis
%{_var}/opt
%{_var}/preserve
%{_var}/run
%dir /var/spool
%dir %attr(0755,root,daemon) /var/spool/lpd
%attr(775,root,mail) /var/spool/mail
%attr(1777,root,root) /var/tmp
%attr(775,root,news) /var/spool/news
%attr(775,root,uucp) /var/spool/uucp
%{_var}/yp
