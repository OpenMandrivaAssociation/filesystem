Name:		filesystem
Version:	3.0
Release:	16
Summary:	The basic directory layout for a Linux system
License:	Public Domain
Group:		System/Base
URL:		%{disturl}
# attempt at fixing up screwup by others cluelessly trying to merge this
# package with setup package
Requires(post):	setup >= 2.8.8-12
Requires(pretrans):	setup >= 2.8.8-12
Source0:	filesystem.rpmlintrc
# Raw source1 URL: https://fedorahosted.org/filesystem/browser/lang-exceptions?format=raw
Source1:	https://fedorahosted.org/filesystem/browser/lang-exceptions
Source2:	iso_639.sed
Source3:	iso_3166.sed
BuildRequires:	iso-codes


%description
The filesystem package is one of the basic packages that is installed on
a %{distribution} system.  Filesystem  contains the basic directory layout
for a Linux operating system, including the correct permissions for the
directories.

%prep
%setup -Tcn %{name}-%{version}

%build

%install
rm -f filelist

mkdir -p %{buildroot}/{mnt,media,bin,boot,dev}
mkdir -p %{buildroot}/{opt,proc,root,run,sbin,srv,sys,tmp}
mkdir -p %{buildroot}/{home,initrd}
mkdir -p %{buildroot}/lib/modules


mkdir -p %{buildroot}%{_sysconfdir}/{bash_completion.d,default,opt,pki,pm/{config.d,power.d,sleep.d},security,skel,ssl,sysconfig,xdg,xinetd.d,X11/{applnk,fontpath.d}}

%if "%{_lib}" == "lib64"
mkdir -p %{buildroot}{/%{_lib},%{_libdir}}
%endif
%ifarch x86_64
mkdir -p %{buildroot}{,%{_prefix},%{_prefix}/local}/libx32
%endif
mkdir -p %{buildroot}%{_usrsrc}{,/debug}


mkdir -p %{buildroot}%{_prefix}/{etc,lib}
mkdir -p %{buildroot}{%{_bindir},%{_includedir},%{_sbindir},%{_datadir}}
mkdir -p %{buildroot}%{_datadir}/{aclocal,appdata,applications,augeas,backgrounds,color/{icc,cmms,settings},desktop-directories,dict,doc,fonts,empty,fontsmisc,games,ghostscript{,/conf.d},gnome,icons,idl,mime-info,misc,omf,pixmaps,ppd,sounds,themes,xsessions,X11}
mkdir -p %{buildroot}%{_infodir}
# games
mkdir -p %{buildroot}{%{_gamesbindir},%{_gamesdatadir}}
mkdir -p %{buildroot}%{_prefix}/lib/games
%if "%{_lib}" == "lib64"
mkdir -p %{buildroot}%{_libdir}/lib/games
%endif


mkdir -p %{buildroot}%{_libdir}/{gcc-lib,pm-utils/{module.d,power.d,sleep.d}}
mkdir -p %{buildroot}%{_prefix}/lib/{gcc-lib,sse2,tls,sse2}
# deprecated..?
mkdir -p %{buildroot}%{_prefix}/lib/X11
mkdir -p %{buildroot}%{_prefix}/lib/debug/{bin,lib,usr/.dwz,sbin}
%if "%{_lib}" == "lib64"
mkdir -p %{buildroot}%{_prefix}/lib/debug/%{_lib}
%endif
%ifarch x86_64
mkdir -p %{buildroot}%{_prefix}/lib/debug/libx32
%endif

mkdir -p %{buildroot}%{_libexecdir}

mkdir -p %{buildroot}%{_prefix}/local/{bin,doc,etc,games,lib,sbin,src,libexec,include}
%if "%{_lib}" == "lib64"
mkdir -p %{buildroot}%{_prefix}/local/%{_lib}
%endif
%ifarch x86_64
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
mkdir -p %{buildroot}%{_var}/{adm,gopher,local,nis,preserve,empty}
mkdir -p %{buildroot}%{_var}/spool/{lpd,mail,news,uucp}
mkdir -p %{buildroot}%{_localstatedir}/lib/{games,misc,rpm-state}
mkdir -p %{buildroot}%{_var}/{db,cache/man,opt,games,gopher,yp}
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
    echo "%lang(${locale})	%{_localedir}/${locale}" >> filelist
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
vr = posix.stat("/var/run")
if vr and vr.type ~= "link" then
    os.rename("/var/run", "/var/run.old")
end

vl = posix.stat("/var/lock")
if vl and vl.type ~= "link" then
    os.rename("/var/lock", "/var/lock.old")
end


%post -p <lua>
--(tpg) seems like arg=arg+1 for lua
if arg[2] >= 2 then
	vr = posix.stat("/var/run")
	if vr and vr.type ~= "link" then
		posix.symlink("../run", "/var/run")
	end

	vr = posix.stat("/var/lock")
	if vr and vr.type ~= "link" then
		posix.symlink("../run/lock", "/var/lock")
	end
end

%files -f filelist
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
%endif
%ifarch x86_64
%dir /libx32
%endif
%dir /media
%dir /mnt
%dir /opt
%dir %attr(555,root,root) /proc
%dir %attr(550,root,root) /root
%dir %{_rundir}
%dir %attr(775,root,uucp) /run/lock
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
%if "%{_lib}" == "lib64"
%dir %ghost %{_prefix}/lib/debug/%{_lib}
%endif
%ifarch x86_64
%dir %ghost %{_prefix}/lib/debug/libx32
%endif
%dir %ghost %{_prefix}/lib/debug/%{_prefix}
%dir %ghost %{_prefix}/lib/debug/%{_prefix}/.dwz
%dir %ghost %{_prefix}/lib/debug/sbin
%dir %attr(555,root,root) %{_prefix}/lib/games
%dir %attr(555,root,root) %{_prefix}/lib/sse2
%ifarch x86_64
%dir %attr(555,root,root) %{_prefix}/libx32
%endif
%if "%{_lib}" == "lib64"
%dir %attr(555,root,root) %{_prefix}/%{_lib}
%endif
%if "%{_lib}" == "lib"
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
%if "%{_lib}" == "lib64"
%dir %{_prefix}/local/%{_lib}
%endif
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
%dir %{_prefix}/local/share/man/
%dir %{_prefix}/local/share/man/man[1-9]
%dir %{_prefix}/local/share/man/man[1-9]x
%dir %{_prefix}/local/share/man/mann
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
%dir %{_mandir}/man[013]p
%dir %{_mandir}/man[1-9]
%dir %{_mandir}/man[1-9]x
%dir %{_mandir}/mann
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
%dir %{_var}/lock
%dir %{_var}/mail
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
%dir %{_varrun}
