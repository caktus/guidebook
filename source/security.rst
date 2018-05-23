Developer Machine Security
##########################

SSH Keys
========

Security is important and that starts with securely stored and accessed credentials, because those
credentials grant you access to all the other infrastructure of a project. We have standards about
the types, size, and storage of SSH keys and this page will help you follow those standards.

Current requirements:

- SSH Length of 2048 or more
- SSH Key stored with a passphrase

Current recommendations:

- SSH Length of 4096 or more

If you have an existing 2048-bit key, you should add a 4096-bit key as a secondary key so you can
transition resources to your more secure key over time. Eventually we may require 4096 bits, so
this will help the transition by starting it sooner, without forcing you to reset all your SSH
keys on every server today.

First, list your current keys and their lengths, by running the following::

    shopt -s extglob; for keyfile in ~/.ssh/id_!(*.sock|*.pub); do \
       ssh-keygen -l -f "${keyfile}"; \
    done | uniq

You'll see some output that shows your keys and their lengths::

    2048 SHA256:aoHoYrBFq/1OwR6BZT4YsYkFCBjJIfgkya5uA/BsiU4 calvin@MBP5.local (RSA)
    2048 SHA256:alNfvb6ar8mpQg4HdhuX8xgEgUUcZow/R63CxjezWcU calvin@caktus001 (RSA)

Second, we'll check if any of your keys do *not* have a passphrase::

    shopt -s extglob; for keyfile in ~/.ssh/id_!(*.sock|*.pub); do \
      ssh-keygen -p -P '' -N '' -f "$keyfile" >/dev/null 2>&1 && echo "WARNING: $keyfile has no passphrase"; \
    done

(per https://unix.stackexchange.com/questions/500/how-can-i-determine-if-someones-ssh-key-contains-an-empty-passphrase)

Adding SSH Key passphrases
--------------------------

If the checks above found keys that do not have a passphrase, then you should add one now. To add passphrases to the existing keys in-place, you can use this ssh-keygen command::

    ssh-keygen -f ${keyfile} -p -o -a 100

(``-o`` = use newer file format, ``-a 100`` = number of KDF rounds, ``-p`` = change password.)

If you have more than one key to add a passphrase to, you can get them all with this snippet::

    shopt -s extglob; for keyfile in ~/.ssh/id_!(*.sock|*.pub); do \
       ssh-keygen -f ${keyfile} -p -o -a 100 ; \
    done

You may use the same passphrase for all your SSH keys. If you do, then `ssh-add` will let you add _all_ of them to your
SSH agent at once, which will make it much easier to use multiple keys.


Creating a 4096-bit RSA Key
----------------------------

If you did not have any 4096-bit keys, then you should create one now.

Create a new key::

    $ ssh-keygen -o -a 100 -t rsa -b 4096 -f ~/.ssh/id_rsa4096
    Generating public/private RSA key pair.
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /home/gert/.ssh/id_rsa4096.
    Your public key has been saved in /home/gert/.ssh/id_rsa4096.pub.
    The key fingerprint is:
    SHA256: [...] gert@hostname
    The key's randomart image is: [...]

Adding keys to ssh-agent
------------------------

If all your keys have the same passphrase and you add them all to your
agent in one command, you'll only have to enter the passphrase once::

    $ shopt -s extglob; ssh-add ~/.ssh/id_!(*.sock|*.pub)
    Enter passphrase for /Users/calvin/.ssh/id_rsa:
    Identity added: /Users/calvin/.ssh/id_rsa (/Users/calvin/.ssh/id_rsa)
    Identity added: /Users/calvin/.ssh/id_ed25519 (calvin@172-20-0-91.caktus.lan)

Possible shortcut: if all your keys are named ~/.ssh/id_rsa, ~/.ssh/id_dsa,
~/.ssh/id_ecdsa, ~/.ssh/id_ed25519 or ~/.ssh/identity, you can just use
``ssh-add`` with no arguments.

Now that you've created a more secure 4096-bit key, or if you already had one, you should treat this as your default key. You do not have to replace your 2048-bit key everywhere at this time, but any _new_ resources you or your team setup should use the new key. Add your key to the company intranet, replacing any previous key you had, so that anyone else granting you access to a server uses your new key.

If any of your previous keys were smaller than 2048-bit then you must stop using them immediately. This means any servers you currently require those keys to use must be updated, on a project-by-project basis.
