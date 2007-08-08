#
# TODO:
#	- check all by sby more experienced, espiacially paths, please
#

%define	distname	Th
%define	distversion	2.99
%define	distrelease	"%{distversion} PLD Linux (%{distname})"

Summary:	Nice PLD Linux release file
Summary(pl.UTF-8):	Ładna wersja Linuksa PLD
Name:		issue-nice
Version:	%{distversion}
Release:	3
License:	GPL
Group:		Base
Source0:	issue-make.sh
#images begins at Source10
# Based on mimooh's work
Source10:	issue-nice-tutorial.xcf.gz
# Based on mimooh's work
Source11:	issue-nice-powered.png
# Based on mimooh's work
Source12:	issue-nice-ac.png
# Based on mimooh's work
Source13:	issue-nice-machine.png
# Based on mimooh's work
Source14:	issue-nice-live.png
# With official PLD logo
Source15:	issue-nice-pldlogo.png
BuildRequires:	rpmbuild(macros) >= 1.176
Requires:	fbgetty
Requires:	fbv >= 0.99-2
Requires:	which
Provides:	issue
Provides:	issue-package
Obsoletes:	issue-package
Obsoletes:	redhat-release
Obsoletes:	mandrake-release
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nice (and big) PLD Linux release file.

%description -l pl.UTF-8
Ładny (i duży) plik wersji Linuksa PLD.

%package devel
Summary:	Nice PLD Linux release file toolbox
Summary(pl.UTF-8):	Ładna wersja Linuksa PLD - narzędzia
Group:		Development
Requires:	awk

%description devel
Nice (and big) PLD Linux release file - some tools and samples.

%description devel -l pl.UTF-8
Ładny (i duży) plik wersji Linuksa PLD - parę narzędzi i przykładów.

%define	data	%{_datadir}/%{name}

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{data}}

install %{SOURCE0} $RPM_BUILD_ROOT%{data}
install %{SOURCE10} $RPM_BUILD_ROOT%{data}/tutorial.xcf.gz
install %{SOURCE11} $RPM_BUILD_ROOT%{data}
install %{SOURCE12} $RPM_BUILD_ROOT%{data}
install %{SOURCE13} $RPM_BUILD_ROOT%{data}
install %{SOURCE14} $RPM_BUILD_ROOT%{data}
install %{SOURCE15} $RPM_BUILD_ROOT%{data}

TEMPLATE=$RPM_BUILD_ROOT%{data}/issue.template.fb
TEMPLATE2=$RPM_BUILD_ROOT%{data}/issue.template2.fb
SCRIPT0=$RPM_BUILD_ROOT%{data}/issue-make.sh
SCRIPT1=$RPM_BUILD_ROOT%{data}/fbv-wrapper.sh
SCRIPT2=$RPM_BUILD_ROOT%{data}/uname-p.sh
SCRIPT3=$RPM_BUILD_ROOT%{data}/random.sh
SCRIPT4=$RPM_BUILD_ROOT%{data}/uptime.sh
SCRIPT5=$RPM_BUILD_ROOT%{data}/procnum.sh
SCRIPT6=$RPM_BUILD_ROOT%{data}/cpumhz.sh

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
\e[36mProcessor speed 	.: \e[1m@@cpumhz@@ \e[0m
EOF
cat >$TEMPLATE2<<EOF
\e[0;32m@@procnum@@ \e[0m
\e[0;32m%r \e[0m
\e[0;32m%n \e[0m

\e[0;32m%u \e[0m
\e[0;32m%l \e[0m
\e[0;32m\$RUNLEVEL \e[0m

\e[0;32m@@cpumhz@@ \e[0m
\e[0;32m%t \e[0m
\e[0;32m@@uname-p@@ \e[0m
\e[0;32m%d \e[0m
\e[0;32m%m \e[0m

\e[0;32m@@uptime@@ \e[0m
EOF
# some small scripts (can they be here or move them to seperated files?)

cat >$SCRIPT1<<EOF
#!/bin/sh
#avoid runnig fbv if /dev/fb? is absent
if [ -e /proc/fb ]; then
	if [ -r  \$1 ]; then
		/usr/bin/fbv -c -e -i -a -d 1 \$1
	fi
fi
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
cat >$SCRIPT4<<EOF
#!/bin/sh
#fbgetty includes also "\n" :/
#!/bin/sh
[ -r /proc/uptime ] || exit;
UPTIMEFILE="/proc/uptime";
SEK=\`cat \$UPTIMEFILE|cut -d'.' -f1\`;
MIN=\$(( \$SEK / 60 ));
GOD=\$(( \$MIN / 60 ));
DOB=\$(( \$GOD / 24 ));
GOD2=\$((\$GOD-\$DOB*24));
MIN2=\$((\$MIN-\$GOD*60));

STR1="\${DOB}d";
STR2="\${GOD2}h";
STR3="\${MIN2}m";

if [ \$DOB -eq 0 ];then
	STR1="";
	if [ \$GOD2 -eq 0 ];then
		STR2=""
	fi
fi
echo -n \$STR1\$STR2\$STR3
EOF
cat >$SCRIPT5<<EOF
#!/bin/sh
#fbgetty includes also "\n" :/
echo -n \`ls /proc/|grep ^[0-9]|wc -l\`
EOF
cat >$SCRIPT6<<EOF
#!/bin/sh
#fbgetty includes also "\n" :/
[ -r /proc/cpuinfo ] || exit;
echo -n \`cat /proc/cpuinfo|egrep "clock|cpu MHz"|sed 's/[^0-9]*//'\`
EOF

chmod +x $SCRIPT0

# issue.0.fb
head -n 15 $TEMPLATE|\
	$SCRIPT0 "10 10 10 10 20 22 10 11 11 11 10  8  8  8  8" "47 47 47 47 47 47 47 47 47 47 47 47 47 47 47" %{data}/\
	>$RPM_BUILD_ROOT%{_sysconfdir}/issue.0.fb
echo -n "\`%{data}/fbv-wrapper.sh %{data}/`basename %{SOURCE11}`\`%l " >>$RPM_BUILD_ROOT%{_sysconfdir}/issue.0.fb

# issue.1.fb
head -n 15 $TEMPLATE|\
	$SCRIPT0 "17 17 17 17 22 23 24 24 24 25 25 25 26 27 20" "60 60 60 60 60 60 60 60 60 60 60 60 60 60 60" %{data}/\
	>$RPM_BUILD_ROOT%{_sysconfdir}/issue.1.fb
echo -n "\`%{data}/fbv-wrapper.sh %{data}/`basename %{SOURCE12}`\`%l " >>$RPM_BUILD_ROOT%{_sysconfdir}/issue.1.fb

# issue.2.fb
head -n 15 $TEMPLATE2|\
	$SCRIPT0 "62 20 53 00 21 61 22 00 61 07 58 07 66 00 16" "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0" %{data}/\
	>$RPM_BUILD_ROOT%{_sysconfdir}/issue.2.fb
echo -n "\`%{data}/fbv-wrapper.sh %{data}/`basename %{SOURCE13}`\`%l " >>$RPM_BUILD_ROOT%{_sysconfdir}/issue.2.fb

# issue.3.fb
head -n 15 $TEMPLATE|\
	$SCRIPT0 "29 29 29 29 29 29 29 29 30 29 28 28 26 23 20" "00 00 00 00 45 49 53 57 61 60 59 58 57 56 55" %{data}/\
	>$RPM_BUILD_ROOT%{_sysconfdir}/issue.3.fb
echo -n "\`%{data}/fbv-wrapper.sh %{data}/`basename %{SOURCE14}`\`%l " >>$RPM_BUILD_ROOT%{_sysconfdir}/issue.3.fb

# issue.4.fb
head -n 15 $TEMPLATE|\
	awk 'NR==3 {print "\e[1;31m --==< [\e[0;35m Welcome to \e[1;35mPLD\e[0;35m Linux Distribution\e[1;31m ] >==-- \e[0m";next;} {print;}'|\
	$SCRIPT0 "17 17 17 17 08 09 11 12 12 13 13 13 13 13 13" "00 00 00 00 60 60 60 60 60 60 60 60 60 60 60" %{data}/\
	>$RPM_BUILD_ROOT%{_sysconfdir}/issue.4.fb
echo -n "\`%{data}/fbv-wrapper.sh %{data}/`basename %{SOURCE15}`\`%l " >>$RPM_BUILD_ROOT%{_sysconfdir}/issue.4.fb

# issue, issue.net
head -n 15 $TEMPLATE|\
	$SCRIPT0 "16 16 16 16 35 35 31 32 15 25 22 23 26 25 24" "40 40 40 40 40 40 40 40 40 40 40 40 40 40 40" %{data}/\
	>$RPM_BUILD_ROOT%{_sysconfdir}/issue
echo -n "%l " >> $RPM_BUILD_ROOT%{_sysconfdir}/issue
head -n 11 $RPM_BUILD_ROOT%{_sysconfdir}/issue|sed 's/\\e[^m]*m//g'\
	>$RPM_BUILD_ROOT%{_sysconfdir}/issue.net

echo %{distrelease} > $RPM_BUILD_ROOT%{_sysconfdir}/pld-release

%clean
rm -rf $RPM_BUILD_ROOT

%post
%banner %{name} -e <<EOF
If you want to see an image, remember to adjust your
/etc/inittab line like this:
2:2345:respawn:/usr/sbin/fbgetty --issue=/etc/issue.0.fb tty2
EOF

%files
%defattr(644,root,root,755)
%{_sysconfdir}/pld-release
%config(noreplace) %{_sysconfdir}/issue*
%dir %{data}
%{data}/*.png
%attr(755,root,root) %{data}/fbv-wrapper.sh
%attr(755,root,root) %{data}/uname-p.sh
%attr(755,root,root) %{data}/random.sh
%attr(755,root,root) %{data}/uptime.sh
%attr(755,root,root) %{data}/procnum.sh
%attr(755,root,root) %{data}/cpumhz.sh

%files devel
%defattr(644,root,root,755)
%{data}/*.fb
%{data}/issue-make.sh
%{data}/*.xcf.gz
