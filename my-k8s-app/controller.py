import kopf
import kubernetes

@kopf.on.create('mycompany.com', 'v1', 'websites')
def create_fn(spec, name, namespace, logger, **kwargs):
    domain = spec.get('domain')
    image = spec.get('image')

    logger.info(f"Creating a Deployment for website '{name}' with image '{image}' and domain '{domain}'")

    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name},
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [{
                        "name": "web",
                        "image": image,
                        "ports": [{"containerPort": 80}]
                    }]
                }
            }
        }
    }

    k8s = kubernetes.client.AppsV1Api()
    k8s.create_namespaced_deployment(namespace=namespace, body=deployment)
