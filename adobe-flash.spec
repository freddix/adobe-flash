Summary:	Adobe Flash
Name:		adobe-flash
Version:	11.2.202.336
Release:	1
License:	Oth
Group:		X11/Applications
Source0:	http://fpdownload.macromedia.com/get/flashplayer/pdc/%{version}/install_flash_player_11_linux.i386.tar.gz
# Source0-md5:	bd7f77dfd0a03bbbd5d124febb8c83d5
Source1:	http://fpdownload.macromedia.com/get/flashplayer/pdc/%{version}/install_flash_player_11_linux.x86_64.tar.gz
# Source1-md5:	63d0a9b141f5a52cf9c7a71bd4f785f2
Source2:	http://www.adobe.com/products/eulas/pdfs/PlatformClients_PC_WWEULA_Combined_20100108_1657.pdf
# Source2-md5:	94ca2aecb409abfe36494d1a7ec7591d
URL:		http://www.adobe.com/products/flashplayer/
%ifarch %{ix86}
Requires:       libasound.so.2
Requires:       libcurl.so.4
%else
Requires:       libasound.so.2()(64bit)
Requires:       libcurl.so.4()(64bit)
%endif
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/adobe
%define		_enable_debug_packages	0

%description
Adobe® Flash® Player is a cross-platform browser-based application
runtime that delivers uncompromised viewing of expressive
applications, content, and videos across screens and browsers.

%prep
%ifarch %{ix86}
%setup -q -T -c -b 0
%else
%setup -q -T -c -b 1
%endif

cp %{SOURCE2} .

%build
s=$(echo 'LNX %{version}' | tr . ,)
v=$(strings libflashplayer.so | grep '^LNX ')
if [ "$v" != "$s" ]; then
	: wrong version
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_libdir}/browser-plugins,%{_iconsdir}}

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/mms.cfg
# http://www.adobe.com/cfusion/knowledgebase/index.cfm?id=16701594
AutoUpdateDisable=1
AutoUpdateInterval=0
EOF

install *.so $RPM_BUILD_ROOT%{_libdir}/browser-plugins
install -D usr/bin/flash-player-properties $RPM_BUILD_ROOT%{_bindir}/flash-player-properties
install -D usr/share/applications/flash-player-properties.desktop \
	$RPM_BUILD_ROOT%{_desktopdir}/flash-player-properties.desktop
cp -a usr/share/icons/* $RPM_BUILD_ROOT%{_iconsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc PlatformClients_PC_WWEULA_Combined_20100108_1657.pdf
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms.cfg
%attr(755,root,root) %{_bindir}/flash-player-properties
%attr(755,root,root) %{_libdir}/browser-plugins/*.so
%{_desktopdir}/flash-player-properties.desktop
%{_iconsdir}/hicolor/*/apps/*.png

