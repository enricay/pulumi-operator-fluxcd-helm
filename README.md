# Pulumi Kubernetes Operator - FluxCD Helm Deployment

This repository contains the FluxCD configuration for deploying the Pulumi Kubernetes Operator using the official Helm chart across multiple environments.

## Overview

The Pulumi Kubernetes Operator enables managing Pulumi stacks as Kubernetes resources, providing a GitOps approach to infrastructure management. This deployment uses the official Helm chart from `oci://ghcr.io/pulumi/helm-charts/pulumi-kubernetes-operator`.

## Architecture

```
flux-cd/
├── infrastructure/
│   ├── base/pulumi-operator/           # Base Helm configuration
│   │   ├── kustomization.yaml          # Base kustomization
│   │   ├── helmrepository.yaml         # OCI Helm repository
│   │   └── helmrelease.yaml            # Base HelmRelease
│   ├── test/pulumi-operator/           # Test environment overlay
│   │   ├── kustomization.yaml          # Test-specific config
│   │   └── helmrelease-patch.yaml      # Test resource limits & config
│   ├── stage/pulumi-operator/          # Staging environment overlay
│   │   ├── kustomization.yaml          # Stage-specific config
│   │   └── helmrelease-patch.yaml      # Stage resource limits & config
│   └── prod/pulumi-operator/           # Production environment overlay
│       ├── kustomization.yaml          # Prod-specific config
│       └── helmrelease-patch.yaml      # Prod resource limits & config
└── clusters/
    ├── test/infrastructure.yaml        # Test cluster FluxCD Kustomization
    ├── stage/infrastructure.yaml       # Stage cluster FluxCD Kustomization
    └── prod/infrastructure.yaml        # Prod cluster FluxCD Kustomization
```

## Deployment Configuration

### Base Configuration
- **Namespace**: `pulumi-kubernetes-operator`
- **Chart**: `oci://ghcr.io/pulumi/helm-charts/pulumi-kubernetes-operator`
- **Version**: `>=2.1.0`
- **RBAC**: Enabled
- **Metrics**: Enabled

### Environment-Specific Overrides

#### Test Environment
- **CPU Limits**: 500m
- **Memory Limits**: 512Mi
- **CPU Requests**: 100m
- **Memory Requests**: 256Mi
- **Pod Labels**: environment=test

#### Stage Environment
- **CPU Limits**: 750m
- **Memory Limits**: 1Gi
- **CPU Requests**: 250m
- **Memory Requests**: 512Mi
- **Pod Labels**: environment=stage

#### Production Environment
- **CPU Limits**: 1000m
- **Memory Limits**: 2Gi
- **CPU Requests**: 500m
- **Memory Requests**: 1Gi
- **Pod Labels**: environment=prod
- **Node Selector**: `node-type: operator`
- **Tolerations**: operator nodes

**Note**: All other values use the official Helm chart defaults for maximum compatibility.

## FluxCD Integration

The operator is deployed via FluxCD Kustomizations referencing:
- Test: `./infrastructure/test/pulumi-operator`
- Stage: `./infrastructure/stage/pulumi-operator`
- Production: `./infrastructure/prod/pulumi-operator`

## Deployment

1. **Commit and push** this repository to your Git repository
2. **Apply the cluster configuration** to your FluxCD-enabled clusters:

```bash
# For test cluster
kubectl apply -f clusters/test/infrastructure.yaml

# For stage cluster  
kubectl apply -f clusters/stage/infrastructure.yaml

# For prod cluster
kubectl apply -f clusters/prod/infrastructure.yaml
```

## Verification

### Check FluxCD Status
```bash
# Check if the Kustomization is ready
kubectl get kustomizations -n flux-system | grep pulumi-operator

# View detailed status
kubectl describe kustomization pulumi-operator -n flux-system

# Check HelmRelease status
kubectl get helmreleases -n pulumi-kubernetes-operator
```

### Check Operator Status
```bash
# Check namespace
kubectl get namespace pulumi-kubernetes-operator

# Check operator pods
kubectl get pods -n pulumi-kubernetes-operator

# Check operator logs
kubectl logs -n pulumi-kubernetes-operator -l app.kubernetes.io/name=pulumi-kubernetes-operator

# Verify CRDs are installed
kubectl get crds | grep pulumi
```

### Expected Resources
- Namespace: `pulumi-kubernetes-operator`
- HelmRepository: `pulumi-kubernetes-operator`
- HelmRelease: `pulumi-kubernetes-operator`
- Deployment: `pulumi-kubernetes-operator`
- Service: `pulumi-kubernetes-operator-metrics`
- CRDs: `programs.pulumi.com`, `stacks.pulumi.com`, `updates.auto.pulumi.com`, `workspaces.auto.pulumi.com`

## Usage

Once deployed, you can create Pulumi stacks as Kubernetes resources:

```yaml
apiVersion: pulumi.com/v1
kind: Stack
metadata:
  name: my-infrastructure
  namespace: pulumi-kubernetes-operator
spec:
  stack: dev
  projectRepo: https://github.com/your-org/your-pulumi-project.git
  branch: main
  envRefs:
    PULUMI_ACCESS_TOKEN:
      type: Secret
      secret:
        name: pulumi-access-token
        key: token
  destroyOnFinalize: true
```

## Helm Chart Benefits

Using the Helm chart provides:
- **Easy version management**: Automatic updates with version constraints
- **Rich configuration**: Full Helm values.yaml support
- **Official support**: Maintained by the Pulumi team
- **Flexible patching**: Environment-specific value overrides

## Maintenance

### Updating the Operator
1. Update the version constraint in `base/helmrelease.yaml`
2. Test changes in the test environment first
3. Promote through stage to production

### Modifying Configuration
1. Edit the appropriate `helmrelease-patch.yaml` file
2. Commit and push changes
3. FluxCD will automatically apply updates

## Troubleshooting

### Common Issues

1. **HelmRepository not ready**: Check OCI registry connectivity
2. **HelmRelease failed**: Check Helm values compatibility
3. **Operator not starting**: Check resource limits and node capacity

### Logs and Debugging
```bash
# View FluxCD logs
kubectl logs -n flux-system -l app=helm-controller
kubectl logs -n flux-system -l app=source-controller

# View HelmRelease status
kubectl describe helmrelease pulumi-kubernetes-operator -n pulumi-kubernetes-operator

# Check operator logs
kubectl logs -n pulumi-kubernetes-operator -l app.kubernetes.io/name=pulumi-kubernetes-operator

# Check resource usage
kubectl top pods -n pulumi-kubernetes-operator
```

## Security Considerations

- Each environment deploys to separate clusters for isolation
- Environment-specific resource limits prevent resource exhaustion
- RBAC is configured via the Helm chart
- Access tokens should be stored as Kubernetes secrets
- Production environment uses node selectors and tolerations for dedicated nodes
