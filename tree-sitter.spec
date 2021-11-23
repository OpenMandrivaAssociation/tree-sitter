%define major 0
%define libname %mklibname tree-sitter %{major}
%define devname %mklibname tree-sitter -d
%define sdevname %mklibname tree-sitter -d -s

Name: tree-sitter
Version:	0.20.1
Release:	1
Source0: https://github.com/tree-sitter/tree-sitter/archive/refs/tags/v%{version}.tar.gz
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

%prep
%autosetup -p1

%build
%make_build PREFIX=%{_prefix} LIBDIR=%{_libdir} CFLAGS="%{optflags}"

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir} CFLAGS="%{optflags}"

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files -n %{sdevname}
%{_libdir}/*.a
