%define debug_package %{nil}

Name:		filesystem
Version:	4.4
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

mkdir -p %{buildroot}%{_sysconfdir}/{bash_completion.d,default,opt,pki,pm/{config.d,power.d,sleep.d},rwtab.d,statetab.d,security,skel,ssl,sysconfig,xdg/autostart,X11/{applnk,fontpath.d,xinit/{xinitrc,xinput}.d},rwtab.d,statetab.d}

%if "%{_lib}" == "lib64"
mkdir -p %{buildroot}%{_libdir}
%endif
%ifarch %{x86_64}
mkdir -p %{buildroot}{%{_prefix},%{_prefix}/local}/libx32
%endif
mkdir -p %{buildroot}%{_usrsrc}{,/debug}

mkdir -p %{buildroot}%{_prefix}/{etc,lib}
mkdir -p %{buildroot}{%{_bindir},%{_includedir},%{_sbindir},%{_datadir}}
mkdir -p %{buildroot}%{_datadir}/{aclocal,appdata,applications,augeas,backgrounds,color/{icc,cmms,settings},desktop-directories,dict,doc,fonts,empty,fontsmisc,games,icons,idl,mime-info,misc,omf,pixmaps,sounds,themes,xsessions,X11}
mkdir -p %{buildroot}%{_infodir}
# games
mkdir -p %{buildroot}{%{_gamesbindir},%{_gamesdatadir}}
mkdir -p %{buildroot}%{_prefix}/lib/games
%if "%{_lib}" == "lib64"
mkdir -p %{buildroot}%{_libdir}/games
%endif

mkdir -p %{buildroot}%{_libdir}/{gcc-lib,pm-utils/{module.d,power.d,sleep.d}}
mkdir -p %{buildroot}%{_prefix}/lib/gcc-lib
mkdir -p %{buildroot}%{_prefix}/lib/modules
mkdir -p %{buildroot}%{_prefix}/lib/debug/{bin,lib,usr/.dwz,sbin}
%if "%{_lib}" == "lib64"
mkdir -p %{buildroot}%{_prefix}/lib/debug/%{_lib}
%endif
%ifarch %{x86_64}
mkdir -p %{buildroot}%{_prefix}/lib/debug/libx32
%endif

mkdir -p %{buildroot}%{_libexecdir}

mkdir -p %{buildroot}%{_prefix}/local/{bin,doc,etc,games,lib,sbin,src,libexec,include}
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
ln -srf %{buildroot}%{_bindir} %{buildroot}/bin
ln -srf %{buildroot}%{_sbindir} %{buildroot}/sbin
ln -sf bin %{buildroot}%{_prefix}/sbin
ln -srf %{buildroot}%{_prefix}/lib %{buildroot}/lib
%if "%{_lib}" != "lib"
ln -srf %{buildroot}%{_prefix}/%{_lib} %{buildroot}/%{_lib}
%endif
%ifarch %{x86_64}
ln -srf %{buildroot}%{_prefix}/libx32 %{buildroot}/libx32
%endif

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

--# Move a directory out of the way, renaming it to *.rpmmoved
local function movedir(path)
	st = posix.stat(path)
	if st and st.type == "directory" then
		status = os.rename(path, path .. ".rpmmoved")
		if not status then
			suffix = 0
			while not status do
				suffix = suffix + 1
				status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved" .. suffix)
			end
			os.rename(path, path .. ".rpmmoved")
		end
	end
end

--# Merge files in a source directory to a destination directory - unless
--# they already exist in the destination directory. Also, if they exist in
--# both directories and one is a symlink, keep the "good" one. Useful when
--# collecting multiple previous directories (e.g. /bin and /usr/bin) in
--# one...
local function mergedirs(source, dest)
	print("=== mergedirs " .. source .. " -> " .. dest)
	local src=posix.stat(source)
	if not src then
		--# Source doesn't exist
		return
	end
	if src.type ~= "directory" then
		--# Source is already a symlink
		return
	end
	if pairs(posix.dir(source)) == nil then
		--# Nothing in the source directory
		posix.rmdir(source)
		return
	end
	local d=posix.stat(dest)
	if not d then
		--# Destination doesn't exist yet, may be a
		--# fresh install
		posix.mkdir(dest)
	elseif d.type == "link" then
		--# This really shouldn't happen, but let's be safe
		posix.unlink(dest)
		posix.mkdir(dest)
	end
	for i,p in pairs(posix.dir(source)) do
		if(p ~= "." and p ~= "..") then
			local keep=""
			local sts=posix.stat(source .. "/" .. p)
			local std=posix.stat(dest .. "/" .. p)
			if (sts and not std) then
				keep=source
			elseif (std and not sts) then
				--# Can't really happen given it was in posix.dir(),
				--# but let's err on the safe side
				keep=dest
			else
				if (sts.type == "link" and std.type == "link") then
					--# Link in both... Let's see if either one
					--# is dangling first...
					local rls=posix.readlink(source .. "/" .. p)
					local rld=posix.readlink(dest .. "/" .. p)
					local wd=posix.getcwd()
					posix.chdir(source)
					if (not posix.stat(rls)) then
						--# Dangling in source -- keep dest
						keep=dest
					end
					posix.chdir(dest)
					if (not posix.stat(rld)) then
						--# Dangling in dest -- keep source
						keep=source
					end
					posix.chdir(wd)
					if(keep == "") then
						if (string.find(rls, dest) == 1) then
							--# Source is symlink to dest -- keep dest
							keep=dest
						elseif (string.find(rld, source) == 1) then
							--# Dest is symlink to source -- keep source
							keep=source

						else
							--# Last resort, let's keep a symlink that
							--# doesn't go outside of the directory first
							--# and default to keeping dest if we're
							--# still unsure
							if (string.find(rls, "../") ~= 1 and string.find(rls, "/") ~= 1) then
								keep=source
							else
								keep=dest
							end
						end
					end
				elseif (sts.type == "link") then
					--# Link in source, file in dest -- keep the file
					keep=dest
				else
					--# Link in dest, file in source -- keep the file
					keep=source
				end
				if(keep == source) then
					posix.unlink(dest .. "/" .. p)
					os.rename(source .. "/" .. p, dest .. "/" .. p)
				else
					posix.unlink(source .. "/" .. p)
					os.rename(dest .. "/" .. p, source .. "/" .. p)
				end
			end
		end
	end
	--# If anything remains (e.g. /lib/systemd vs /usr/lib/systemd directories)
	--# move it around to be on the safe side
	for i,p in pairs(posix.dir(source)) do
		if(p ~= "." and p ~= "..") then
			os.rename(source .. "/" .. p, dest .. "/" .. p .. ".PRE-USRMERGE")
		end
	end
	posix.rmdir(source)
	--# Just in case rmdir failed (e.g. because of a file left
	--# for whatever reason)
	movedir(source)
end
posix.mkdir("/usr")
posix.mkdir("/usr/bin")
posix.mkdir("/usr/lib")
posix.mkdir("/usr/lib/debug")
posix.mkdir("/usr/%{_lib}")
posix.mkdir("/run")
posix.mkdir("/proc")
posix.mkdir("/sys")
posix.chmod("/proc", 0555)
posix.chmod("/sys", 0555)
posix.mkdir("/var")
posix.symlink("../run", "/var/run")
posix.symlink("../run/lock", "/var/lock")

local st=posix.stat("/bin")
if st and st.type == "directory" then
	mergedirs("/bin", "/usr/bin")
end
local st=posix.stat("/sbin")
if st and st.type == "directory" then
	mergedirs("/sbin", "/usr/bin")
end
local st=posix.stat("/usr/sbin")
if st and st.type == "directory" then
	mergedirs("/usr/sbin", "/usr/bin")
end
local st=posix.stat("/lib")
if st and st.type == "directory" then
	--# /lib/modules should definitely be preferred
	--# over the typically empty /usr/lib/modules...
	posix.rmdir("/usr/lib/modules")
	--# If it wasn't empty, move it aside
	os.rename("/usr/lib/modules", "/usr/lib/modules.PRE-USRMERGE")
	os.rename("/lib/modules", "/usr/lib/modules")
	mergedirs("/lib", "/usr/lib")
end
%if "%{_lib}" != "lib"
local st=posix.stat("/%{_lib}")
if st and st.type == "directory" then
	mergedirs("/%{_lib}", "/usr/%{_lib}")
end
%endif
%ifarch %{x86_64}
local st=posix.stat("/libx32")
if st and st.type == "directory" then
	mergedirs("/libx32", "/usr/libx32")
end
%endif

posix.symlink("usr/bin", "/bin")
posix.symlink("usr/bin", "/sbin")
posix.symlink("bin", "/usr/sbin")
posix.symlink("usr/lib", "/lib")
%if "%{_lib}" != "lib"
posix.symlink("usr/%{_lib}", "/%{_lib}")
%endif
%ifarch %{x86_64}
posix.symlink("usr/libx32", "/libx32")
%endif
print("Lua pretrans script reached end")
return 0

%files -f filelist
%defattr(0755,root,root,-)
%dir %attr(555,root,root) /
%attr(555,root,root) /boot
%dir /dev
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
%dir /home
%dir /initrd
%dir /media
%dir /mnt
%dir /opt
%ghost %attr(555,root,root) /proc
%dir %attr(550,root,root) /root
%dir %{_rundir}
%dir %attr(775,root,uucp) /run/lock
%dir /srv
%ghost %attr(555,root,root) /sys
%dir %attr(1777,root,root) /tmp
%dir %{_prefix}
%dir %attr(555,root,root) %{_bindir}
%dir %{_gamesbindir}
%dir %{_includedir}
%dir %attr(555,root,root) %{_prefix}/lib
%dir %{_prefix}/lib/debug
%dir %{_prefix}/lib/debug/bin
%dir %{_prefix}/lib/debug/lib
%dir %{_prefix}/lib/modules
%if "%{_lib}" == "lib64"
%dir %{_prefix}/lib/debug/%{_lib}
%endif
%ifarch %{x86_64}
%dir %{_prefix}/lib/debug/libx32
%endif
%dir %{_prefix}/lib/debug/%{_prefix}
%dir %{_prefix}/lib/debug/%{_prefix}/.dwz
%dir %{_prefix}/lib/debug/sbin
%dir %attr(555,root,root) %{_prefix}/lib/games
%ifarch %{x86_64}
%dir %attr(555,root,root) %{_prefix}/libx32
%endif
%if "%{_lib}" != "lib"
%dir %attr(555,root,root) %{_prefix}/%{_lib}
%endif
%if "%{_lib}" == "lib"
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
%if "%{_lib}" != "lib"
%dir %{_prefix}/local/%{_lib}
%endif
%ifarch %{x86_64}
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
%{_prefix}/sbin
/sbin
/bin
/lib
%if "%{_lib}" != "lib"
/%{_lib}
%endif
%ifarch %{x86_64}
/libx32
%endif
