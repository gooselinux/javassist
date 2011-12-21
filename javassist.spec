%global ext_ver .GA
%global         with_maven 0

Name:           javassist
Version:        3.9.0
Release:        6%{?dist}
Summary:        The Java Programming Assistant provides simple Java bytecode manipulation
Group:          Development/Libraries
License:        MPLv1.1 or LGPLv2+
URL:            http://www.csg.is.titech.ac.jp/~chiba/javassist/
Source0:        http://downloads.sourceforge.net/jboss/%{name}3.9.GA.zip
Patch0:         javassist-buildfile-nosource1.4-nosrcjar.patch
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     java-devel >= 1:1.6.0
BuildRequires:     jpackage-utils

%if %{with_maven}
BuildRequires:     maven2
BuildRequires:     maven2-plugin-compiler
BuildRequires:     maven2-plugin-install
BuildRequires:     maven2-plugin-jar
BuildRequires:     maven2-plugin-javadoc
BuildRequires:     maven2-plugin-resources
BuildRequires:     maven2-plugin-surefire
BuildRequires:     maven2-plugin-source
BuildRequires:     maven2-plugin-antrun
%else
BuildRequires:     ant
%endif

Requires:          java >= 1:1.6.0
Requires:          jpackage-utils

Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
Javassist enables Java programs to define a new class at runtime and to
modify a class file when the JVM loads it. Unlike other similar
bytecode editors, Javassist provides two levels of API: source level
and bytecode level. If the users use the source-level API, they can
edit a class file without knowledge of the specifications of the Java
bytecode. The whole API is designed with only the vocabulary of the
Java language. You can even specify inserted bytecode in the form of
source text; Javassist compiles it on the fly. On the other hand, the
bytecode-level API allows the users to directly edit a class file as
other editors.


%package javadoc
Summary:           Javadocs for javassist
Group:             Documentation
Requires:          %{name} = %{version}-%{release}
Requires:          jpackage-utils

%description javadoc
javassist development documentation.


%prep
%setup -q # -n %{name}-%{version}
%patch0 -p0

find . -name \*.jar -type f -delete


%build
%if %{with_maven}
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
-Dmaven.repo.local=$MAVEN_REPO_LOCAL \
install javadoc:javadoc
%else
ant jar javadocs
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
%if %{with_maven}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap %{name} %{name} %{version}%{ext_ver} JPP %{name}
%endif

# jar
install -d $RPM_BUILD_ROOT%{_javadir}
%if %{with_maven}
install -m644 target/%{name}-%{version}%{ext_ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}%{ext_ver}.jar
%else
install -m644 %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}%{ext_ver}.jar
%endif
ln -s %{name}-%{version}%{ext_ver}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%if %{with_maven}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%else
cp -rp html/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%endif
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}


%clean
rm -rf $RPM_BUILD_ROOT

%if %{with_maven}
%post
%update_maven_depmap

%postun
%update_maven_depmap
%endif

%files
%defattr(-,root,root,-)
%doc License.html
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}%{ext_ver}.jar
%if %{with_maven}
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%endif


%files javadoc
%defattr(-,root,root,-)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
%{_javadocdir}/%{name}-%{version}/*


%changelog
* Tue Dec 08 2009 Andrew Overholt <overholt@redhat.com> 3.9.0-6
- Add ability to build with ant and not maven
- Remove maven2-plugin-release BR (part of maven2 now)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 John5342 <john5342 at, fedoraproject.org> - 3.9.0-3
- Correct group id for maven depmap

* Mon Jan 26 2009 John5342 <john5342 at, fedoraproject.org> - 3.9.0-2
- Build using maven and install maven stuff (fixes bug 480428)

* Tue Dec 16 2008 Sandro Mathys <red at fedoraproject.org> - 3.9.0-1
- initial build
