import pulumi
import pulumi_kubernetes as k8s

# Create a simple ConfigMap
config_map = k8s.core.v1.ConfigMap(
    "sample-configmap",
    metadata=k8s.meta.v1.ObjectMetaArgs(
        name="sample-config",
        namespace="default",
    ),
    data={
        "message": "Hello from Pulumi Kubernetes Operator!",
        "environment": "staging",
        "created-by": "pulumi-operator",
        "version": "1.0.0",
    }
)

# Export the ConfigMap name and namespace
pulumi.export("configMapName", config_map.metadata["name"])
pulumi.export("configMapNamespace", config_map.metadata["namespace"])
