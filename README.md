# autoshrink
An opererator that can shrink all deployments (based on a label) to 0 or the original size.

It is intended to be used for the case where applications are deployed in a secondary cluster with deployments set to 0 replicas, until a condition is met. 

The code provided switches on a timer.

# run locally
point at the cluster

```
minukube start
. venv/bin/activate
pip install -r requirements.txt
kopf run operator-autoshrink.py
# in another terminal:
helm install test sample-helm-chart
```

# deployment
see https://kopf.readthedocs.io/en/stable/deployment/