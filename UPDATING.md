# docker-compose installation

The best way of launching tower is to setup it via docker and docker compose.

Updating tower as simple as 
```
cd /etc/docker-compose/tower
docker-compose pull
docker-compose down
docker-compose up -d
```

If you are using install without docker there is  [migration guide](docs/migrate_dc.md)



<details>
<summary>Also there is a way to update tower manually </summary>

Meanwhile old method of updating noc-tower is still supported. 

To do so 
check if pip version is greater than 1.5 to do so 
<pre><code>
# cd /opt/tower
# ./bin/pip --version 
# ./bin/pip install --upgrade pip
# ./bin/pip --version 
</code></pre>
than 
<pre><code>
# cd /opt/tower
# ./bin/pip install --upgrade https://cdn.getnoc.com/tower/noc-tower-latest.zip
</code></pre>
After it please recheck if ansible version is good enough. Current is is 2.5

<pre><code>
# cd /opt/tower
# ./bin/ansible --version
ansible 2.5.0
  config file = 
  configured module search path = Default w/o overrides

</code></pre>

If ansible version is too old update it with 
<pre><code>
# ./bin/pip install --upgrade ansible
</code></pre>


</details>
