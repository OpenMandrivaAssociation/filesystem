Name:		filesystem
Version:	2.1.9
Release:	22
Summary:	The basic directory layout for a Linux system
License:	Public Domain
Group:		System/Base
URL:		http://www.mandrivalinux.com/
Requires(pre):	setup
Source0:	filesystem.rpmlintrc

%description
The filesystem package is one of the basic packages that is installed on
a %{distribution} system.  Filesystem  contains the basic directory layout
for a Linux operating system, including the correct permissions for the
directories.

%prep

%build

%install

mkdir -p %{buildroot}/{mnt,media,bin,boot,dev}
mkdir -p %{buildroot}/{opt,proc,root,run,sbin,srv,sys,tmp}
mkdir -p %{buildroot}/{home,initrd}
mkdir -p %{buildroot}/lib/modules


mkdir -p %{buildroot}%{_sysconfdir}/{bash_completion.d,default,opt,pki,pm/{config.d,power.d,sleep.d},profile.d,security,skel,ssl,sysconfig,xdg,xinetd.d,X11/{applnk,fontpath.d}}

%ifarch x86_64
mkdir -p %{buildroot}{%{_prefix},{/local,}/libx32}
%endif
mkdir -p %{buildroot}{/%{_lib},%{_libdir},%{_usrsrc},%{_usrsrc}/debug}


mkdir -p %{buildroot}%{_prefix}/{etc,lib}
mkdir -p %{buildroot}{%{_bindir},%{_libdir},%{_includedir},%{_sbindir},%{_datadir}}
mkdir -p %{buildroot}%{_datadir}/{aclocal,appdata,applications,augeas,backgrounds,color/{icc,cmms,settings},desktop-directories,dict,doc,fonts,empty,fontsmisc,games,ghostscript{,/conf.d},gnome,icons,idl,mime-info,misc,omf,pixmaps,ppd,sounds,themes,xsessions,X11}

# man
mkdir -p %{buildroot}%{_mandir}/man{%(seq -s, 1 9),n}
mkdir -p %{buildroot}%{_infodir}
# games
mkdir -p %{buildroot}{%{_gamesbindir},%{_gamesdatadir}}
mkdir -p %{buildroot}{%{_libdir},%{_prefix}/lib}/games

mkdir -p %{buildroot}%{_libdir}/{gcc-lib,pm-utils/{module.d,power.d,sleep.d}}
mkdir -p %{buildroot}%{_prefix}/lib/{gcc-lib,sse2,tls,sse2}
mkdir -p %{buildroot}%{_prefix}/lib/debug/{bin,lib,%{_lib},usr/.dwz,sbin}
mkdir -p %{buildroot}%{_libexecdir}

mkdir -p %{buildroot}%{_prefix}/local/{bin,doc,etc,games,lib,%{_lib},sbin,src,libexec,include}
mkdir -p %{buildroot}%{_prefix}/local/share/{applications,desktop-directories}
mkdir -p %{buildroot}%{_prefix}/local/share/man/man{%(seq -s, 1 9),n}
mkdir -p %{buildroot}%{_prefix}/local/share/info

mkdir -p %{buildroot}%{_localedir}
mkdir -p %{buildroot}{%{_varrun},%{_logdir},%{_tmppath}}
mkdir -p %{buildroot}%{_var}/{adm,gopher,local,nis,preserve,empty}
mkdir -p %{buildroot}%{_var}/spool/{lpd,mail,news,uucp}
mkdir -p %{buildroot}%{_localstatedir}/lib/{games,misc,rpm-state}
mkdir -p %{buildroot}%{_var}/{db,cache/man,opt,games,gopher,yp}
mkdir -p %{buildroot}%{_var}/lock/subsys


ln -snf ../%{_var}/tmp %{buildroot}%{_prefix}/tmp
ln -snf spool/mail %{buildroot}%{_var}/mail

%files
%defattr(0755,root,root,-)
%dir %attr(555,root,root) /
%dir /bin
%attr(555,root,root) /boot
%dir /dev
%dir %{_sysconfdir}
%dir %{_sysconfdir}/bash_completion.d/
%dir %{_sysconfdir}/default
%dir %{_sysconfdir}/opt
%dir %{_sysconfdir}/pki
%dir %{_sysconfdir}/pm
%dir %{_sysconfdir}/profile.d
%dir %{_sysconfdir}/security
%dir %{_sysconfdir}/ssl
%dir %{_sysconfdir}/skel
%dir %{_sysconfdir}/sysconfig
%dir %{_sysconfdir}/xdg
%dir %{_sysconfdir}/xinetd.d
%dir %{_sysconfdir}/X11
%dir /home
%dir /initrd
%dir /lib
%dir /lib/modules
%if "%{_lib}" == "lib64"
%dir /%{_lib}
%ifarch x86_64
%dir /libx32
%endif
%endif
%dir /media
%dir /mnt
%dir /opt
%dir %attr(555,root,root) /proc
%dir %attr(550,root,root) /root
%dir /run
%dir /sbin
%dir /srv
%dir %attr(555,root,root) /sys
%dir %attr(1777,root,root) /tmp
%dir %{_prefix}
%dir %attr(555,root,root) %{_bindir}
%dir %{_gamesbindir}
%dir %{_includedir}
%dir %attr(555,root,root) %{_prefix}/lib
%dir %{_prefix}/lib/debug
%dir %{_prefix}/lib/debug/bin
%dir %ghost %{_prefix}/lib/debug/lib
%dir %ghost %{_prefix}/lib/debug/%{_lib}
%dir %ghost %{_prefix}/lib/debug/%{_prefix}
%dir %ghost %{_prefix}/lib/debug/%{_prefix}/.dwz
%dir %ghost %{_prefix}/lib/debug/sbin
%dir %attr(555,root,root) %{_prefix}/lib/games
%dir %attr(555,root,root) %{_prefix}/lib/sse2
%if "%{_lib}" == "lib64"
%dir %attr(555,root,root) %{_prefix}/%{_lib}
%ifarch x86_64
%dir %{_prefix}/libx32
%endif
%else
%dir %attr(555,root,root) %{_prefix}/lib/tls
%dir %attr(555,root,root) %{_prefix}/lib/X11
%dir %attr(555,root,root) %{_prefix}/lib/pm-utils
%endif
%dir %{_libexecdir}
%dir %{_prefix}/local
%dir %{_prefix}/local/bin
%dir %{_prefix}/local/doc
%dir %{_prefix}/local/etc
%dir %{_prefix}/local/games
%dir %{_prefix}/local/lib
%dir %{_prefix}/local/%{_lib}
%ifarch x86_64
%dir %{_prefix}/local/libx32
%endif
%dir %{_prefix}/local/sbin
%dir %{_prefix}/local/src
%dir %{_prefix}/local/libexec
%dir %{_prefix}/local/include
%dir %{_prefix}/local/share/applications
%dir %{_prefix}/local/share/desktop-directories
%dir %{_prefix}/local/share/
%dir %{_prefix}/local/share/man
%dir %{_prefix}/local/share/man/man*
%dir %{_prefix}/local/share/info
%dir %attr(555,root,root) %{_sbindir}
%dir %{_datadir}
%dir %{_datadir}/aclocal
%dir %{_datadir}/appdata
%dir %{_datadir}/applications
%dir %{_datadir}/augeas
%dir %{_datadir}/backgrounds
%dir %{_datadir}/color
%dir %{_datadir}/color/icc
%dir %{_datadir}/color/cmms
%dir %{_datadir}/color/settings
%dir %{_datadir}/desktop-directories
%dir %{_datadir}/dict
%dir %{_datadir}/doc
%dir %attr(555,root,root) %{_datadir}/empty
%dir %{_datadir}/fonts
%dir %{_datadir}/fontsmisc
%dir %{_datadir}/games
%dir %{_datadir}/ghostscript
%dir %{_datadir}/ghostscript/conf.d
%dir %{_datadir}/gnome
%dir %{_datadir}/icons
%dir %{_datadir}/idl
%dir %{_datadir}/mime-info
%dir %{_datadir}/misc
%dir %{_datadir}/omf
%dir %{_datadir}/pixmaps
%dir %{_datadir}/sounds
%dir %{_datadir}/themes
%dir %{_datadir}/xsessions
%dir %{_datadir}/X11
%dir %{_localedir}
%dir %{_localstatedir}/lib
%dir %{_localstatedir}/lib/games
%dir %{_localstatedir}/lib/misc
%dir %{_localstatedir}/lib/rpm-state
%dir %{_logdir}
%dir %{_mandir}
%dir %{_mandir}/man*
%dir %{_usrsrc}
%dir %{_usrsrc}/debug
%dir %{_prefix}/tmp
%dir %{_var}
%dir %{_var}/adm
%dir %{_var}/cache
%dir %{_var}/cache/man
%dir %{_var}/db
%dir %{_var}/empty
%dir %{_var}/games
%dir %{_var}/gopher
%dir %{_var}/local
%dir %attr(775,root,uucp) /var/lock
%dir %{_var}/lock/subsys
%dir %{_var}/mail
%dir %{_var}/nis
%dir %{_var}/opt
%dir %{_var}/preserve
%dir %{_varrun}
%dir %{_var}/spool
%dir %attr(755,root,root) %{_var}/spool/lpd
%dir %attr(775,root,mail) %{_var}/spool/mail
%dir %attr(775,root,news) /var/spool/news
%dir %attr(775,root,uucp) %{_var}/spool/uucp
%dir %attr(1777,root,root) %{_var}/tmp
%dir %{_var}/yp
