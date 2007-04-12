Name:		filesystem
Version:	2.1.8
Release:	%mkrel 5
Summary:	The basic directory layout for a Linux system
License:	Public Domain
Group:		System/Base
URL:		http://www.mandrivalinux.com/
Requires:	setup
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

mkdir -p var/{local,log,nis,preserve,run,lib}
mkdir -p var/spool/{mail,lpd}
mkdir -p var/lib/{games,misc}
mkdir -p var/{tmp,db,cache/man,opt,games,yp}
mkdir -p var/lock/subsys

ln -snf ../var/tmp usr/tmp
ln -snf spool/mail var/mail

%clean
rm -rf %{buildroot}

%post -p <lua>
function mkdir_missing(dir)
    if posix.stat(dir) == nil then 
        posix.mkdir(dir)
    end
end

mkdir_missing("/mnt/disk")
mkdir_missing("/media/floppy")
mkdir_missing("/media/cdrom")

%triggerun -- filesystem < 2.1.8
# only on upgrade we keep /usr/lib/X11 and /usr/X11R6/lib/X11 linked together
# on install, /usr/X11R6/lib/X11 will be a directory
if rm -f /usr/%{_lib}/X11 && mv /usr/X11R6/lib/X11 /usr/%{_lib} 2>/dev/null; then
    echo "/usr/lib/X11 is no more a symlink, keeping /usr/X11R6/lib/X11 linked to it for upgrade"
    ln -s ../../%{_lib}/X11 /usr/X11R6/lib/X11
fi

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
%dir %attr(775,root,root) /var/lock
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



