#!/usr/bin/env bash

# NOTE Update the Version: parameter in the spec file and save it before
# NOTE running this script.
#
# This script will download and vendor both the python-proton-vpn-local-agent/Cargo.toml
# and the local_agent_rs/Cargo.toml files in order that everything both crates
# require is vendorered for the build, this is the mess that is cargo/rust.
#
# Upload both the local-agent-rs.tar.gz source tarball and the
# local-agent-rs-%{version}-vendor.tar.xz to the abf file store.

DownloadSource () {
	local FILENAME=$( basename $1 )
	if  [ ! -f "./${FILENAME}"  ]; then
		printf "${FILENAME} does not exist in package directory. \nAttempting to download..\n"
		if curl -o /dev/null -sfL -r 0-0 "${1}"; then
			printf "File exists on remote, downloading..\n"
			curl -o "${FILENAME}" -L $1
		else
			printf "URI/Archive: $FILENAME does not exist on remote server. \nCheck package Name or oname define in spec file.\n\n"
			exit 0
		fi
else
	printf "${FILENAME} exists in package directory, skipping download attempt.\n"
fi
}
#Get the package source URL from the spec file
PACKAGE_SRC=$(awk -F " " '/^Source:|^Source0:/ {print $2}' *.spec)
# Get version and defined oname from spec file
VERSION=$(awk -F ":" '/Version/ {print $2}' tree-sitter.spec)
# Remove leading and trailing whitespace from VERSION
VERSION="${VERSION#"${VERSION%%[![:space:]]*}"}"
VERSION="${VERSION%"${VERSION##*[![:space:]]}"}"

PACKAGE_NAME=$(awk -F ":" '/Name/ {print $2}' *.spec)
# Remove leading and trailing whitespace from PACKAGE
PACKAGE_NAME="${PACKAGE_NAME#"${PACKAGE_NAME%%[![:space:]]*}"}"
PACKAGE_NAME="${PACKAGE_NAME%"${PACKAGE_NAME##*[![:space:]]}"}"

PACKAGE_SRC=${PACKAGE_SRC/[%]\{version\}/"${VERSION}"}
PACKAGE_SRC=${PACKAGE_SRC/[%]\{version\}/"${VERSION}"}
PACKAGE_SRC=${PACKAGE_SRC/[%]\{name\}/"${PACKAGE_NAME}"}

echo "Found Version: ${VERSION}"
echo "Package Source: ${PACKAGE_SRC}"
echo "Package Name: $PACKAGE_NAME"

DownloadSource ${PACKAGE_SRC}

echo "Extracting source from ${PACKAGE_SRC/*\//}"
tar -xf ${PACKAGE_SRC/*\//}
cd ./${PACKAGE_NAME}-${VERSION}/cli

printf "Creating vendor archive: $PACKAGE_NAME-$VERSION-vendor.tar.xz \n"
# vendor the crate and its dependency crate
mkdir .cargo
cargo vendor  > .cargo/config.toml
cd ..
# archive the vendor dir into the spec file root
tar -cJf ../$PACKAGE_NAME-$VERSION-vendor.tar.xz ./cli/vendor ./cli/.cargo/config.toml
printf "Completed creating archive: $PACKAGE_NAME-$VERSION-vendor.tar.xz \n"
# remove the vendor folder and contents generated during vendoring
# if you need to see what is vendored look inside the archive.
rm -rf ./cli/vendor
rm -rf ./cli/.cargo
