%global rc_ver 2
%global baserelease 0.1
%global maj_ver 11
%global min_ver 0
%global patch_ver 0
%global mlir_srcdir llvm-project-%{version}%{?rc_ver:rc%{rc_ver}}

Name: mlir
Version: %{maj_ver}.%{min_ver}.%{patch_ver}
Release: %{baserelease}%{?rc_ver:.rc%{rc_ver}}%{?dist}
Summary: Multi-Level Intermediate Representation Overview

License: ASL 2.0 with exceptions
URL: http://mlir.llvm.org
Source0: https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}%{?rc_ver:-rc%{rc_ver}}/%{mlir_srcdir}.tar.xz
Source1: https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}%{?rc_ver:-rc%{rc_ver}}/%{mlir_srcdir}.tar.xz.sig
Source2: https://prereleases.llvm.org/%{version}/hans-gpg-key.asc

# Support standalone build (MLIR is usually built as part of LLVM)
Patch0: mlir-cmake-standalone.patch

# Unexpected linking error: neither -j1, disabling lto, LD_LIBRARY_PATH, rpath work 
ExcludeArch: armv7hl

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: zlib-devel
BuildRequires: llvm-devel = %{version}
BuildRequires: llvm-test = %{version}

# For origin certification
BuildRequires: gnupg2

%description
The MLIR project is a novel approach to building reusable and extensible
compiler infrastructure. MLIR aims to address software fragmentation,
improve compilation for heterogeneous hardware, significantly reduce
the cost of building domain specific compilers, and aid in connecting
existing compilers together.

%package static
Summary: MLIR static files
Requires: %{name}%{?_isa} = %{version}-%{release}

%description static
MLIR static files.

%package devel
Summary: MLIR development files
Requires: %{name}-static%{?_isa} = %{version}-%{release}

%description devel
MLIR development files.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n %{mlir_srcdir}/%{name} -p2
# remove all but keep mlir
find ../* -maxdepth 0 ! -name '%{name}' -exec rm -rf {} +


%build
%cmake  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DCMAKE_SKIP_RPATH=ON \
        -DLLVM_LINK_LLVM_DYLIB:BOOL=ON \
        -DCMAKE_PREFIX_PATH=%{_libdir}/cmake/llvm/ \
        -DMLIR_INCLUDE_DOCS:BOOL=ON \
        -DMLIR_INCLUDE_TESTS:BOOL=OFF \
        -DMLIR_INCLUDE_INTEGRATION_TESTS:BOOL=OFF \
%if 0%{?__isa_bits} == 64
        -DLLVM_LIBDIR_SUFFIX=64
%else
        -DLLVM_LIBDIR_SUFFIX=
%endif
# build process .exe tools normally use rpath or static linkage
export LD_LIBRARY_PATH=%{_builddir}/%{mlir_srcdir}/%{name}/%{_build}/bin
%cmake_build


%install
%cmake_install

%check
# build process .exe tools normally use rpath or static linkage
%cmake_build --target check-mlir || true

%files
%license LICENSE.TXT
%{_libdir}/libMLIR*.so.%{maj_ver}*
%{_libdir}/libmlir_runner_utils.so.%{maj_ver}*
%{_libdir}/libmlir_c_runner_utils.so.%{maj_ver}*
%{_libdir}/libmlir_c_runner_utils_static.so.%{maj_ver}*

%files static
%{_libdir}/libMLIR*.a

%files devel
%{_libdir}/libMLIR*.so
%{_libdir}/libmlir_runner_utils.so
%{_libdir}/libmlir_c_runner_utils.so
%{_libdir}/libmlir_c_runner_utils_static.so
%{_includedir}/mlir
%{_includedir}/mlir-c
%{_libdir}/cmake/mlir

%changelog
* Wed Aug 12 2020 Cristian Balint <cristian.balint@gmail.com> - 11.0.0-0.1.rc1
- Initial version.

