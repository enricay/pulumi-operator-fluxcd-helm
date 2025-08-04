# Pulumi Kubernetes Operator - Staging Deployment

## Overview
This document explains how to deploy the Pulumi Kubernetes Operator to the staging environment using FluxCD and Kustomization.

## What Gets Deployed

When you deploy to staging, the following Kubernetes resources are created:

### 1. Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  labels:
    name: pulumi-kubernetes-operator
  name: pulumi-kubernetes-operator
```

### 2. HelmRepository (OCI Registry)
```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: HelmRepository
metadata:
  name: pulumi-kubernetes-operator
  namespace: pulumi-kubernetes-operator
spec:
  interval: 5m0s
  type: oci
  url: oci://ghcr.io/pulumi/helm-charts
```

### 3. HelmRelease
```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: pulumi-kubernetes-operator
  namespace: pulumi-kubernetes-operator
spec:
  chart:
    spec:
      chart: pulumi-kubernetes-operator
      interval: 5m0s
      sourceRef:
        kind: HelmRepository
        name: pulumi-kubernetes-operator
        namespace: pulumi-kubernetes-operator
      version: 2.0.0
  interval: 5m0s
  values: {}
```

## Configuration Details

- **Chart Version**: `2.0.0`
- **Namespace**: `pulumi-kubernetes-operator`
- **Values**: Using default Helm chart values (no customizations)
- **Update Interval**: 5 minutes
- **Chart Source**: OCI registry at `ghcr.io/pulumi/helm-charts`

## Deployment Steps

### Prerequisites
- Kubernetes cluster with FluxCD installed
- `kubectl` configured to connect to your staging cluster
- Proper RBAC permissions to create namespaces and install operators

### Deploy to Staging

1. **Preview what will be deployed:**
   ```bash
   kubectl kustomize infrastructure/stage/pulumi-operator
   ```

2. **Deploy to staging:**
   ```bash
   kubectl apply -k infrastructure/stage/pulumi-operator
   ```

3. **Verify deployment:**
   ```bash
   # Check HelmRelease status
   kubectl get helmreleases -n pulumi-kubernetes-operator
   
   # Check HelmRepository status
   kubectl get helmrepositories -n pulumi-kubernetes-operator
   
   # Check operator pods
   kubectl get pods -n pulumi-kubernetes-operator
   
   # Check operator logs
   kubectl logs -n pulumi-kubernetes-operator -l app.kubernetes.io/name=pulumi-kubernetes-operator
   ```

## Expected Resources After Deployment

Once deployed successfully, you should see:

### FluxCD Resources
- ✅ HelmRepository: `pulumi-kubernetes-operator` (READY: True)
- ✅ HelmRelease: `pulumi-kubernetes-operator` (READY: True)

### Kubernetes Resources (created by Helm)
- ✅ Namespace: `pulumi-kubernetes-operator`
- ✅ Deployment: `pulumi-kubernetes-operator-controller-manager`
- ✅ Service: `pulumi-kubernetes-operator-webhook-service`
- ✅ ServiceAccount: `pulumi-kubernetes-operator-controller-manager`
- ✅ ClusterRole: `pulumi-kubernetes-operator-manager-role`
- ✅ ClusterRoleBinding: `pulumi-kubernetes-operator-manager-rolebinding`

### Custom Resource Definitions (CRDs)
- ✅ `programs.pulumi.com`
- ✅ `stacks.pulumi.com`
- ✅ `updates.auto.pulumi.com`
- ✅ `workspaces.auto.pulumi.com`

## Monitoring Deployment Status

### Check HelmRelease Status
```bash
kubectl get helmrelease pulumi-kubernetes-operator -n pulumi-kubernetes-operator -o yaml
```

### Check Operator Health
```bash
# Pod status
kubectl get pods -n pulumi-kubernetes-operator

# Pod logs
kubectl logs -n pulumi-kubernetes-operator deployment/pulumi-kubernetes-operator-controller-manager

# Resource usage
kubectl top pods -n pulumi-kubernetes-operator
```

### Verify CRD Installation
```bash
kubectl get crds | grep pulumi
```

## Troubleshooting

### Common Issues

1. **HelmRepository not ready**
   - Check network connectivity to `ghcr.io`
   - Verify OCI registry permissions

2. **HelmRelease failed**
   - Check Helm chart compatibility
   - Review detailed status: `kubectl describe helmrelease pulumi-kubernetes-operator -n pulumi-kubernetes-operator`

3. **Operator pods not starting**
   - Check resource availability on nodes
   - Review pod events: `kubectl describe pod <pod-name> -n pulumi-kubernetes-operator`

### Cleanup Commands

To completely remove the staging deployment:

```bash
# Remove all resources
kubectl delete -k infrastructure/stage/pulumi-operator

# Clean up CRDs if needed
kubectl delete crd programs.pulumi.com stacks.pulumi.com updates.auto.pulumi.com workspaces.auto.pulumi.com
```

## Next Steps

After successful deployment, you can:

1. **Create Pulumi Stack resources** in the cluster
2. **Configure Pulumi access tokens** as Kubernetes secrets
3. **Set up GitOps workflows** for infrastructure management
4. **Monitor operator metrics** (if metrics are enabled)

## Architecture

```
staging-cluster/
├── pulumi-kubernetes-operator (namespace)
│   ├── HelmRepository (OCI: ghcr.io/pulumi/helm-charts)
│   ├── HelmRelease (chart: pulumi-kubernetes-operator:2.0.0)
│   └── Operator Deployment
│       ├── Controller Manager Pod
│       ├── Webhook Service
│       └── RBAC Resources
└── CRDs (cluster-wide)
    ├── programs.pulumi.com
    ├── stacks.pulumi.com
    ├── updates.auto.pulumi.com
    └── workspaces.auto.pulumi.com
```

## File Structure Reference

```
infrastructure/stage/pulumi-operator/
├── kustomization.yaml          # References base + applies patches
└── helmrelease-patch.yaml      # Staging-specific overrides (currently empty)

infrastructure/base/pulumi-operator/
├── kustomization.yaml          # Base resources list
├── namespace.yaml              # Namespace definition
├── helmrepository.yaml         # OCI Helm repository
└── helmrelease.yaml            # Base Helm release configuration
```
