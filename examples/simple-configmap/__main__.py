import pulumi
from pulumi_kubernetes.core.v1 import ConfigMap, Namespace

# Create a simple ConfigMap
config_map = ConfigMap(
    "sample-configmap",
    metadata={
        "name": "sample-config",
        "namespace": "default",
    },
    data={
        "message": "Hello from Pulumi Kubernetes Operator!",
        "environment": "staging",
        "created-by": "pulumi-operator",
        "version": "1.0.1",
        "test-time": "2025-08-04T21:30:00Z"
    }
)

# Create Namespace
namespace = Namespace(
    "sample-ns",
    metadata={
        "name": "default",
    }
)

# Export the ConfigMap name and namespace
pulumi.export("configMapName", config_map.metadata["name"])
pulumi.export("configMapNamespace", config_map.metadata["namespace"])
