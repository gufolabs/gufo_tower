# Git Repository URL Format

Gufo Tower uses Git repository URLs to obtain Ansible playbooks and Extra Roles.

The following URL schemes are supported:

| Scheme | Description |
| --- | --- |
| `http://` | Git repository accessed over HTTP. |
| `https://` | Git repository accessed over HTTPS. |
| `git://` | Git repository accessed using the Git protocol. |
| `ssh://` | Git repository accessed using SSH. |
| `git+http://` | Git repository accessed over HTTP using Git/Pip-style URL syntax. |
| `git+https://` | Git repository accessed over HTTPS using Git/Pip-style URL syntax. |
| `git+ssh://` | Git repository accessed using SSH using Git/Pip-style URL syntax. |