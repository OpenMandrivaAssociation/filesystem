Name:		filesystem
Version:	2.1.9
Release:	14
Summary:	The basic directory layout for a Linux system
License:	Public Domain
Group:		System/Base
URL:		http://www.mandrivalinux.com/
Source0:	%{name}.rpmlintrc

%description
The filesystem package is one of the basic packages that is installed on
a Mandriva Linux system.  Filesystem  contains the basic directory layout
for a Linux operating system, including the correct permissions for the
directories.

%install
mkdir -p %{buildroot}

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





%changelog
* Sun May 08 2011 Funda Wang <fwang@mandriva.org> 2.1.9-11mdv2011.0
+ Revision: 672341
- fix install

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.9-10mdv2011.0
+ Revision: 605129
- rebuild

* Fri Jan 08 2010 Frederic Crozat <fcrozat@mandriva.com> 2.1.9-9mdv2010.1
+ Revision: 487466
- Add colors directories

* Sat Dec 05 2009 Olivier Thauvin <nanardon@mandriva.org> 2.1.9-8mdv2010.1
+ Revision: 473995
- don't requires setup package, no reason to require it, and can help about #56228

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.1.9-7mdv2010.0
+ Revision: 424435
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 2.1.9-6mdv2009.1
+ Revision: 350993
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 2.1.9-5mdv2009.0
+ Revision: 220792
- rebuild

* Wed Mar 19 2008 Frederic Crozat <fcrozat@mandriva.com> 2.1.9-4mdv2008.1
+ Revision: 188863
- No longer create /mnt/disk, /media/floppy and /media/cdrom, they are handled by hal

* Sun Mar 02 2008 Olivier Blin <oblin@mandriva.com> 2.1.9-3mdv2008.1
+ Revision: 177778
- make /var/lock owned by the uucp group (#16739)

* Sat Jan 12 2008 Thierry Vignaud <tv@mandriva.org> 2.1.9-2mdv2008.1
+ Revision: 149724
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Jul 27 2007 Olivier Thauvin <nanardon@mandriva.org> 2.1.9-1mdv2008.0
+ Revision: 56383
- provide a /var/empty at it is need by some services

* Thu Jul 05 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 2.1.8-6mdv2008.0
+ Revision: 48313
- removing trigger which was supposed to handle the
  /usr/X11R6/lib/X11 transiction to /usr/lib/X11. It doesn't handle
  all upgrade scenarios (see #23423). A better solution was to fix
  the directories on x11-server-common package and there conflict
  with older filesystem packages which own /usr/X11R6/lib/X11/.


* Tue Dec 05 2006 Pixel <pixel@mandriva.com> 2.1.8-5mdv2007.0
+ Revision: 91242
- from from /mnt to /media for removable media (cdrom, floppy, usb...)

  + Olivier Thauvin <nanardon@mandriva.org>
    - make spec readable

* Fri Aug 04 2006 Olivier Thauvin <nanardon@mandriva.org> 2.1.8-4mdv2007.0
+ Revision: 49578
- readd trigger, but using lua to avoid one dependencies
- don't provide /mnt/*

* Thu Aug 03 2006 Olivier Thauvin <nanardon@mandriva.org> 2.1.8-3mdv2007.0
+ Revision: 43018
- avoid a trigger to avoid sh requrirement, for the other, no solution currently :\
- Import filesystem

* Thu Jun 15 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.8-2mdv2007.0
- add /etc/default
- some spec cleanup

* Tue May 23 2006 Pixel <pixel@mandriva.com> 2.1.8-2mdk
- move things from /usr/X11R6/lib/X11 into /usr/lib/X11 since /usr/lib/X11 is no more a symlink
  (only on upgrade, later on, /usr/X11R6/lib/X11 and /usr/lib/X11 can have separate lives...)

* Sat May 20 2006 Pixel <pixel@mandriva.com> 2.1.8-1mdk
- drop links /usr/%%lib/X11 /usr/bin/X11
- drop dirs /usr/X11R6 /usr/X11R6/bin /usr/X11R6/include /usr/X11R6/lib /usr/X11R6/man
  (since /usr/X11R6 is deprecated)

* Wed Feb 08 2006 Thierry Vignaud <tvignaud@mandriva.com> 2.1.7-2mdk
- fix typo in description (#20993)

* Thu Feb 02 2006 Frederic Crozat <fcrozat@mandriva.com> 2.1.7-1mdk
- Own /usr/share/fonts
- fix url

* Thu Jun 16 2005 Olivier Thauvin <nanardon@mandriva.org> 2.1.6-1mdk
- fix link /usr/%%lib/X11 (to /usr/lib/X11 on lib64, hope it's ok)
- spec cleanup

* Mon Jan 05 2004 Frederic Lepied <flepied@mandrakesoft.com> 2.1.5-1mdk
- simplified spec file
- make it lib64 aware (so no more noarch)
- switched to direct build of the directories
- added /usr/share/dict /etc/sysconfig /etc/skel /etc/ssl

