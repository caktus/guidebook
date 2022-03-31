# From Caktus with Love

## Growth suggestions from cakti to cakti

** Command Line ** <br>
I highly suggest this [command line](https://www.udemy.com/course/the-linux-command-line-bootcamp/) class by instructor Colt Steele on Udemy. The class covers basic commands such as navigating your system, creating folders, removing files and more important and interesting conceps such as piping, grep, permission and how to alter them, modifying our own command lines, and more. While the class is lenghty, the instructor keeps it fun. There's a lot of power to the command line, and this course helped me tap a bit more into it.

Ronard 🌵

** Save Yourself ** <br>
If you use a *nix* style command line with any frequency and especially if you tend to be heavy handed with `rm -rf` do yourself a favor and install `trash-cli` on Debian derivatives, and add an alias to your shell's `rc` file: `alias rm="trash"`. If you ever make a mistake like I just did you can recover the files.

* [Ubuntu](https://manpages.ubuntu.com/manpages/jammy/en/man1/trash-put.1.html)
* [Mac](https://formulae.brew.sh/formula/trash-cli)

Jeremy 🌵

** Disable Homebrew auto updates ** <br>
Have you ever inocently tried install a package using [Homebrew](https://brew.sh/) and before you know it, Homebrew updates all of your dependecies? The result, all of your virtual environments are broken & much more. 
Well, there is a way to avoid that - rather than `brew install <formula>`, run `HOMEBREW_NO_AUTO_UPDATE=1 brew install <formula>`
   
Click [here](https://computingforgeeks.com/prevent-homebrew-auto-update-on-macos/) for more info. Credit to Dmitriy for the discovery.

Ronard 🌵

** Google Meet and Macs ** <br>
For anybody on a Mac who has had problems sharing their screen on a google meet, the following fixed it for me. I had to disallow Chrome's access to record my screen, then allow it again.

* Go to settings --> Security & Privacy --> Privacy tab --> Camera on left side
* There you can disallow, then allow again.

Michael 🌵

** The extension for YAML files is .yaml ** <br>
In the great YAML debate of 2022 Cakti agreed that .yaml was the correct extension for YAML files. 

Henceforth new projects at Caktus will use .yaml and old projects will be converted to .yaml as time allows.

Scott 🌵
