%define major 0
%define oldlibname %mklibname tree-sitter 0
%define libname %mklibname tree-sitter
%define devname %mklibname tree-sitter -d
%define sdevname %mklibname tree-sitter -d -s
%define cliname tree-sitter_cli

Name: tree-sitter
Version:	0.25.8
Release:	1
Source0: https://github.com/tree-sitter/tree-sitter/archive/v%{version}/%{name}-%{version}.tar.gz
# Source1 is the vendored files for tree-sitter cli. It is generated using cargo-vendor.sh which is
# included in this repository.
Source1: %{name}-%{version}-vendor.tar.xz 
Summary: Parser generator tool and incremental parsing library
URL: https://tree-sitter.github.io/
License: MIT
Group: System/Libraries

%description
Tree-sitter is a parser generator tool and an incremental parsing library.
It can build a concrete syntax tree for a source file and efficiently update
the syntax tree as the source file is edited. Tree-sitter aims to be:

* General enough to parse any programming language
* Fast enough to parse on every keystroke in a text editor
* Robust enough to provide useful results even in the presence of syntax errors
* Dependency-free so that the runtime library (which is written in pure C) can
  be embedded in any application

%package -n %{libname}
Summary: Parser generator tool and incremental parsing library
Group: System/Libraries
%rename %{oldlibname}

%description -n %{libname}
Tree-sitter is a parser generator tool and an incremental parsing library.
It can build a concrete syntax tree for a source file and efficiently update
the syntax tree as the source file is edited. Tree-sitter aims to be:

* General enough to parse any programming language
* Fast enough to parse on every keystroke in a text editor
* Robust enough to provide useful results even in the presence of syntax errors
* Dependency-free so that the runtime library (which is written in pure C) can
  be embedded in any application

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

Tree-sitter is a parser generator tool and an incremental parsing library.
It can build a concrete syntax tree for a source file and efficiently update
the syntax tree as the source file is edited. Tree-sitter aims to be:

* General enough to parse any programming language
* Fast enough to parse on every keystroke in a text editor
* Robust enough to provide useful results even in the presence of syntax errors
* Dependency-free so that the runtime library (which is written in pure C) can
  be embedded in any application

%package -n %{sdevname}
Summary: Static library for %{name}
Group: Development/C
Requires: %{devname} = %{EVRD}

%description -n %{sdevname}
Static library for %{name}.

Tree-sitter is a parser generator tool and an incremental parsing library.
It can build a concrete syntax tree for a source file and efficiently update
the syntax tree as the source file is edited. Tree-sitter aims to be:

* General enough to parse any programming language
* Fast enough to parse on every keystroke in a text editor
* Robust enough to provide useful results even in the presence of syntax errors
* Dependency-free so that the runtime library (which is written in pure C) can
  be embedded in any application

%package -n %{cliname}
Summary: Tree-sitter command line interface 
Group: Development/Other
Requires: nodejs
Requires: clang
BuildRequires: rust
BuildRequires: cargo
%description -n %{cliname}
The Tree-sitter CLI allows you to develop, test, and use Tree-sitter grammars
from the command line

%prep
%autosetup -a1 -p1

%build
%make_build PREFIX=%{_prefix} LIBDIR=%{_libdir} CC="%{__cc}" CFLAGS="%{optflags}"
cd "%{builddir}/%{buildsubdir}/cli"
cargo build --release --frozen

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir} CC="%{__cc}" CFLAGS="%{optflags}"
cd "%{builddir}/%{buildsubdir}/cli"
cargo install --path . --root %{buildroot}/%{_prefix} --frozen --no-track

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files -n %{sdevname}
%{_libdir}/*.a

%files -n %{cliname}
%{_bindir}/%{name}
