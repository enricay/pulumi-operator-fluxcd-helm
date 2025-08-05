# Pulumi Operator Deployment for Stage

## Files Changed
- `clusters/stage/infrastructure.yaml` - Defines stage-specific Kustomization details.
- `infrastructure/stage/pulumi-operator/kustomization.yaml` - References base resources and applies patches.
- `infrastructure/stage/pulumi-operator/helmrelease-patch.yaml` - Contains stage-specific Helm release configurations.

## Deployment Status
- The `pulumi-operator` namespace is set up,and the deployment is successful (deployments, services, etc.) are currently active there.
- A Pulumi Access Token is required but not present in the `pulumi-operator` namespace.

## Next Steps
1. **Create Sample Stacks/Programs:**
   - Develop sample Pulumi stacks/programs to test the operator functionality.
   - Use the `Pulumi.yaml` and other configuration files as templates (eg python,typescript yaml to test)

2. **Deploying Pulumi Token:**
   - A Pulumi Access Token needs to be deployed to the `pulumi-operator` namespace to allow for creating and managing stacks.
   - You need to ask if the token should be provided manually or if you should automate the deployment.
   - Example command to deploy a Pulumi token secret:
     ```bash
     kubectl create secret generic pulumi-api-secret --from-literal=accessToken=<your-access-token> -n pulumi-operator
     ```

3. **Monitoring & Validation:**
   - Once deployed, validate the deployment through the HelmRelease and HelmRepository resources.
   - Monitor pod and HelmRelease events to ensure everything is functioning as expected.

