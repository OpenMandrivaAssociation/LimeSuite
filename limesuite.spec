%define major 20
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Name:           LimeSuite
Version:        20.10.0
Release:        1%{?dist}
Summary:        Collection of software supporting LMS7-based hardware
License:        Apache-2.0
Group:          Productivity/Hamradio/Other
URL:            https://myriadrf.org/projects/lime-suite/
#Git-Clone:     https://github.com/myriadrf/LimeSuite.git
Source:         https://github.com/myriadrf/LimeSuite/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gnuplot
BuildRequires:  wxgtku3.0-devel
BuildRequires:  pkgconfig(SoapySDR)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(glu)

%description
Lime Suite is a collection of software supporting several hardware
platforms including the LimeSDR, drivers for the LMS7002M transceiver
RFIC, and other tools for developing with LMS7-based hardware. Lime
Suite enables many SDR applications, such as GQRX for example, to
work with supported hardware through the bundled SoapySDR support
module.

%package -n	%{libname}
Summary:        Library for Lime Suite
Group:          System/Libraries
Requires:       %{name}-udev

%description -n	%{libname}
Lime Suite is a collection of software supporting several hardware
platforms and other tools for developing with LMS7-based hardware.

%package udev
Summary:        Udev rules for LimeSDR
Group:          Hardware/Other

%description udev
Udev rules for Lime Suite

%package -n	%{devname}
Summary:        Development files for libLimeSuite
Group:          Development/Libraries/C and C++
Requires:       %{libname} = %{EVRD}

%description -n	%{devname}
Libraries and header files for developing applications that want to make
use of libLimeSuite.

%package -n soapysdr-module-lms7
Summary:        SoapySDR LMS7 support module
Group:          System/Libraries

%description -n soapysdr-module-lms7
Soapy LMS7 - LimeSDR device support for Soapy SDR.
A Soapy module that supports LimeSDR devices within the Soapy API.

%package doc
Summary:        Documentation for LimeSuite

%description doc
Documentation for LimeSuite

%prep
%autosetup

# HACK: set udev permissions to 666
sed -i 's|MODE="660"|MODE="666"|g' udev-rules/64-limesuite.rules

%build
export CC=gcc
export CXX=g++
%cmake \
  -DBUILD_SHARED_LIBS=ON \
  -DCMAKE_AUTOSET_INSTALL_RPATH=FALSE \
  -DUDEV_RULES_PATH=%{_udevrulesdir} \
%ifarch %{x86_64}
  -DENABLE_SIMD_FLAGS="SSE3" \
%else
  -DENABLE_SIMD_FLAGS="none" \
%endif
  -DLIME_SUITE_EXTVER=release
%make_build

%install
%make_install -C build

%files
%license COPYING
%{_bindir}/LimeUtil
%{_bindir}/LimeSuiteGUI
%{_bindir}/LimeQuickTest
%dir %{_datadir}/Lime
%{_datadir}/Lime/Desktop

%files udev
%{_udevrulesdir}/64-limesuite.rules

%files -n %{libname}
%{_libdir}/libLimeSuite.so.%{major}*

%files -n %{devname}
%{_libdir}/libLimeSuite.so
%{_includedir}/lime
%{_libdir}/pkgconfig/LimeSuite.pc
%{_libdir}/cmake/LimeSuite/

%files -n soapysdr-module-lms7
%dir %{_libdir}/SoapySDR
%dir %{_libdir}/SoapySDR/modules0.7
%{_libdir}/SoapySDR/modules0.7/libLMS7Support.so

%files doc
%doc Changelog.txt README.md
