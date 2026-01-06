Name: springboot-camel
Version: 1.0.0
Release: 2%{?dist}
Summary: Spring Boot Camel Application

License: Proprietary
BuildArch: noarch

%description
Spring Boot Apache Camel application packaged as an RPM
with DEV and QA systemd services.

%install
# Create directories
mkdir -p %{buildroot}/opt/springboot/dev
mkdir -p %{buildroot}/opt/springboot/qa
mkdir -p %{buildroot}/etc/systemd/system

# Copy application JAR
cp %{_sourcedir}/app.jar %{buildroot}/opt/springboot/dev/app.jar
cp %{_sourcedir}/app.jar %{buildroot}/opt/springboot/qa/app.jar

# Copy systemd services
cp %{_sourcedir}/springboot-dev.service %{buildroot}/etc/systemd/system/
cp %{_sourcedir}/springboot-qa.service %{buildroot}/etc/systemd/system/

%post
systemctl daemon-reload

%files
/opt/springboot/dev/app.jar
/opt/springboot/qa/app.jar
/etc/systemd/system/springboot-dev.service
/etc/systemd/system/springboot-qa.service
