%define debug_package %{nil}

Name:		filesystem
Version:	5.0
Release:	1
Summary:	The basic directory layout for a Linux system
License:	Public Domain
Group:		System/Base
URL:		%{disturl}
Source0:	filesystem.rpmlintrc
# Raw source1 URL: https://fedorahosted.org/filesystem/browser/lang-exceptions?format=raw
Source1:	https://fedorahosted.org/filesystem/browser/lang-exceptions
Source2:	iso_639.sed
Source3:	iso_3166.sed
BuildRequires:	iso-codes
Requires(pre):	setup
Conflicts:	setup < 2.8.9-3
# (tpg) fix upgrade from 2014.x
Conflicts:	man-pages < 4.05
Conflicts:	man-pages-cs < 0.18.20090209-19
Conflicts:	man-pages-da < 0.1.1-25
Conflicts:	man-pages-de < 0.9-12
Conflicts:	man-pages-es < 1.55-20
Conflicts:	man-pages-fr < 3.03.0-24
Conflicts:	man-pages-hu < 0.2.2-28
Conflicts:	man-pages-id < 0.1-30
Conflicts:	man-pages-it < 2.80-18
Conflicts:	man-pages-ja < 20091215-17
Conflicts:	man-pages-ko < 20050219-23
Conflicts:	man-pages-pl < 0.6-24
Conflicts:	man-pages-pt_BR < 0.1-21
Conflicts:	man-pages-ru < 3.41-25
Conflicts:	man-pages-zh < 1.5-21

%description
The filesystem package is one of the basic packages that is installed on
a %{distribution} system. Filesystem contains the basic directory layout
for a Linux operating system, including the correct permissions for the
directories.

%prep
%setup -Tcn %{name}-%{version}

%build

%install
rm -f filelist

mkdir -p %{buildroot}/{mnt,media,boot,dev}
mkdir -p %{buildroot}/{opt,root,run,srv,tmp}
mkdir -p %{buildroot}/{home,initrd}
mkdir -p %{buildroot}/usr/%{_target_platform}/{bin,lib}
mkdir -p %{buildroot}/usr/share
ln -s ../share %{buildroot}/usr/%{_target_platform}/share

ln -s bin %{buildroot}/usr/%{_target_platform}/sbin
for i in bin sbin; do
	ln -s usr/%{_target_platform}/$i %{buildroot}/$i
done
for i in bin sbin libexec; do
	ln -s %{_target_platform}/$i %{buildroot}/usr/$i
done
%ifarch %{x86_64}
ln -s usr/%{_target_platform}/lib %{buildroot}/lib64
ln -s usr/i686-openmandriva-linux-gnu/lib %{buildroot}/lib
ln -s i686-openmandriva-linux-gnu/lib %{buildroot}/usr/lib
ln -s usr/x86_64-openmandriva-linux-gnux32/lib %{buildroot}/libx32
ln -s x86_64-openmandriva-linux-gnux32/lib %{buildroot}/usr/libx32
%endif
%ifarch %{aarch64}
ln -s usr/%{_target_platform}/lib %{buildroot}/lib64
ln -s usr/armv7hnl-openmandriva-linux-gnueabihf/lib %{buildroot}/lib
%endif

mkdir -p %{buildroot}%{_sysconfdir}/{bash_completion.d,default,opt,pki,pm/{config.d,power.d,sleep.d},rwtab.d,statetab.d,security,skel,ssl,sysconfig,xdg/autostart,X11/{applnk,fontpath.d,xinit/{xinitrc,xinput}.d},rwtab.d,statetab.d}

mkdir -p %{buildroot}%{_usrsrc}{,/debug}

mkdir -p %{buildroot}%{_prefix}/etc
mkdir -p %{buildroot}{%{_bindir},%{_includedir},%{_sbindir},%{_datadir}}
mkdir -p %{buildroot}%{_datadir}/{aclocal,appdata,applications,augeas,backgrounds,color/{icc,cmms,settings},desktop-directories,dict,doc,fonts,empty,fontsmisc,games,icons,idl,mime-info,misc,omf,pixmaps,ppd,sounds,themes,xsessions,X11}
mkdir -p %{buildroot}%{_infodir}
# games
mkdir -p %{buildroot}{%{_gamesbindir},%{_gamesdatadir}}

mkdir -p %{buildroot}%{_libdir}/{pm-utils/{module.d,power.d,sleep.d}}

mkdir -p %{buildroot}%{_prefix}/local/{bin,doc,etc,games,lib,src,libexec,include}
ln -s bin %{buildroot}%{_prefix}/local/sbin
%if "%{_lib}" == "lib64"
mkdir -p %{buildroot}%{_prefix}/local/%{_lib}
%endif
%ifarch %{x86_64}
mkdir -p %{buildroot}%{_prefix}/local/libx32
%endif

mkdir -p %{buildroot}%{_prefix}/local/share/{applications,desktop-directories}
for i in $(seq 1 9); do
	mkdir -p -m755 %{buildroot}%{_prefix}/local/share/man/man${i}{,x}
done
mkdir -p %{buildroot}%{_prefix}/local/share/man/mann
mkdir -p %{buildroot}%{_prefix}/local/share/info

mkdir -p %{buildroot}%{_localedir}
mkdir -p %{buildroot}{%{_logdir},%{_tmppath}}
mkdir -p %{buildroot}%{_var}/{adm,local,nis,preserve,empty}
mkdir -p %{buildroot}%{_var}/spool/{lpd,mail,news,uucp}
mkdir -p %{buildroot}%{_localstatedir}/lib/{games,misc,rpm-state}
mkdir -p %{buildroot}%{_var}/{db,cache,opt,games,yp}
mkdir -p %{buildroot}/run/lock

ln -srf %{buildroot}/run %{buildroot}%{_var}/run
ln -srf %{buildroot}/run/lock %{buildroot}%{_var}/lock
ln -srf %{buildroot}%{_tmppath} %{buildroot}%{_prefix}/tmp
ln -srf %{buildroot}%{_var}/spool/mail %{buildroot}%{_var}/mail

sed -n -f %{SOURCE2} %{_datadir}/xml/iso-codes/iso_639.xml \
  > iso_639.tab
sed -n -f %{SOURCE3} %{_datadir}/xml/iso-codes/iso_3166.xml \
  > iso_3166.tab

grep -v "^$" iso_639.tab | grep -v "^#" | while read a b c d ; do
    [[ "$d" =~ "^Reserved" ]] && continue
    [[ "$d" =~ "^No linguistic" ]] && continue

    locale=$c
    if [ "$locale" = "XX" ]; then
        locale=$b
    fi
    echo "%lang(${locale}) %{_localedir}/${locale}" >> filelist
    echo "%lang(${locale}) %ghost %config(missingok) %{_mandir}/${locale}" >>filelist
done
cat %{SOURCE1} | grep -v "^#" | grep -v "^$" | while read loc ; do
    locale=$loc
    locality=
    special=
    [[ "$locale" =~ "@" ]] && locale=${locale%%%%@*}
    [[ "$locale" =~ "_" ]] && locality=${locale##*_}
    [[ "$locality" =~ "." ]] && locality=${locality%%%%.*}
    [[ "$loc" =~ "_" ]] || [[ "$loc" =~ "@" ]] || special=$loc

    # If the locality is not official, skip it
    if [ -n "$locality" ]; then
        grep -q "^$locality" iso_3166.tab || continue
    fi
    # If the locale is not official and not special, skip it
    if [ -z "$special" ]; then
        egrep -q "[[:space:]]${locale%%_*}[[:space:]]" \
           iso_639.tab || continue
    fi
    echo "%lang(${locale})	%{_localedir}/${loc}" >> filelist
    echo "%lang(${locale})  %ghost %config(missingok) %{_mandir}/${loc}" >> filelist
done

cat filelist | grep "locale" | while read a b ; do
    mkdir -p -m755 %{buildroot}${b}/LC_MESSAGES
done

cat filelist | grep "/share/man" | while read a b c d; do
    for i in $(seq 1 9); do
	mkdir -p -m755 %{buildroot}${d}/man${i}{,x}
    done
    for i in 0p 1p 3p n; do
	mkdir -p -m755 %{buildroot}${d}/man${i}
    done
done

# non-localized man pages
for i in $(seq 1 9); do
    mkdir -p -m755 %{buildroot}%{_mandir}/man${i}{,x}
done
for i in 0p 1p 3p n; do
    mkdir -p -m755 %{buildroot}%{_mandir}/man${i}
done

%pretrans -p <lua>
--# If we are running in pretrans in a fresh root, there is no /usr and
--# symlinks. We cannot be sure, to be the very first rpm in the
--# transaction list. Let's create the needed base directories and symlinks
--# here, to place the files from other packages in the right locations.
--# When our rpm is unpacked by cpio, it will set all permissions and modes
--# later.

--# Move all files in a source directory to a destination directory -- useful
--# when we can't just move the directory because we're collecting multiple
--# previous directories in one new one...
local function mvdir(source, dest)
	for i,p in pairs(posix.dir(source)) do
		os.rename(source .. "/" .. p, dest .. "/" .. p)
	end
end
posix.mkdir("/usr")
posix.mkdir("/usr/%{_target_platform}")
posix.mkdir("/usr/%{_target_platform}/bin")
posix.mkdir("/usr/%{_target_platform}/lib")
posix.mkdir("/usr/%{_target_platform}/libexec")
%ifarch %{x86_64}
posix.mkdir("/usr/i686-openmandriva-linux-gnu")
posix.mkdir("/usr/i686-openmandriva-linux-gnu/lib")
%endif
%ifarch %{aarch64}
posix.mkdir("/usr/armv7hnl-openmandriva-linux-gnueabihf")
posix.mkdir("/usr/armv7hnl-openmandriva-linux-gnueabihf/lib")
%endif

--# If we're updating from 4.x, we need to move contents of what used to
--# be directories around...
st=posix.stat("/bin")
if st and st.type == "directory" then
	mvdir("/bin", "/usr/%{_target_platform}/bin")
	mvdir("/sbin", "/usr/%{_target_platform}/bin")
	mvdir("/usr/bin", "/usr/%{_target_platform}/bin")
	mvdir("/usr/sbin", "/usr/%{_target_platform}/bin")
	mvdir("/usr/libexec", "/usr/%{_target_platform}/libexec")

	posix.rmdir("/bin")
	posix.rmdir("/sbin")
	posix.rmdir("/usr/bin")
	posix.rmdir("/usr/sbin")
	posix.rmdir("/usr/libexec")
%ifarch %{x86_64} %{aarch64}
	mvdir("/lib64", "/usr/%{_target_platform}/lib")
	mvdir("/usr/lib64", "/usr/%{_target_platform}/lib")
	posix.rmdir("/lib64")
	posix.rmdir("/usr/lib64")
%ifarch %{x86_64}
	mvdir("/lib", "/usr/i686-openmandriva-linux-gnu/lib")
	mvdir("/usr/lib", "/usr/i686-openmandriva-linux-gnu/lib")
%endif
%ifarch %{aarch64}
	mvdir("/lib", "/usr/armv7hnl-openmandriva-linux-gnueabihf/lib")
	mvdir("/usr/lib", "/usr/armv7hnl-openmandriva-linux-gnueabihf/lib")
%endif
%else
	mvdir("/lib", "/usr/%{_target_platform}/lib")
	mvdir("/usr/lib", "/usr/%{_target_platform}/lib")
	posix.rmdir("/lib")
	posix.rmdir("/usr/lib")
%endif
end

%ifarch %{x86_64} %{aarch64}
posix.symlink("usr/%{_target_platform}/lib", "/lib64")
posix.symlink("usr/%{_target_platform}/lib", "/usr/lib64")
%else
posix.symlink("usr/%{_target_platform}/lib", "/lib")
posix.symlink("usr/%{_target_platform}/lib", "/usr/lib")
%endif
posix.symlink("usr/%{_target_platform}/bin", "/bin")
posix.symlink("usr/%{_target_platform}/bin", "/sbin")
posix.symlink("%{_target_platform}/bin", "/usr/bin")
posix.symlink("%{_target_platform}/bin", "/usr/sbin")
posix.symlink("%{_target_platform}/libexec", "/usr/libexec")

posix.mkdir("/usr/lib/debug")
posix.mkdir("/run")
posix.mkdir("/proc")
posix.mkdir("/sys")
posix.chmod("/proc", 0555)
posix.chmod("/sys", 0555)
posix.mkdir("/var")
posix.symlink("../run", "/var/run")
posix.symlink("../run/lock", "/var/lock")
return 0

%files -f filelist
%defattr(0755,root,root,-)
%dir %attr(555,root,root) /
/bin
%attr(555,root,root) /boot
/dev
%dir %{_sysconfdir}
%dir %{_sysconfdir}/bash_completion.d/
%dir %{_sysconfdir}/default
%dir %{_sysconfdir}/opt
%dir %{_sysconfdir}/pki
%dir %{_sysconfdir}/pm
%dir %{_sysconfdir}/rwtab.d
%dir %{_sysconfdir}/statetab.d
%dir %{_sysconfdir}/security
%dir %{_sysconfdir}/ssl
%dir %{_sysconfdir}/skel
%dir %{_sysconfdir}/sysconfig
%dir %{_sysconfdir}/xdg
%dir %{_sysconfdir}/X11
%dir %{_sysconfdir}/rwtab.d
%dir %{_sysconfdir}/statetab.d 
%dir /home
%dir /initrd
/usr/%{_target_platform}
/lib
/usr/lib
%ifarch %{x86_64} %{aarch64}
/lib64
/usr/lib64
%ifarch %{x86_64}
/libx32
/usr/libx32
%endif
%endif
%dir /media
%dir /mnt
%dir /opt
%ghost %attr(555,root,root) /proc
%dir %attr(550,root,root) /root
%dir %{_rundir}
%dir %attr(775,root,uucp) /run/lock
/sbin
%dir /srv
%ghost %attr(555,root,root) /sys
%dir %attr(1777,root,root) /tmp
%dir /usr
/usr/bin
%dir %{_gamesbindir}
%dir %{_includedir}
%{_prefix}/lib
%ifarch %{x86_64}
%{_prefix}/libx32
%endif
%if "%{_lib}" == "lib64"
%dir %attr(555,root,root) %{_prefix}/%{_lib}
%endif
%if "%{_lib}" == "lib"
%dir %attr(555,root,root) %{_prefix}/lib/X11
%dir %attr(555,root,root) %{_prefix}/lib/pm-utils
%endif
%{_libexecdir}
%dir %{_prefix}/local
%dir %{_prefix}/local/bin
%dir %{_prefix}/local/doc
%dir %{_prefix}/local/etc
%dir %{_prefix}/local/games
%dir %{_prefix}/local/lib
%if "%{_lib}" == "lib64"
%dir %{_prefix}/local/%{_lib}
%endif
%ifarch %{x86_64}
%dir %{_prefix}/local/libx32
%endif
%{_prefix}/local/sbin
%dir %{_prefix}/local/src
%dir %{_prefix}/local/libexec
%dir %{_prefix}/local/include
%dir %{_prefix}/local/share/applications
%dir %{_prefix}/local/share/desktop-directories
%dir %{_prefix}/local/share/
%dir %{_prefix}/local/share/man/
%dir %{_prefix}/local/share/man/man[1-9]
%dir %{_prefix}/local/share/man/man[1-9]x
%dir %{_prefix}/local/share/man/mann
%dir %{_prefix}/local/share/info
/usr/sbin
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
%dir %{_mandir}/man[013]p
%dir %{_mandir}/man[1-9]
%dir %{_mandir}/man[1-9]x
%dir %{_mandir}/mann
%dir %{_usrsrc}
%dir %{_usrsrc}/debug
%dir %{_var}
%dir %{_var}/adm
%dir %{_var}/cache
%dir %{_var}/db
%dir %{_var}/empty
%dir %{_var}/games
%dir %{_var}/local
%dir %{_var}/nis
%dir %{_var}/opt
%dir %{_var}/preserve
%dir %{_var}/spool
%dir %attr(755,root,root) %{_var}/spool/lpd
%dir %attr(775,root,mail) %{_var}/spool/mail
%dir %attr(775,root,news) %{_var}/spool/news
%dir %attr(775,root,uucp) %{_var}/spool/uucp
%dir %attr(1777,root,root) %{_tmppath}
%dir %{_var}/yp
# Symlinks to the "right" location...
%{_var}/mail
# Legacy symlinks...
/var/run
%{_prefix}/tmp
%{_var}/lock
