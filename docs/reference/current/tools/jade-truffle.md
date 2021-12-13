# [Jade-Truffle (the smallest caktus)](https://github.com/caktus/jade-truffle)

Jade Truffle is the Mandarin traslation of the cacti species
*blossfeldia liliputana*. The smallest of all cacti.

Jade Truffle is a
[cookiecutter](https://github.com/cookiecutter/cookiecutter) template
designed to generate a greenfield Django or Wagtail project.

Jade Truffle is a work in progress. The intention is to make the base
project quickly deployable, while at the same time allowing for project
specific overrides.

Currently the template is highly tuned to an AWS/EKS deployment
methodology using [Django
K8s](https://github.com/caktus/ansible-role-django-k8s), [AWS Web
Stacks](https://github.com/caktus/ansible-role-aws-web-stacks), and [K8s
Web Cluster](https://github.com/caktus/ansible-role-k8s-web-cluster).
The hope is that future work will add to the deployment methods.

Requirements
------------

-   Python 3.8
-   pip-tools
-   cookiecutter
-   A virtual environment manager
-   direnv
-   pyenv

Installation
------------

Create a Python virtual environment with your tool of choice. For
purposes of these instructions we'll call the environment
`jade-truffle`.

Enable your environment and install cookiecutter:

    (jade-truffle)$ pip install cookiecutter

Now you have an environment that can install cookiecutter templates.

Next use cookiecutter to build a project using `jade-truffle`:

    (jade-truffle)$ cookiecutter https://github.com/caktus/jade-truffle

Options
-------

The cookiecutter will run through a series of configuration options

1. Project Name: This can be anything you like (e.g. Apple Pie)

1. Project Slug: Generated from the Project Name, but can be overridden.
   Used in most configuration options in the generated project.
    
        apple_pie/apple_pie/settings
        apple_pie/apple_pie/urls.py

1. Project Type: `django` or `wagtail`
1. Testing Type: `django` or `pytest`
1. CSS Style: `sass` or `tailwind`
1. CI/CD: `actions` or `circleci`    
1. Cloud Provider: `aws` or `gcp`
1. Postgres Port: Defaults to `5432`
   This is used for local dev so you can set this to any port you like. 
   
        NOTE: If you have a postgres server running locally on port 5432, you
        will want to choose a different port than 5432.

1. Primary App: Will be used as the main app in the projects apps directory.
   
        For example: `apple_pie/apps/apple_pie`

1. Project Domain Name:
    
        Defaults to `caktus-built.com`

The generated project has a README that details the steps for install.