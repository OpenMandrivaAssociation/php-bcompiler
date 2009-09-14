%define modname bcompiler
%define soname %{modname}.so
%define inifile A88_%{modname}.ini

Summary:	A bytecode compiler for PHP
Name:		php-%{modname}
Version:	0.8
Release:	%mkrel 8
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/bcompiler
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	bzip2-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
bcompiler enables you to encode your scripts in phpbytecode, enabling you to
protect the source code. bcompiler could be used in the following situations:

 - to create a exe file of a PHP-GTK application (in conjunction with other
   software)
 - to create closed source libraries
 - to provide clients with time expired software (prior to payment)
 - to deliver close source applications
 - for use on embedded systems, where disk space is a priority.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv -f ../package*.xml .

# lib64 fixes
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

# fix attribs
chmod 644 examples/*.php CREDITS README TODO

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS README TODO examples/*.php
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

