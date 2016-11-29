ec2-meta-env
============

A simple wrapper script to manifest EC2 instance metadata as environment
variables.

Installing ec2-meta-env
=======================

Installing `ec2-meta-env` is as simple as::

    pip install ec2-meta-env --upgrade


Using ec2-meta-env
==================

To include EC2 instance meta data in your application's shell environment,
wrap your shell command with the `ec2-meta-env` script and specify the
environment variables you wish to use, e.g.::

    ec2-meta-env -e local-ipv4 /path/to/my/app

In the above example, the value of `local-ipv4` will be accessible in the shell
environment for `/path/to/my/app` under the variable name `EC2_LOCAL_IPV4`.
Environment variable names are formed by prepending the meta API path with
`EC2_`, uppercasing, and replacing all dashes and forward slashes with
underscores.

Other options
=============

A complete list of options can be found by running::

    ec2-meta-env --help

Why ec2-meta-env?
=================

EC2 provides instance metadata via `http://169.254.169.254/latest/meta-data/`.
Sometimes it's easier to use that information if it's available via environment
variables, for example, if your application's running inside a Docker container
on Amazon's Elastic Container Service (ECS). This project makes it possible to
do that without calling the EC2 instance meta data API manually.


Thanks and I hope you find ec2-meta-env helpful!

~Tobias McNulty
