%global rc_ver 3
%global baserelease 4
%global maj_ver 12
%global min_ver 0
%global patch_ver 0
%global mlir_srcdir llvm-project-%{version}%{?rc_ver:rc%{rc_ver}}.src

Name: mlir
Version: %{maj_ver}.%{min_ver}.%{patch_ver}
Release: %{?rc_ver:0.}%{baserelease}%{?rc_ver:.rc%{rc_ver}}%{?dist}
Summary: Multi-Level Intermediate Representation Overview

License: ASL 2.0 with exceptions
URL: http://mlir.llvm.org
Source0: https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}%{?rc_ver:-rc%{rc_ver}}/%{mlir_srcdir}.tar.xz
Source1: https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}%{?rc_ver:-rc%{rc_ver}}/%{mlir_srcdir}.tar.xz.sig
Source2: tstellar-gpg-key.asc

Patch0: 0001-PATCH-mlir-Support-building-MLIR-standalone.patch
Patch1: 0002-PATCH-mlir-Fix-building-unittests-in-in-tree-build.patch

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
        -DLLVM_BUILD_UTILS:BOOL=ON \
        -DMLIR_INCLUDE_DOCS:BOOL=ON \
        -DMLIR_INCLUDE_TESTS:BOOL=OFF \
        -DMLIR_INCLUDE_INTEGRATION_TESTS:BOOL=OFF \
        -DBUILD_SHARED_LIBS=OFF \
%if 0%{?__isa_bits} == 64
        -DLLVM_LIBDIR_SUFFIX=64
%else
        -DLLVM_LIBDIR_SUFFIX=
%endif
# build process .exe tools normally use rpath or static linkage
export LD_LIBRARY_PATH=%{_builddir}/%{mlir_srcdir}/%{name}/%{_build}/%{_lib}
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
%{_libdir}/libmlir_async_runtime.so.%{maj_ver}*

%files static
%{_libdir}/libMLIR*.a
%{_libdir}/libmlir_c_runner_utils_static.a

%files devel
%{_bindir}/mlir-tblgen
%{_libdir}/libMLIR*.so
%{_libdir}/libmlir_runner_utils.so
%{_libdir}/libmlir_c_runner_utils.so
%{_libdir}//libmlir_async_runtime.so
%{_includedir}/mlir
%{_includedir}/mlir-c
%{_libdir}/cmake/mlir

%changelog
* Thu Mar 11 2021 sguelton@redhat.com - 12.0.0-0.4.rc3
- LLVM 12.0.0 rc3

* Wed Mar 10 2021 sguelton@redhat.com - 12.0.0-0.3.rc2
- rebuilt

* Wed Feb 24 2021 sguelton@redhat.com - 12.0.0-0.2.rc2
- llvm 12.0.0-rc2 release

* Thu Feb 18 2021 sguelton@redhat.com - 12.0.0-0.1.rc1
- llvm 12.0.0-rc1 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.0-0.3.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Serge Guelton - 11.1.0-0.2.rc2
- llvm 11.1.0-rc2 release

* Thu Jan 14 2021 Serge Guelton - 11.1.0-0.1.rc1
- 11.1.0-rc1 release

* Wed Jan 06 2021 Serge Guelton - 11.0.1-3
- LLVM 11.0.1 final

* Tue Dec 22 2020 sguelton@redhat.com - 11.0.1-2.rc2
- llvm 11.0.1-rc2

* Tue Dec 01 2020 sguelton@redhat.com - 11.0.1-1.rc1
- llvm 11.0.1-rc1

* Thu Oct 15 2020 sguelton@redhat.com - 11.0.0-1
- Fix NVR

* Mon Oct 12 2020 sguelton@redhat.com - 11.0.0-0.6
- llvm 11.0.0 - final release

* Thu Oct 08 2020 sguelton@redhat.com - 11.0.0-0.5.rc6
- 11.0.0-rc6

* Fri Oct 02 2020 sguelton@redhat.com - 11.0.0-0.4.rc5
- 11.0.0-rc5 Release

* Sun Sep 27 2020 sguelton@redhat.com - 11.0.0-0.3.rc3
- Fix NVR

* Thu Sep 24 2020 sguelton@redhat.com - 11.0.0-0.1.rc3
- 11.0.0-rc3 Release

* Wed Sep 02 2020 sguelton@redhat.com - 11.0.0-0.2.rc2
- Package mlir-tblgen

* Wed Aug 12 2020 Cristian Balint <cristian.balint@gmail.com> - 11.0.0-0.1.rc1
- Initial version.

