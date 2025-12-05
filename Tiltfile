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
    flags=[
        '--set',
        'service.type=NodePort',
        '--set',
        'ports.web.nodePort=30000',
    ]
)

k8s_yaml(namespace_yaml('redis'), allow_duplicates=False)
k8s_resource(
    workload='redis',
    labels=['infra'],
)
helm_resource(
    name='redis',
    chart='oci://registry-1.docker.io/cloudpirates/redis',
    namespace='redis'
)

k8s_resource(
    workload='postgresql',
    labels=['infra'],
    resource_deps=['postgresql-repo']
)
k8s_yaml(namespace_yaml('postgresql'), allow_duplicates=False)
k8s_yaml(['src/infra/postgres/configmap-ddl.yaml'])
helm_repo('postgresql-repo', 'https://groundhog2k.github.io/helm-charts')
helm_resource(
    name='postgresql',
    chart='postgresql-repo/postgres',
    deps=['postgresql-repo'],
    namespace='postgresql',
    flags=[
        "--set", "env[0].name=POSTGRES_PASSWORD",
        "--set", "env[0].value=Asdasd11",
        "--set", "extraScripts=db-recipe-init-scripts"
    ]
)

# Test deployment
k8s_yaml(
    [
        'src/apps/test/deployment.yaml',
        'src/apps/test/service.yaml',
        'src/apps/test/ingress.yaml',
    ]
)

k8s_resource(
    workload='skalazhato',
    labels=['apps'],
    resource_deps=['postgresql', 'redis', 'traefik-system']
)
k8s_yaml(namespace_yaml('skalazhato'), allow_duplicates=False)
docker_build(
    ref='recipe',
    context='src/apps/recipe-service',
)
helm_resource(
    name='skalazhato',
    chart='src/helm/skalazhato',
    namespace='skalazhato',
    image_deps=['recipe'],
    image_keys=[('recipeService.image.repository', 'recipeService.image.tag')],
)
