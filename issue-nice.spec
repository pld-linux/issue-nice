#
# TODO:
#	- check all by sby more experienced, espiacially paths, please
#

%define	distname	Ra
%define	distversion	1.0

Summary:	Nice PLD Linux release file
Summary(pl):	£adna wersja Linuksa PLD
Name:		issue-nice
Version:	%{distversion}
Release:	1
License:	GPL
Group:		Base
Source0:	issue-make.sh
# Based on mimooh's work
Source1:	stork0.png
# Based on mimooh's work
Source2:	stork1.png
Buildarch:	noarch
BuildRequires:	awk
BuildRequires:	sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	redhat-release
Obsoletes:	mandrake-release
Obsoletes:	issue
Obsoletes:	issue-alpha
Obsoletes:	issue-fancy
Obsoletes:	issue-logo
Obsoletes:	issue-pure
Requires:	which
Requires:	fbv >= 0.99-2
Requires:	fbgetty

%define	distrelease	"%{distversion} PLD Linux (%{distname})"

%description
Nice (and big) PLD Linux release file.

%description -l pl
£adny (i du¿y) plik wersji Linuksa PLD.

%package devel
Summary:	Nice PLD Linux release file toolbox
Summary(pl):	£adna wersja Linuksa PLD - narzêdzia
Group:		Development
Requires:	awk

%description devel
Nice (and big) PLD Linux release file - some tools.

%description devel -l pl
£adny (i du¿y) plik wersji Linuksa PLD - pare narzêdzi.

%define	data	%{_libdir}/%{name}

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{data}

install %{SOURCE0} $RPM_BUILD_ROOT%{data}
install %{SOURCE1} $RPM_BUILD_ROOT%{data}
install %{SOURCE2} $RPM_BUILD_ROOT%{data}

TEMPLATE=$RPM_BUILD_ROOT%{data}/issue.template.fb
SCRIPT0=$RPM_BUILD_ROOT%{data}/issue-make.sh
SCRIPT1=$RPM_BUILD_ROOT%{data}/fbv-wrapper.sh
SCRIPT2=$RPM_BUILD_ROOT%{data}/uname-p.sh
SCRIPT3=$RPM_BUILD_ROOT%{data}/random.sh

# warning! there are <space><tab> - they must be
cat >$TEMPLATE<<EOF
\e[1;31m        ___________________________________\e[0m
\e[1;31m      /\'                                   \\\`\\\\\\e[0m
\e[1;33m --==\e[1;31m< \e[1;37m[\e[1;34m Welcome to \e[1;32mPLD\e[0;32m Linux Distribution\e[1;31m \e[1;37m]\e[1;31m >\e[1;33m==-- \e[0m
\e[1;31m      \\\\_____________________________________/\e[0m
\e[36mDate 	.: \e[1m%d \e[0m
\e[36mTime 	.: \e[1m%t \e[0m
\e[36mHostname 	.: \e[1m%n \e[0m
\e[36mConsole 	.: \e[1m%l \e[0m
\e[36mNumber of user connected 	.: \e[1m%u \e[0m
\e[36mKernel version 	.: \e[1m%r \e[0m
\e[36mHost Architecture 	.: \e[1m%m \e[0m
\e[36mCurrent runlevel 	.: \e[1m\$RUNLEVEL \e[0m
\e[36mTerminal type 	.: \e[1m\$TERM \e[0m
\e[36mProcessor type 	.: \e[1m@@uname-p@@ \e[0m
\e[36mRandom number 	.: \e[1m@@random@@ \e[0m
EOF

# some small scripts (can they be here or move them to seperated files?)

cat >$SCRIPT1<<EOF
#!/bin/sh
#avoid runnig fbv if /dev/fb? is absent
#help: how to recognize it better?
grep "^vesafb: framebuffer at" /var/log/dmesg >/dev/null 2>&1 && \\
	[ -x `which fbv 2>/dev/null` -a -f \$1 ] && \\
		`which fbv 2>/dev/null` -c -e -i -a -d 1 \$1
EOF

cat >$SCRIPT2<<EOF
#!/bin/sh
#fbgetty includes also "\n" :/
[ -x /bin/uname ] && \\
	echo -n \`/bin/uname -p\`
EOF

cat >$SCRIPT3<<EOF
#!/bin/sh
#fbgetty includes also "\n" :/
echo -n \$RANDOM
EOF

chmod +x $SCRIPT0

echo %{distrelease} > $RPM_BUILD_ROOT%{_sysconfdir}/pld-release

# issue.0.fb
head -15 $TEMPLATE|\
	$SCRIPT0 "10 10 10 10 20 22 10 11 11 11 10  8  8  8  8" "47 47 47 47 47 47 47 47 47 47 47 47 47 47 47" %{data}/\
	>$RPM_BUILD_ROOT%{_sysconfdir}/issue.0.fb
echo -n "\`%{data}/fbv-wrapper.sh %{data}/`basename %{SOURCE1}`\`%l " >>$RPM_BUILD_ROOT%{_sysconfdir}/issue.0.fb

# issue.1.fb
head -15 $TEMPLATE|\
	$SCRIPT0 "17 17 17 17 22 23 24 24 24 25 25 25 26 27 20" "60 60 60 60 60 60 60 60 60 60 60 60 60 60 60" %{data}/\
	>$RPM_BUILD_ROOT%{_sysconfdir}/issue.1.fb
echo -n "\`%{data}/fbv-wrapper.sh %{data}/`basename %{SOURCE2}`\`%l " >>$RPM_BUILD_ROOT%{_sysconfdir}/issue.1.fb

# issue, issue.net
head -15 $TEMPLATE|\
	$SCRIPT0 "16 16 16 15 35 35 31 32 15 25 22 23 26 25 26" "40 40 40 40 40 40 40 40 40 40 40 40 40 40 40" %{data}/\
	>$RPM_BUILD_ROOT%{_sysconfdir}/issue
echo -n "%l " >> $RPM_BUILD_ROOT%{_sysconfdir}/issue
head -11 $RPM_BUILD_ROOT%{_sysconfdir}/issue|sed 's/\\e[^m]*m//g'\
	>$RPM_BUILD_ROOT%{_sysconfdir}/issue.net


%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "If you want to see an image, remember to adjust your /etc/inittab line like this:"
echo "2:2345:respawn:/usr/sbin/fbgetty --issue=/etc/issue.0.fb tty2"

%files
%defattr(644,root,root,755)
%{_sysconfdir}/pld-release
%config(noreplace) %{_sysconfdir}/issue*
%{data}/*.png
%attr(755,root,root) %{data}/fbv-wrapper.sh
%attr(755,root,root) %{data}/uname-p.sh
%attr(755,root,root) %{data}/random.sh

%files devel
%defattr(644,root,root,755)
%{data}/issue.template.fb
%{data}/issue-make.sh
