Name     : docker-cli
Version  : 20.10.17
Release  : 21
URL      : https://github.com/docker/cli/archive/v20.10.17.tar.gz
Source0  : https://github.com/docker/cli/archive/v20.10.17.tar.gz
Summary  : cli used in the Docker CE
Group    : Development/Tools
License  : Apache-2.0
BuildRequires : buildreq-golang
BuildRequires : golang-github-cpuguy83-go-md2man

# don't strip, these are not ordinary object files
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

# Commit ID of the version release
%global docker_src_dir cli-%{version}

%description
Docker-cli is an open source project of the cli used in the Docker CE and Docker EE products.

%prep
%setup -q -n %docker_src_dir

%build
export AUTO_GOPATH=1 DOCKER_BUILDTAGS='exclude_graphdriver_aufs seccomp'
export GOPATH=$HOME/go GO111MODULE="auto"
export DISABLE_WARN_OUTSIDE_CONTAINER=1

mkdir -p $HOME/go/src/github.com/docker/
rm -fr $HOME/go/src/github.com/docker/cli
ln -s /builddir/build/BUILD/%docker_src_dir $HOME/go/src/github.com/docker/cli
pushd $HOME/go/src/github.com/docker/cli
make VERSION=%version BUILDTAGS="exclude_graphdriver_aufs  seccomp"  dynbinary manpages

%install
rm -rf %{buildroot}
# install binary
install -d %{buildroot}/usr/bin
install -p -m 755 build/docker-linux-amd64 %{buildroot}/usr/bin/docker

# install bash completion file.
install -m 0644 -D ./contrib/completion/bash/docker %{buildroot}/usr/share/bash-completion/completions/docker

# install man pages
install -d %{buildroot}/usr/share/man/man1 %{buildroot}/usr/share/man/man5 %{buildroot}/usr/share/man/man8
install ./man/man1/* %{buildroot}/usr/share/man/man1
install ./man/man5/* %{buildroot}/usr/share/man/man5
install ./man/man8/* %{buildroot}/usr/share/man/man8
chmod -x %{buildroot}/usr/share/man/man*/*

%files
%defattr(-,root,root,-)
/usr/bin/docker
/usr/share/bash-completion/completions/docker
/usr/share/man/man*/*
