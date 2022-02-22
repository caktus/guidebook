
(This is an example of a more streamlined super-project workflow, for cases where the super-project doesn't change as much as the submodule during development.
A good example is `rebar-site`'s `rebar_cms`, where our work is almost entirely concentrated in the cms submodule.)

# Superproject Inclusion Workflow

## Description
rebar-cms is designed as a submodule which means that development of the
library will typically happen in the context of development on a superproject. A superproject is
any project that contains a submodule link. For rebar-cms the primary superproject is
rebar-site, though rebar-cms may well also be included in other projects in the future
such as the investigator portal.

This doc is intended to serve as a template that will ensure a consistent and
predictable workflow for committing versions of the library into superprojects.
It's a bit simplified currently as we have only one including
project, but can be expanded to cover the multi-superproject case later.


NOTE: In this doc, we use the newer `git switch` command rather that `git checkout`. They are compatible with each other,
but git [has opinions](https://git-scm.com/docs/git-switch).

## Phases

1. Development
1. Review
1. Release

For illustration in this document, we will assume work on a `hero_block` to be added to superproject SP1.


### Development

During development, both the superproject and rebar-cms should be on a branch that
references the same ticket.

If `SP1` is the primary superproject, then development should begin there with a ticket.

Assuming we are starting from the develop branch of `SP1` with a ticket `1`:

```shell
    (SP1) (develop)$ git switch -c SP1-1-hero-block
    (SP1) (SP1-1-hero-block)$ cd rebar_cms/
    (SP1/rebar_cms) (HEAD)$ git switch -c SP1-1-hero-block
    (SP1/rebar_cms) (SP1-1-hero-block)$ <make changes>
```

(The branch names here are using Jira convention name, Shortcut's suggested names are longer but
should be used if that is the tracker in use for the ticket.)

As you develop the feature on `SP1`, you will be committing changes to the block library along with the
superproject.

### Review

When the superproject and rebar-cms code changes are ready for review, open PR's on the superproject and add,
as a checkbox in the library's PR body, each project that the library work is impacting.

Before the library can be merged and released, all superproject PR's must be approved, with the latest commit of the 
block library. As they are approved, mark off the task boxes.

### Release

The state we are in now is this:
```shell
rebar-cms commit(abc123): PR approved
SP1: PR approved with rebar-cms(abc123)

```

Now merge the rebar-cms PR into the `main` branch and release a version.

#### Tag Version Format

The tag shall follow the following format:

The leading part of the tag should be the date in iso format at the beginning. After the `day` part of the date add a `-`
and a trailing sequence number. The first number of the sequence should be `1`.

```shell
    2021-03-15-1
```

Then add a description that contains the changes introduced by the release.

#### Fix the Release in the superprojects

After the release has been created, return to each of the superprojects and do the following, for the
example release noted above:

```shell
    (SP1) (SP1-1-hero-block)$ cd rebar_cms/
    (SP1/rebar_cms) (HEAD)$ git fetch --all 
    (SP1/rebar_cms) (HEAD)$ git switch 2021-03-15-1
    (SP1/rebar_cms) (2021-03-15-1)$ cd -
    (SP1) (SP1-1-hero-block)$ git add .
    (SP1) (SP1-1-hero-block)$ git commit -m "Pin rebar-cms to release 2021-03-15-1"
```

Then commit the changes. This will fix the commit hash for the submodule to the released version.
It is a good idea to include in the message of the commit some indication that this
is what you are doing (e.g. "git commit -m 'Pin rebar-cms  to release 2021-03-15-1')

Push your changes to the superproject and merge into develop.
