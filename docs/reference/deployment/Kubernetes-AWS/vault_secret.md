# Configure A Secret for Ansible Vault

## On AWS

1. From the AWS console navigate to the `AWS secrets manager`
1. Click `Store a new secret`
1. Select `Other type of secret`
1. Select `Plaintext`
1. Remove the dictionary.
1. Generate a secret key from the command line `pwgen -n 64`
1. Copy one of the keys into the plaintext input. Ensure that the key is the only string present
1. Ensure that `Encryption key` has `aws/secretsmanager` selected
1. Click `Next`
1. Give your secret a name. Convention is `<projectname>-ansible-vault-secret`
1. Click `Next`
1. Click `Next` again.

## Local

In `deploy/echo-vault-pass.sh` add the secret name to the `export SECRET_ID` line.

```shell
8 export SECRET_ID="<projectname>-ansible-vault-secret"
```