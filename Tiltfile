load('ext://helm_resource', 'helm_resource', 'helm_repo')
load('ext://namespace', 'namespace_yaml')

k8s_resource(
    workload='traefik-system',
    labels=['infra'],
    resource_deps=['traefik-repo']
)
k8s_yaml(namespace_yaml('traefik'), allow_duplicates=False)
helm_repo('traefik-repo', 'https://traefik.github.io/charts')
helm_resource(
    name='traefik-system',
    chart='traefik/traefik',
    deps=['traefik-repo'],
    namespace='traefik',
    flags=['--set', 'service.type=NodePort']
)

# Test deployment
k8s_yaml(
    [
        'src/apps/test/deployment.yaml',
        'src/apps/test/service.yaml',
        'src/apps/test/ingress.yaml',
    ]
)