# Making SSH Keys

## Making your SSH keys
### Unix Systems (Mac/Linux)
```
$ cd ~
$ mkdir .ssh
$ ssh-keygen -C "youremail@whatever.com"
Generating public/private rsa key pair.
Enter file in which to save the key (/home/username/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/username/.ssh/id_rsa.
Your public key has been saved in /home/username/.ssh/id_rsa.pub.
The key fingerprint is: someLongStringOfText
```

### Windows
Open a Git bash terminal
```
$ cd ~
$ mkdir .ssh
$ ssh-keygen.exe -C "youremail@whatever.com"
Generating public/private rsa key pair.
Enter file in which to save the key (C:/Users/username/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in C:/Users/username/.ssh/id_rsa.
Your public key has been saved in C:/Users/username/.ssh/id_rsa.
The key fingerprint is: someLongStringOfText
```

## Copying Your **PUBLIC** Key
Cannot stress this enough: use the file with ".pub" at the end. The other one is your **private** key that can be used to access your system if the wrong people had it.

Assuming you are still in your home folder (either "/home/username/" or "C:/Users/username/"),
for all systems (Unix users in Terminal, Windows in Git bash terminal):
```
$ cd .ssh/
$ less id_rsa.pub
```
You should now see a very long string of text ending in the email you entered before. Copy this entire string.

## Adding Your Public SSH Key to GitLab
* Login to [Gitlab](https://gitlab-sysprog.informatik.uni-bonn.de/users/sign_in)
* Click on the symbol in the top right --> Settings --> SSH Keys
* Paste the contents of your public key in the main box and give it a description title (e.g. Personal Laptop)
* Press "Add Key"

## Cloning Repos
From now on, you should be able to clone repositories using the SSH "Clone with SSH"
