# Developer On-boarding Documentation

This documentation is meant for new developers at Caktus Consulting Group. It describes our particular
setup and development workflow. It is not meant as a prescription but as a path that is well tested and
known to work. Of course there are some steps, which if not followed, will result in an inability to use or 
access services, or result in a difficult time seeking help from your fellow developers. So if you know the 
consequences of straying from the Golden Path feel free to play around with these setup steps. If you are 
fresh-faced and apple cheeked, best to follow exactly.

See you on the other side and happy coding.

## Caktus' Golden Path Tech Stack

We have stolen the idea of the Golden Path from a Spotify [blog post](https://engineering.atspotify.com/2020/08/17/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem/). The idea is as they put it in their post.

!!! quote

    This is the way we support an easy and streamlined way of working. If you are an adventurer you can of course leave the Golden Path and do your own thing, but then you will not have the same support.


!!! note

    Assumptions about what is or is not "Golden Path" were made solely by me (Jeremy Gibson). Today. During shipit. We should probably come together as a company wide team and hammer this out.

## Core Stack
The following list are the primary technologies that we use right now.

1. [Python](https://www.python.org/ "Readability counts")
1. [Django](https://www.djangoproject.com/ "The web framework for perfectionists with deadlines")
1. [Wagtail](https://wagtail.io/ "Wagtail, the powerful CMS for modern websites")
1. [PostgreSQL](https://www.postgresql.org/ "An open source object-relational database system")
1. [Ansible](https://www.ansible.com/ "A foundation for building and operating automation across an organization")
1. [React](https://reactjs.org/ "A JavaScript library for building user interfaces") 
1. [Kubernetes](https://kubernetes.io/ "An open-source system for automating deployment, scaling, and management of containerized applications")
1. [AWS](https://aws.amazon.com/ "Amazon Web Services Cloud Services")

## Support Stack

!!! warning "hic sunt dracones"
    This is also the point where those of you who feel like striking off from the Golden Path would typically do so. 

This stack is more fungible than the core stack and may change, or may not apply to older projects. If you are working on a project that comes from [jade-truffle](https://github.com/caktus/jade-truffle "The smallest Caktus project") then these will be assumed.  


1. [direnv](https://direnv.net/ "Unclutter your profile")
1. [pyenv](https://github.com/pyenv/pyenv "pyenv lets you easily switch between multiple versions of Python")
1. [nvm](https://github.com/nvm-sh/nvm "Node Version Manager - POSIX-compliant bash script to manage multiple active node.js versions")
1. [invoke-kubesae](https://github.com/caktus/invoke-kubesae, "For running tasks in projects")
1. [Docker](https://www.docker.com/ "Build, share, and run any app, anywhere")


## Tech We Are Experimenting with

1. [Poetry](https://python-poetry.org/ "Python Packaging and Dependency Mangement made easy")
1. [PDM](https://github.com/pdm-project/pdm "A modern Python package manager with PEP 582 support")

## Recommended Setup Path

!!! note

    If you have an M1 start there.

1. [M1](./M1.md)
1. [AWS Setup](./AWS.md)
1. [Kubernetes Setup](./kubernetes.md)
