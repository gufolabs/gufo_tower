**********
Node setup
**********

Following steps are necessary to prepare the node for NOC deployment


Proxy setup
###########
Setting up proxy to work with ansible may be somewhat tricky tasks

System environment setup
************************
Set up system environment on LSB systems:

.. code-block::

    # cat > /etc/profile.d/proxy.sh
    https_proxy="http://<IP>:<port>/"
    https_proxy="http://<IP>:<port>/"
    export http_proxy https_proxy
    _EOF_

Set up ssh environment:

.. code-block::

    # cat > ~/ansible/.ssh/environment << _EOF_
    https_proxy=http://<IP>:<port>/
    https_proxy=http://<IP>:<port>/
    _EOF_

Set up ssh daemon:

.. code-block::

    # cat >> /etc/ssh/sshd_config << _EOF_
    PermitUserEnvironment yes
    UseDNS no
    _EOF_

Check /etc/sudoers. If you have *Defaults env_reset* add following

.. code-block::

    Defaults        env_keep += "http_proxy"
    Defaults        env_keep += "https_proxy"

