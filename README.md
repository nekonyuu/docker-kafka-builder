## Description
This docker allows to build an Apache Kafka RPMs in a contained environment. Built RPMs support CentOS 6 for now.

# Building

You can either use the public image or build it yourself. The public one :

    docker run -v $(pwd):/target nekonyuu/kafka-builder

This will build the RPMs and copy them in your current folder. You just need to modify "$(pwd)" by your chosen path if you want them at another place.
