# noc-tower helm chart

Please mention that tower is *not* for configuring noc in k8s.

That is just old plain tower to configure noc on VMs.


**Install**
0. install k3s https://k3s.io/
1.  install HELM https://github.com/helm/helm
2.  cd contrib/k8s/
3.  helm install --replace  noc-tower/  --debug --set ingress.host=*towerhostname*

**Example**
 
`helm install --replace  noc-tower/  --debug --set ingress.host=tower.k3s.local`

check pod state 

`kubectl get --all-namespaces=true all`

Open web site 

`https://towerhostname`