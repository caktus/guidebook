Developer Machine Security
==========================

SSH Keys
--------

Security is important and that starts with securely stored and accessed
credentials, because those credentials grant you access to all the other
infrastructure of a project. We have standards about the types, size,
and storage of SSH keys and this page will help you follow those
standards.

Current requirements:

-   SSH RSA key length of 2048 or more
-   SSH key stored with a passphrase

Current recommendations:

-   Ed25519 key

If you have an existing 2048-bit (or greater) key, you should add a
Ed25519 key as a secondary key so you can transition resources to your
more secure key over time. Eventually we may require Ed25519, so this
will help the transition by starting it sooner, without forcing you to
reset all your SSH keys on every server today.

### Listing Your Current Keys

List your current keys, their lengths, and whether or not your keys do
*not* have a passphrase (per [Stack
Exchange](https://unix.stackexchange.com/questions/500/how-can-i-determine-if-someones-ssh-key-contains-an-empty-passphrase)),
by running the following `bash` script:

``` {.sourceCode .bash}
shopt -s extglob
for keyfile in ~/.ssh/id_!(*.sock|*.pub); do \
  ssh-keygen -l -f "${keyfile}"; \
  ssh-keygen -p -P '' -N '' -f "$keyfile" >/dev/null 2>&1 && echo "WARNING: $keyfile has no passphrase"; \
done | uniq
```

Example output:

    256 SHA256:41p4W87laEgkXY/jYQXkYXm3C8PE7vwgoZLasXwNm3s copelco@caktusgroup.com (ED25519)
    4096 SHA256:2+dPQggqya9Q93U8eNFgcBamqP8mw3R62d/AfQbgrJM copelco@caktusgroup.com (RSA)
    4096 SHA256:BWTy9KXG5tPEuzTHqlS6xRwehbiMd7hUB/rHRTPE66I copelco@MBP0.local (RSA)
    WARNING: /Users/copelco/.ssh/id_rsa4096 has no passphrase

What to look for:

-   **DSA or RSA 1024 bits:** Red flag. Unsafe.
-   **WARNING: \<key\> has no passphrase**: Red flag. Unsafe.
-   **RSA 2048-4096 bits:** Recommend to transition to Ed25519.
-   **Ed25519:** Great!

### Adding SSH Key passphrases

If the checks above found keys that do not have a passphrase, then you
should add one now. To add passphrases to the existing keys in-place,
you can use this ssh-keygen command:

    ssh-keygen -f ${keyfile} -p -o -a 100

(`-o` = use newer file format, `-a 100` = number of KDF rounds, `-p` =
change password.)

If you have more than one key to add a passphrase to, you can get them
all with this snippet:

    shopt -s extglob
    for keyfile in ~/.ssh/id_!(*.sock|*.pub); do \
       ssh-keygen -f ${keyfile} -p -o -a 100 ; \
    done

You may use the same passphrase for all your SSH keys. If you do, then
[ssh-add]{.title-ref} will let you add \_[all]() of them to your SSH
agent at once, which will make it much easier to use multiple keys.

### Creating a Ed25519 Key

If you did not have a Ed25519 key, then you should create one now.

Create a new key:

    $ ssh-keygen -a 100 -t ed25519 -f ~/.ssh/id_ed25519

-   -a 100: KDF (Key Derivation Function) rounds. Higher numbers =
    increased brute-force resistance, but slower passphrase
    verification.
-   -t ed25519: the type of key to create, in our case the Ed25519
-   -P pass: Passphrase for the key
-   -f \~/.ssh/id\_ed25519: filename of the generated key file
-   (optional) -C <myname@whatever.com>: Comment for the key appended at
    the end of the public file

### Adding keys to ssh-agent

If all your keys have the same passphrase and you add them all to your
agent in one command, you\'ll only have to enter the passphrase once:

``` {.sourceCode .bash}
$ shopt -s extglob
$ ssh-add ~/.ssh/id_!(*.sock|*.pub)
```

Of if you\'re on a Mac (to add to your keychain):: bash

> \$ shopt -s extglob \$ ssh-add -K \~/.ssh/[id]()!(*.sock\|*.pub)

Possible shortcut: if all your keys are named \~/.ssh/id\_rsa,
\~/.ssh/id\_dsa, \~/.ssh/id\_ecdsa, \~/.ssh/id\_ed25519 or
\~/.ssh/identity, you can just use `ssh-add` with no arguments.

Now that you\'ve created a more secure Ed25519 key, or if you already
had one, you should treat this as your default key. You do not have to
replace your 2048-bit key everywhere at this time, but any \_[new]()
resources you or your team setup should use the new key. Add your key to
the company intranet, replacing any previous key you had, so that anyone
else granting you access to a server uses your new key.

If any of your previous keys were smaller than 2048-bit then you must
stop using them immediately. This means any servers you currently
require those keys to use must be updated, on a project-by-project
basis.
