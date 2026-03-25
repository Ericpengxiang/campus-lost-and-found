#!/usr/bin/env python3
"""
Deploy campus-laf to Sealos via Kubernetes API
"""
import ssl, json, urllib.request, urllib.error, time

TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkhBQ05qTHhYb3E2djJwNGhPSjE5eTEzUnhYYmxnb3pDUEYzSUJndmJQUlkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJ1c2VyLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJzZWFsb3MtdG9rZW4tMHNzbWpwMG4tMTU1MCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiIwc3NtanAwbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImE3Zjk1MDZmLWI0NDEtNDM0Zi1iZDY4LTUyNGViZDg3Mjg3MyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDp1c2VyLXN5c3RlbTowc3NtanAwbiJ9.J04ysEMJ98FZJLolAXnzWyt3dYQKOcqxGSHZd1hJp5Rv88txHTJw2OG4AOaUmqSa3mc9YDyGrybNUU-eHlEeqKwoU9F7bVv_WuScoF0xMVQu6y3Js0c40peMrmiCr_NrsopVCp5EhQO656P5Ueak-QCVCDO8TFSnq2Kl-ls6055DsqhDief8QNhrZOQb-jXeWqXt_XqW1CGSTe8S1mR8ziYodn2TAN5kePtwPRuVzXfaHNPcXO5edfPv6gYzNN8iqiXGjoJDNlVtFE3nIRwuMYx6bdYZgdBG51DW9bb2pkc9OyOL3hgvoGiDPF2ZaHDdb3p2_sN-LJEoC--riOlDNg"
SERVER = "https://cloud.sealos.io:6443"
NS = "ns-0ssmjp0n"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def api_request(method, path, body=None):
    url = f"{SERVER}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())
    except Exception as e:
        return 0, {"error": str(e)}

def apply_or_update(resource_type, api_path, body):
    name = body["metadata"]["name"]
    print(f"  Applying {resource_type}/{name}...")
    
    # Try GET first
    status, _ = api_request("GET", f"{api_path}/{name}")
    
    if status == 200:
        # Resource exists, update it
        status, resp = api_request("PUT", f"{api_path}/{name}", body)
        if status in (200, 201):
            print(f"  ✓ Updated {resource_type}/{name}")
        else:
            print(f"  ✗ Failed to update: {resp.get('message', resp)}")
    elif status == 404:
        # Create new
        status, resp = api_request("POST", api_path, body)
        if status in (200, 201):
            print(f"  ✓ Created {resource_type}/{name}")
        else:
            print(f"  ✗ Failed to create: {resp.get('message', resp)}")
    else:
        print(f"  ✗ Unexpected status {status}")

# ── Deployment ──────────────────────────────────────────────────
deployment = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "campus-laf",
        "namespace": NS,
        "labels": {"app": "campus-laf"}
    },
    "spec": {
        "replicas": 1,
        "selector": {"matchLabels": {"app": "campus-laf"}},
        "template": {
            "metadata": {"labels": {"app": "campus-laf"}},
            "spec": {
                "containers": [{
                    "name": "campus-laf",
                    "image": "zxseric/campus-lost-and-found:latest",
                    "imagePullPolicy": "Always",
                    "ports": [{"containerPort": 80}],
                    "env": [
                        {"name": "DEBUG", "value": "False"},
                        {"name": "SECRET_KEY", "value": "campus-laf-sealos-prod-2024-xjt"},
                        {"name": "ALLOWED_HOSTS", "value": "*"},
                    ],
                    "resources": {
                        "requests": {"cpu": "100m", "memory": "256Mi"},
                        "limits": {"cpu": "500m", "memory": "512Mi"},
                    },
                }]
            }
        }
    }
}

# ── Service ──────────────────────────────────────────────────────
service = {
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {"name": "campus-laf", "namespace": NS},
    "spec": {
        "selector": {"app": "campus-laf"},
        "ports": [{"protocol": "TCP", "port": 80, "targetPort": 80}],
        "type": "ClusterIP",
    }
}

# ── Ingress ──────────────────────────────────────────────────────
ingress = {
    "apiVersion": "networking.k8s.io/v1",
    "kind": "Ingress",
    "metadata": {
        "name": "campus-laf",
        "namespace": NS,
        "annotations": {
            "kubernetes.io/ingress.class": "nginx",
            "nginx.ingress.kubernetes.io/proxy-body-size": "20m",
        }
    },
    "spec": {
        "rules": [{
            "host": "campus-laf.cloud.sealos.io",
            "http": {
                "paths": [{
                    "path": "/",
                    "pathType": "Prefix",
                    "backend": {
                        "service": {
                            "name": "campus-laf",
                            "port": {"number": 80}
                        }
                    }
                }]
            }
        }],
        "tls": [{
            "hosts": ["campus-laf.cloud.sealos.io"],
            "secretName": "wildcard-cloud-sealos-io-cert"
        }]
    }
}

print("=== Deploying Campus Lost & Found to Sealos ===")
print(f"Namespace: {NS}")
print()

print("[1/3] Deploying...")
apply_or_update("Deployment", f"/apis/apps/v1/namespaces/{NS}/deployments", deployment)

print("[2/3] Service...")
apply_or_update("Service", f"/api/v1/namespaces/{NS}/services", service)

print("[3/3] Ingress...")
apply_or_update("Ingress", f"/apis/networking.k8s.io/v1/namespaces/{NS}/ingresses", ingress)

print()
print("=== Checking deployment status ===")
time.sleep(3)
status, resp = api_request("GET", f"/apis/apps/v1/namespaces/{NS}/deployments/campus-laf")
if status == 200:
    spec = resp.get("spec", {})
    ds = resp.get("status", {})
    print(f"Replicas: {spec.get('replicas')} desired, {ds.get('readyReplicas', 0)} ready")
    print()
    print("✓ Deployment submitted successfully!")
    print()
    print("=== Access Information ===")
    print("URL: https://campus-laf.cloud.sealos.io")
    print("Admin: admin / admin123456")
    print()
    print("Note: First startup takes ~60s for DB init and seed data.")
else:
    print(f"Could not get deployment status: {status}")
