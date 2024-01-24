from os import environ, getuid, getgid
from logging import getLogger
from dataclasses import dataclass
from typing import ClassVar
from functools import cached_property
from os.path import (
    join,
    abspath,
    dirname,
    relpath as relative_path,
)

from omniblack.repo import Package, PkgKind, LibKind

from .kube import (
    Container,
    ContainerPort,
    ContainerSecurityContext,
    DeploymentSpec,
    EnvVar,
    HostPath,
    JobSpec,
    KubeMetadata,
    KubeObject,
    KubeObjectKind,
    KubeSelector,
    PathTypes,
    PodSecurityContext,
    PodSpec,
    PodTemplate,
    ReplacementStrategy,
    ReplacementStrategyTypes,
    RestartPolicy,
    ServicePort,
    ServiceSpec,
    TemplateMetadata,
    Volume,
    VolumeMount,
)

from omniblack.caddy import (
    MatcherList,
    PathMatcher,
    RewriteHandler,
    Route,
    VarsHandler,
    ReverseProxyHandler,
    Upstream,
    add_standard_headers,
)

log = getLogger(__name__)

PORT = int(environ.get('PORT', 3000))

next_range_start = PORT + 10


def next_range():
    global next_range_start

    range_start = next_range_start
    next_range_start += 10

    return range(range_start, next_range_start)


class DevPackage(Package):
    def create_dev_configs(self):
        for lang in self.languages:
            if lang in Config.lang_configs:
                yield Config(self, lang)


@dataclass
class Config:
    lang_configs: ClassVar = {}
    pkg: DevPackage
    lang: str

    def __new__(cls, pkg, lang):
        cls = cls.lang_configs[lang]
        return super().__new__(cls)

    def __post_init__(self, *args, **kwargs):
        if hasattr(self, 'assign_ports'):
            self.port_range = iter(next_range())
            self.assign_ports()

    def __init_subclass__(cls, lang):
        Config.lang_configs[lang] = cls

    @property
    def base_image_name(self):
        rel_path = relative_path(self.pkg.path, self.pkg.root_dir)
        return rel_path.replace('/', '_').replace('.', '_').lower()

    def image_name(self, task=None):
        image_name = self.base_image_name

        if task is not None:
            image_name += '_' + task

        return image_name

    def resource_name(self, task=None):
        resource_name = self.base_image_name

        if task is not None:
            resource_name += '-' + task

        resource_name = resource_name.replace('_', '-')
        return resource_name

    def create_volume_mounts(self):
        return [
            VolumeMount(
                mountPath=self.pkg.root_dir,
                name='source-code',
                readOnly=False,
            ),
            VolumeMount(
                mountPath='/etc/localtime',
                name='localtime',
                readOnly=True,
            ),
        ]

    def create_volumes(self):
        return [
            Volume(
                name='source-code',
                hostPath=HostPath(
                    path=self.pkg.root_dir,
                    type=PathTypes.directory
                ),
            ),
            Volume(
                name='localtime',
                hostPath=HostPath(
                    path='/etc/localtime',
                    type=PathTypes.file,
                ),
            ),
        ]

    def to_yaml_env(self, env):
        return [
            EnvVar(name=name, value=str(value))
            for name, value in env.items()
        ]

    def pod_spec(self, restart_policy, containers):
        return PodSpec(
            restartPolicy=restart_policy,
            backoffLimit=0,
            workingDir=self.pkg.path,
            volumes=self.create_volumes(),
            containers=containers,
            securityContext=PodSecurityContext(
                runAsUser=getuid(),
                runAsGroup=getgid(),
            ),
        )

    def create_kube_object(self, task, kube_kind, sub_spec):
        match kube_kind:
            case KubeObjectKind.job:
                api_version = 'batch/v1'
            case KubeObjectKind.deployment:
                api_version = 'apps/v1'
            case KubeObjectKind.service:
                api_version = 'v1'

        return KubeObject(
            apiVersion=api_version,
            kind=kube_kind,
            metadata=KubeMetadata(
                name=self.resource_name(task),
            ),
            spec=sub_spec,
        )

    def container(self, task, env, command, port=None):
        ports = []

        if port is not None:
            ports.append(ContainerPort(containerPort=port))

        return Container(
            image=self.image_name(task),
            name=self.resource_name(task),
            command=command,
            env=env,
            workingDir=self.pkg.path,
            volumeMounts=self.create_volume_mounts(),
            securityContext=ContainerSecurityContext(
                allowPrivilegeEscalation=False,
            ),
            ports=ports,
        )

    def job(self, name, env, command):
        task = f'{self.lang }_{name}'
        cont = self.container(task, env, command)
        pod_spec = self.pod_spec(RestartPolicy.never, [cont])
        metadata = TemplateMetadata(labels=dict(app=self.resource_name(task)))

        pod_template = PodTemplate(
            spec=pod_spec,
            metadata=metadata,
        )

        job = JobSpec(backoffLimit=0, template=pod_template)

        return self.create_kube_object(task, KubeObjectKind.job, job)

    def deployment(self, name, env, command, port=None):
        task = f'{self.lang}_{name}'

        cont = self.container(task, env, command, port=port)
        pod_spec = self.pod_spec(RestartPolicy.always, [cont])
        metadata = TemplateMetadata(labels=dict(app=self.resource_name(task)))

        pod_template = PodTemplate(
            spec=pod_spec,
            metadata=metadata,
        )

        deployment = DeploymentSpec(
            replicas=1,
            template=pod_template,
            strategy=ReplacementStrategy(
                type=ReplacementStrategyTypes.recreate,
            ),
            selector=KubeSelector(
                matchLabels=dict(app=self.resource_name(task)),
            ),
        )

        return self.create_kube_object(
            task,
            KubeObjectKind.deployment,
            deployment,
        )

    def service(self, name, ports):
        task = f'{self.lang}_{name}'

        ports = [
            ServicePort(name=name, port=port)
            for name, port in ports.items()
        ]

        service = ServiceSpec(
            selector=dict(app=self.resource_name(task)),
            ports=ports,
        )

        return self.create_kube_object(
            task,
            KubeObjectKind.service,
            service,
        )

    @cached_property
    def public_path(self):
        if 'public_path' not in self.pkg.config:
            return None

        public_path = self.pkg.config.public_path

        if not public_path.startswith('/'):
            return '/' + public_path

        return public_path


class JsConfig(Config, lang='js'):
    def assign_ports(self):
        self.reload_port = next(self.port_range)
        self.debug_port = next(self.port_range)

    def is_spa(self):
        is_comp_lib = False

        if self.pkg.config.type == PkgKind.lib:
            is_comp_lib = LibKind.svelte is self.pkg.config.lib_type

        return self.pkg.config.type == PkgKind.spa or is_comp_lib

    @property
    def pnpm_store(self):
        SRC = self.pkg.root_dir
        return abspath(join(SRC, '../.pnpm-store'))

    def create_volume_mounts(self):
        mounts = super().create_volume_mounts()
        mounts.append(VolumeMount(
            mountPath=self.pnpm_store,
            name='pnpm-store',
            readOnly=False,
        ))

        return mounts

    def create_volumes(self):
        volumes = super().create_volumes()
        volumes.append(Volume(
            name='pnpm-store',
            hostPath=HostPath(
                path=self.pnpm_store,
                type=PathTypes.directory,
            ),
        ))

        return volumes

    def js_env(self):
        return self.pkg.proc_env | dict(
            CONFIG_PATH=self.pkg.config_path,
            DEBUG_PORT=str(self.debug_port),
            FORCE_COLOR='3',
            JS_PATH=self.pkg.js.path,
            NODE_OPTIONS='--experimental-import-meta-resolve',
            PKG_PATH=self.pkg.path,
            RELOAD_PORT=str(self.reload_port),
        )

    def image_names(self):
        image_names = []

        pkg_json = self.pkg.js.manifest

        scripts = pkg_json.get('scripts', {})

        if 'test' in scripts:
            image_names.append(self.image_name('js_test'))

        if self.is_spa():
            image_names.append(self.image_name('js_spa'))

        return image_names

    def resources(self):
        resources = []

        pkg_json = self.pkg.js.manifest

        scripts = pkg_json.get('scripts', {})

        if 'test' in scripts:
            resources.append(
                dict(
                    name=self.resource_name('js_test'),
                    labels=['y-Test'],
                ),
            )

        if self.is_spa():
            resources.append(
                dict(
                    name=self.resource_name('js_spa'),
                    labels=['x-SPA'],
                ),
            )

        return resources

    def create_kube_objects(self):
        objects = []

        pkg_json = self.pkg.js.manifest
        scripts = pkg_json.get('scripts', {})

        if 'test' in scripts:
            objects.append(self.job(
                'test',
                self.to_yaml_env(self.js_env()),
                ['pnpm', 'run', 'test'],
            ))

        if self.is_spa():
            objects.append(self.deployment(
                'spa',
                self.to_yaml_env(self.js_env()),
                [
                    'node',
                    '--unhandled-rejections=strict',
                    join(dirname(__file__), 'dev.js'),
                ],
            ))

        return objects

    def routes(self):
        routes = [
            self.spa_route(),
        ]

        return [
            route
            for route in routes
            if route is not None
        ]

    def spa_route(self):
        if not self.is_spa():
            return None

        vars_handler = VarsHandler()
        vars_handler.vars['path_prefix'] = self.public_path
        vars_handler.vars['root'] = self.pkg.resolve_path(
            self.pkg.config.output_dir,
        )

        matcher = PathMatcher(f'{self.public_path}/*', self.public_path)
        match = MatcherList(matcher)

        return Route(
            handle=[vars_handler],
            match=match,
            group='static_files',

        )


class PyConfig(Config, lang='py'):
    def assign_ports(self):
        self.server_port = 8000

    def resources(self):
        resources = []

        if self.pkg.config.type == PkgKind.server:
            resources.append(
                dict(
                    name=self.resource_name('py_server'),
                    labels=['v-Server'],
                ),
            )

        return resources

    def image_names(self):
        image_names = []

        if self.pkg.config.type == PkgKind.server:
            image_names.append(self.image_name('py_server'))

        return image_names

    def create_kube_objects(self):
        objects = []

        if self.pkg.config.type == PkgKind.server:
            mod_name = self.pkg.py.manifest['project']['name']

            objects.append(self.deployment(
                'server',
                self.to_yaml_env(self.pkg.proc_env),
                [
                    'gunicorn',
                    '--bind', f'0.0.0.0:{self.server_port}',
                    f'{mod_name}:app',
                ],
                self.server_port,
            ))

            objects.append(
                self.service('server', dict(primary=self.server_port)),
            )

        return objects

    def server_route(self):
        if self.pkg.config.type != PkgKind.server or not self.public_path:
            return None

        resource_name = self.resource_name('py-server')
        upstream = f'{resource_name}:{self.server_port}'
        proxy = ReverseProxyHandler(
            upstreams=[
                Upstream(dial=upstream),
            ],
        )

        add_standard_headers(proxy.headers)

        matcher = PathMatcher(f'{self.public_path}/*', self.public_path)

        return Route(
            match=MatcherList(matcher),
            handle=[
                RewriteHandler(strip_path_prefix=self.public_path),
                proxy,
            ],
        )

    def routes(self):
        routes = [
            self.server_route()
        ]

        return [
            route
            for route in routes
            if route is not None
        ]
