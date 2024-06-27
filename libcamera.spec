#
# Conditional build:
%bcond_without	apidocs		# Sphinx/doxygen based API documentation

Summary:	A complex camera support library
Summary(pl.UTF-8):	Biblioteka obsługi złożonych kamer
Name:		libcamera
Version:	0.3.0
Release:	0.1
License:	LGPL v2.1+
Group:		Libraries
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	b2c84de368c8754e05f6572b0286f993
Patch0:		no-docs.patch
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	elfutils-devel
BuildRequires:	glib2-devel
BuildRequires:	gnutls-devel
%{?with_apidocs:BuildRequires:	graphviz}
BuildRequires:	gstreamer-plugins-base-devel >= 1.14
%ifarch %{armv6}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	libunwind-devel
BuildRequires:	lttng-ust-devel
BuildRequires:	meson >= 0.60
BuildRequires:	ninja >= 1.5
BuildRequires:	openssl-tools
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-PyYAML
BuildRequires:	python3-jinja2
BuildRequires:	python3-ply
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.007
%{?with_apidocs:BuildRequires:	sphinx-pdg}
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	xz
BuildRequires:	yaml-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cameras are complex devices that need heavy hardware image processing
operations. Control of the processing is based on advanced algorithms
that must run on a programmable processor. This has traditionally been
implemented in a dedicated MCU in the camera, but in embedded devices
algorithms have been moved to the main CPU to save cost. Blurring the
boundary between camera devices and Linux often left the user with no
other option than a vendor-specific closed-source solution.

To address this problem the Linux media community has very recently
started collaboration with the industry to develop a camera stack that
will be open-source-friendly while still protecting vendor core IP.
libcamera was born out of that collaboration and will offer modern
camera support to Linux-based systems, including traditional Linux
distributions, ChromeOS and Android.

%package devel
Summary:	Header files for libcamera library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libcamera
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libcamera library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libcamera.

%package apidocs
Summary:	API documentation for libcamera library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libcamera
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libcamera library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libcamera.

%package ipa-ipu3
Summary:	libcamera IPA plugin for Intel Image Processing Unit 3
Summary(pl.UTF-8):	Wtyczka IPA libcamera do Intel Image Processing Unit 3
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ipa-ipu3
libcamera IPA plugin for Intel Image Processing Unit 3.

%description ipa-ipu3 -l pl.UTF-8
Wtyczka IPA libcamera do Intel Image Processing Unit 3.

%package ipa-raspberrypi
Summary:	libcamera IPA plugin for Raspberry Pi
Summary(pl.UTF-8):	Wtyczka IPA libcamera do Raspberry Pi
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ipa-raspberrypi
libcamera IPA plugin for Raspberry Pi.

%description ipa-raspberrypi -l pl.UTF-8
Wtyczka IPA libcamera do Raspberry Pi.

%package ipa-rkisp1
Summary:	libcamera IPA plugin for Rockchip Image Signal Processor
Summary(pl.UTF-8):	Wtyczka IPA libcamera do Rockchip Image Signal Processor
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ipa-rkisp1
libcamera IPA plugin for Rockchip Image Signal Processor.

%description ipa-rkisp1 -l pl.UTF-8
Wtyczka IPA libcamera do Rockchip Image Signal Processor.

%package ipa-soft-simple
Summary:	Simple software libcamera IPA plugin
Summary(pl.UTF-8):	Prosta programowa wtyczka IPA libcamera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ipa-soft-simple
Simple software libcamera IPA plugin.

%description ipa-soft-simple -l pl.UTF-8
Prosta programowa wtyczka IPA libcamera.

%package ipa-vimc
Summary:	libcamera IPA plugin for Virtual Media Controller Driver
Summary(pl.UTF-8):	Wtyczka IPA libcamera do sterownika Virtual Media Controller Driver
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ipa-vimc
libcamera IPA plugin for Virtual Media Controller Driver.

%description ipa-vimc -l pl.UTF-8
Wtyczka IPA libcamera do sterownika Virtual Media Controller Driver.

%package v4l2-compat
Summary:	libcamera compatibility layer providing Video4Linux2 interface
Summary(pl.UTF-8):	Warstwa zgodności libcamera udostępniająca interfejs Video4Linux2
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description v4l2-compat
libcamera compatibility layer providing Video4Linux2 interface.

%description v4l2-compat -l pl.UTF-8
Warstwa zgodności libcamera udostępniająca interfejs Video4Linux2.

%package -n gstreamer-libcamera
Summary:	GStreamer plugin for accessing libcamera devices
Summary(pl.UTF-8):	Wtyczka GStreamera do dostępu do urządzeń libcamera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gstreamer-plugins-base >= 1.14

%description -n gstreamer-libcamera
GStreamer plugin for accessing libcamera devices.

%description -n gstreamer-libcamera -l pl.UTF-8
Wtyczka GStreamera do dostępu do urządzeń libcamera.

%prep
%setup -q
%patch0 -p1

%build
ipas="simple,vimc"
pipelines="simple,uvcvideo,vimc"
%ifarch %{ix86} %{x8664} x32
ipas="$ipas,ipu3"
pipelines="$pipelines,ipu3"
%endif
%ifarch %{arm} aarch64
ipas="$ipas,rpi/vc4,rkisp1"
pipelines="$pipelines,imx8-isi,mali-c55,rpi/vc4,rkisp1"
%endif

%meson build \
	-Dcam=disabled \
	-Ddocumentation=%{__enabled_disabled apidocs} \
	-Dgstreamer=enabled \
	-Dipas=$ipas \
	-Dlc-compliance=disabled \
	-Dpipelines=$pipelines \
	-Dqcam=disabled \
	-Dv4l2=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%{?with_apidocs:%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_libdir}/libcamera.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcamera.so.0.3
%attr(755,root,root) %{_libdir}/libcamera-base.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcamera-base.so.0.3
%dir %{_libdir}/libcamera
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/libcamera
%endif
%dir %{_datadir}/libcamera
%dir %{_datadir}/libcamera/ipa

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamera.so
%attr(755,root,root) %{_libdir}/libcamera-base.so
%{_includedir}/libcamera
%{_pkgconfigdir}/libcamera.pc
%{_pkgconfigdir}/libcamera-base.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/Documentation/api-html build/Documentation/html
%endif

%ifarch %{ix86} %{x8664} x32
%files ipa-ipu3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamera/ipa_ipu3.so
%attr(755,root,root) %{_libexecdir}/libcamera/ipu3_ipa_proxy
%{_datadir}/libcamera/ipa/ipu3
%endif

%ifarch %{arm} aarch64
%files ipa-raspberrypi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamera/ipa_rpi_vc4.so
%attr(755,root,root) %{_libexecdir}/libcamera/raspberrypi_ipa_proxy
%{_datadir}/libcamera/ipa/rpi

%files ipa-rkisp1
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamera/ipa_rkisp1.so
%attr(755,root,root) %{_libexecdir}/libcamera/rkisp1_ipa_proxy
%{_datadir}/libcamera/ipa/rkisp1
%endif

%files ipa-soft-simple
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamera/ipa_soft_simple.so
%attr(755,root,root) %{_libexecdir}/libcamera/soft_ipa_proxy
%{_datadir}/libcamera/ipa/simple

%files ipa-vimc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamera/ipa_vimc.so
%attr(755,root,root) %{_libexecdir}/libcamera/vimc_ipa_proxy
%{_datadir}/libcamera/ipa/vimc

%files v4l2-compat
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/libcamerify
%attr(755,root,root) %{_libexecdir}/libcamera/v4l2-compat.so

%files -n gstreamer-libcamera
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstlibcamera.so
