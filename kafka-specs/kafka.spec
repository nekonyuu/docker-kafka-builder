%define kafka_name kafka
%define kafka_branch 0.8
%define kafka_version 0.8.1.1
%define release_version 2
%define kafka_home /opt/%{kafka_name}-%{kafka_version}
%define etc_kafka /etc/%{name}
%define config_kafka %{etc_kafka}/config
%define kafka_user kafka
%define kafka_group kafka

Name: %{kafka_name}
Version: %{kafka_version}
Release: %{release_version}%{?dist}
Summary: Apache Kafka is a high-throughput distributed publish-subscribe messaging system.
License: Apache 2.0
URL: http://incubator.apache.org/kafka/
Group: Development/Libraries
Source0: http://mirrors.ircam.fr/pub/apache/kafka/%{kafka_version}/%{kafka_name}_2.10-%{kafka_version}.tgz
Source1: kafka-server
Source2: kafka
Source3: kafka.nofiles.conf
Patch0: kafka-env-mem-fix.patch 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Provides: kafka
Requires: java
Packager: Jonathan "nekonyuu" Raffre <nk@nyuu.eu>

%description
Apache Kafka is a distributed publish-subscribe messaging system. It
is designed to support the following:

* Persistent messaging with O(1) disk structures that provide constant
  time performance even with many TB of stored messages.

* High-throughput: even with very modest hardware Kafka can support
  hundreds of thousands of messages per second.

* Explicit support for partitioning messages over Kafka servers and
  distributing consumption over a cluster of consumer machines while
  maintaining per-partition ordering semantics.

* Support for parallel data load into Hadoop.

Kafka provides a publish-subscribe solution that can handle all
activity stream data and processing on a consumer-scale web site. This
kind of activity (page views, searches, and other user actions) are a
key ingredient in many of the social feature on the modern web. This
data is typically handled by "logging" and ad hoc log aggregation
solutions due to the throughput requirements. This kind of ad hoc
solution is a viable solution to providing logging data to an offline
analysis system like Hadoop, but is very limiting for building
real-time processing. Kafka aims to unify offline and online
processing by providing a mechanism for parallel load into Hadoop as
well as the ability to partition real-time consumption over a cluster
of machines.

The use for activity stream processing makes Kafka comparable to
Facebook's Scribe or Apache Flume (beta1), though the
architecture and primitives are very different for these systems and
make Kafka more comparable to a traditional messaging system. See our
design page for more detail

%prep
%setup -n %{kafka_name}_2.10-%{kafka_version}

%patch0 -p0

%build

%clean
rm -rf %{buildroot}

%install
pwd
mkdir -p %{buildroot}/%{kafka_home}/
mkdir -p %{buildroot}/%{kafka_home}/config/
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/%{_sysconfdir}/security/limits.d/
mkdir -p %{buildroot}/var/log/kafka
mkdir -p %{buildroot}/%{etc_kafka}

cp -r %{_builddir}/%{kafka_name}_2.10-%{kafka_version}/bin          %{buildroot}/%{kafka_home}/
cp -r %{_builddir}/%{kafka_name}_2.10-%{kafka_version}/config       %{buildroot}/%{kafka_home}/
cp -r %{_builddir}/%{kafka_name}_2.10-%{kafka_version}/libs         %{buildroot}/%{kafka_home}/

cd %{buildroot}/opt/
ln -s %{kafka_name}-%{kafka_version} %{kafka_name}
cd -

cd %{buildroot}/%{etc_kafka}
ln -s %{kafka_home}/config config
cd -

cp %_sourcedir/kafka-server       %{buildroot}/%{_initrddir}/kafka-server
cp %_sourcedir/kafka              %{buildroot}/%{_sysconfdir}/sysconfig/kafka
cp %_sourcedir/kafka.nofiles.conf %{buildroot}/%{_sysconfdir}/security/limits.d/kafka.nofiles.conf

%pre
getent group %{kafka_group} >/dev/null || groupadd -r %{kafka_group}
getent passwd %{kafka_user} >/dev/null || /usr/sbin/useradd --comment "Kafka Daemon User" --shell /bin/bash -M -r -g %{kafka_group} --home %{kafka_home} %{kafka_user}

%files
%defattr(-,%{kafka_user},%{kafka_group})
/opt/%{kafka_name}
%{kafka_home}
%{kafka_home}/*
%{kafka_home}/config/*.properties
%attr(755,%{kafka_user},%{kafka_group}) %{kafka_home}/bin/*.sh
/etc/kafka/
%attr(755,%{kafka_user},%{kafka_group}) /var/log/kafka/
/etc/sysconfig/kafka
/etc/security/limits.d/kafka.nofiles.conf
%{_initrddir}/%{kafka_name}-server

%post
chkconfig --add %{kafka_name}-server
%preun
service %{kafka_name}-server stop > /dev/null 2>&1
chkconfig --del %{kafka_name}-server
%postun
service %{kafka_name}-server restart >/dev/null 2>&1

%changelog
* Fri Nov 11 2014 Jonathan Raffre <nk@nyuu.eu> [0.8.1.1-1]
- Initial Build Release 0.8.1.1.
