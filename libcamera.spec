#
# Conditional build:
%bcond_without	apidocs		# build without API docs

Summary:	A complex camera support library
Name:		libcamera
Version:	0.0.1
Release:	0.1
License:	LGPL v2.1+
Group:		Libraries
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	2abc10f6026717d448f1d95d8cc6ff36
Patch0:		no-docs.patch
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	elfutils-devel
BuildRequires:	glib2-devel
BuildRequires:	gnutls-devel
%{?with_apidocs:BuildRequires:	graphviz}
BuildRequires:	gstreamer-plugins-base-devel >= 1.14
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libunwind-devel
BuildRequires:	lttng-ust-devel
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja
BuildRequires:	openssl-tools
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	python3-PyYAML
BuildRequires:	python3-jinja2
BuildRequires:	python3-ply
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
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
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libcamera library.

%package apidocs
Summary:	API documentation for libcamera library
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libcamera library.

%package ipa-ipu3
Summary:	libcamera IPA plugin for Intel Image Processing Unit 3
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ipa-ipu3
libcamera IPA plugin for Intel Image Processing Unit 3.

%package ipa-raspberrypi
Summary:	libcamera IPA plugin for Raspberry Pi
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ipa-raspberrypi
libcamera IPA plugin for Raspberry Pi.

%package ipa-rkisp1
Summary:	libcamera IPA plugin for Rockchip Image Signal Processor
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ipa-rkisp1
libcamera IPA plugin for Rockchip Image Signal Processor.

%package ipa-vimc
Summary:	libcamera IPA plugin for Virtual Media Controller Driver
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description ipa-vimc
libcamera IPA plugin for Virtual Media Controller Driver.

%package v4l2-compat
Summary:	libcamera compatibility layer providing Video4Linux2 interface
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description v4l2-compat
libcamera compatibility layer providing Video4Linux2 interface.

%package -n gstreamer-libcamera
Summary:	GStreamer plugin for accessing libcamera devices
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gstreamer-plugins-base >= 1.14

%description -n gstreamer-libcamera
GStreamer plugin for accessing libcamera devices.

%prep
%setup -q
%patch0 -p1

%build
ipas="vimc"
pipelines="simple,uvcvideo,vimc"
%ifarch %{ix86} %{x8664} x32
ipas="$ipas,ipu3"
pipelines="$pipelines,ipu3"
%endif
%ifarch %{arm} aarch64
ipas="$ipas,raspberrypi,rkisp1"
pipelines="$pipelines,raspberrypi,rkisp1"
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
%attr(755,root,root) %{_libdir}/libcamera.so.0.0.1
%attr(755,root,root) %{_libdir}/libcamera-base.so.0.0.1
%dir %{_libdir}/libcamera
%dir %{_libexecdir}/libcamera
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
%attr(755,root,root) %{_libdir}/libcamera/ipa_rpi.so
%attr(755,root,root) %{_libexecdir}/libcamera/raspberrypi_ipa_proxy
%{_datadir}/libcamera/ipa/raspberrypi

%files ipa-rkisp1
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamera/ipa_rkisp1.so
%attr(755,root,root) %{_libexecdir}/libcamera/rkisp1_ipa_proxy
%{_datadir}/libcamera/ipa/rkisp1
%endif

%files ipa-vimc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcamera/ipa_vimc.so
%attr(755,root,root) %{_libexecdir}/libcamera/vimc_ipa_proxy
%{_datadir}/libcamera/ipa/vimc

%files v4l2-compat
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/libcamerify
%attr(755,root,root) %{_libdir}/v4l2-compat.so

%files -n gstreamer-libcamera
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gstreamer-1.0/libgstlibcamera.so
