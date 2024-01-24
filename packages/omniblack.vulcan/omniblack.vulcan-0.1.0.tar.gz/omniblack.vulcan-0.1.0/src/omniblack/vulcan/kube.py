from pydantic import BaseModel
from omniblack.utils import Enum


class EnvVar(BaseModel):
    name: str
    value: str


class VolumeMount(BaseModel):
    name: str
    mountPath: str
    readOnly: bool


class PortProtocol(Enum):
    TCP = 'TCP'
    UDP = 'UDP'
    SCTP = 'SCTP'


class ContainerPort(BaseModel):
    containerPort: int
    hostIP: str | None = None
    hostPort: int | None = None
    name: str | None = None
    protocol: PortProtocol = PortProtocol.TCP


class PathTypes(Enum):
    directory_or_create = 'DirectoryOrCreate'
    directory = 'Directory'
    file_or_create = 'FileOrCreate'
    file = 'File'
    socket = 'Socket'
    char_device = 'CharDevice'
    block_device = 'BlockDevice'


class HostPath(BaseModel):
    path: str
    type: PathTypes


class Volume(BaseModel):
    name: str
    hostPath: HostPath


class ContainerSecurityContext(BaseModel):
    allowPrivilegeEscalation: bool


class Container(BaseModel):
    name: str
    image: str
    command: list[str] = None
    env: list[EnvVar] = None
    securityContext: ContainerSecurityContext = None
    volumeMounts: list[VolumeMount] = None
    workingDir: str = None
    ports: list[ContainerPort] = None


class PodSecurityContext(BaseModel):
    runAsUser: int
    runAsGroup: int


class RestartPolicy(Enum):
    always = 'Always'
    on_failure = 'OnFailure'
    never = 'Never'


class PodSpec(BaseModel):
    securityContext: PodSecurityContext
    restartPolicy: RestartPolicy
    backoffLimit: int
    workingDir: str
    volumes: list[Volume]
    containers: list[Container]


class TemplateMetadata(BaseModel):
    labels: dict[str, str]


class PodTemplate(BaseModel):
    metadata: TemplateMetadata
    spec: PodSpec


class KubeMetadata(BaseModel):
    name: str


class KubeObjectKind(Enum):
    deployment = 'Deployment'
    job = 'Job'
    service = 'Service'


class KubeSelector(BaseModel):
    matchLabels: dict[str, str]


class ReplacementStrategyTypes(Enum):
    recreate = 'Recreate'
    rolling_update = 'RollingUpdate'


class ReplacementStrategy(BaseModel):
    type: ReplacementStrategyTypes


class DeploymentSpec(BaseModel):
    replicas: int
    selector: KubeSelector
    strategy: ReplacementStrategy
    template: PodTemplate


class JobSpec(BaseModel):
    backoffLimit: int
    template: PodTemplate


class ServicePort(BaseModel):
    port: int
    name: str = None
    targetPort: int = None
    protocol: PortProtocol = None
    nodePort: int = None
    appProtocol: str = None


class ServiceType(Enum):
    cluster_ip = 'ClusterIp'
    node_port = 'NodePort'
    load_balancer = 'LoadBalancer'


class ServiceSpec(BaseModel):
    selector: dict[str, str]
    ports: list[ServicePort]
    type: ServiceType = None


class KubeObject(BaseModel):
    kind: KubeObjectKind
    apiVersion: str
    metadata: KubeMetadata
    spec: DeploymentSpec | JobSpec | ServiceSpec
