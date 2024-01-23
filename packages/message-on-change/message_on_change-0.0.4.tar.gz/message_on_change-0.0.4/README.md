<h1>message_on_change</h1> is a small python program, that let's you check if a url has changed since the starting of the script.
This can be useful for
<li>
    Awaiting some results on some website
</li>
<li>
    Monitoring the update schedule of some sites
</li>

if you install the package regularly it will probably not be available as a shell command
on your system, and instead be installed in the ``.local/bin`` directory, from witch based on your shell
configuration you cannot launch the application.

Install with sudo to resolve:

```commandline
$ sudo pip install message-on-change
```

