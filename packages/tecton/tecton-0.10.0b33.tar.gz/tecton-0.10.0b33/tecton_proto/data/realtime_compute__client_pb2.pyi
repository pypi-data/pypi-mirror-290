from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class AWSComputeInstanceGroup(_message.Message):
    __slots__ = ["ami_image_id", "autoscaling_group_arn", "autoscaling_group_name", "health_check_path", "iam_instance_profile_arn", "instance_type", "launch_template_id", "port", "region", "security_group_ids", "subnet_ids"]
    AMI_IMAGE_ID_FIELD_NUMBER: ClassVar[int]
    AUTOSCALING_GROUP_ARN_FIELD_NUMBER: ClassVar[int]
    AUTOSCALING_GROUP_NAME_FIELD_NUMBER: ClassVar[int]
    HEALTH_CHECK_PATH_FIELD_NUMBER: ClassVar[int]
    IAM_INSTANCE_PROFILE_ARN_FIELD_NUMBER: ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: ClassVar[int]
    LAUNCH_TEMPLATE_ID_FIELD_NUMBER: ClassVar[int]
    PORT_FIELD_NUMBER: ClassVar[int]
    REGION_FIELD_NUMBER: ClassVar[int]
    SECURITY_GROUP_IDS_FIELD_NUMBER: ClassVar[int]
    SUBNET_IDS_FIELD_NUMBER: ClassVar[int]
    ami_image_id: str
    autoscaling_group_arn: str
    autoscaling_group_name: str
    health_check_path: str
    iam_instance_profile_arn: str
    instance_type: str
    launch_template_id: str
    port: int
    region: str
    security_group_ids: _containers.RepeatedScalarFieldContainer[str]
    subnet_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, autoscaling_group_arn: Optional[str] = ..., autoscaling_group_name: Optional[str] = ..., region: Optional[str] = ..., port: Optional[int] = ..., health_check_path: Optional[str] = ..., instance_type: Optional[str] = ..., ami_image_id: Optional[str] = ..., iam_instance_profile_arn: Optional[str] = ..., security_group_ids: Optional[Iterable[str]] = ..., subnet_ids: Optional[Iterable[str]] = ..., launch_template_id: Optional[str] = ...) -> None: ...

class AWSTargetGroup(_message.Message):
    __slots__ = ["arn", "compute_instance_group", "name"]
    ARN_FIELD_NUMBER: ClassVar[int]
    COMPUTE_INSTANCE_GROUP_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    arn: str
    compute_instance_group: AWSComputeInstanceGroup
    name: str
    def __init__(self, arn: Optional[str] = ..., name: Optional[str] = ..., compute_instance_group: Optional[Union[AWSComputeInstanceGroup, Mapping]] = ...) -> None: ...

class ColocatedComputeConfig(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GoogleCloudBackendService(_message.Message):
    __slots__ = ["compute_instance_group", "project", "region", "target_id"]
    COMPUTE_INSTANCE_GROUP_FIELD_NUMBER: ClassVar[int]
    PROJECT_FIELD_NUMBER: ClassVar[int]
    REGION_FIELD_NUMBER: ClassVar[int]
    TARGET_ID_FIELD_NUMBER: ClassVar[int]
    compute_instance_group: GoogleCloudComputeInstanceGroup
    project: str
    region: str
    target_id: str
    def __init__(self, target_id: Optional[str] = ..., project: Optional[str] = ..., region: Optional[str] = ..., compute_instance_group: Optional[Union[GoogleCloudComputeInstanceGroup, Mapping]] = ...) -> None: ...

class GoogleCloudComputeInstanceGroup(_message.Message):
    __slots__ = ["project", "region", "target_id"]
    PROJECT_FIELD_NUMBER: ClassVar[int]
    REGION_FIELD_NUMBER: ClassVar[int]
    TARGET_ID_FIELD_NUMBER: ClassVar[int]
    project: str
    region: str
    target_id: str
    def __init__(self, project: Optional[str] = ..., region: Optional[str] = ..., target_id: Optional[str] = ...) -> None: ...

class LoadBalancerTarget(_message.Message):
    __slots__ = ["aws_target_group", "google_backend_service"]
    AWS_TARGET_GROUP_FIELD_NUMBER: ClassVar[int]
    GOOGLE_BACKEND_SERVICE_FIELD_NUMBER: ClassVar[int]
    aws_target_group: AWSTargetGroup
    google_backend_service: GoogleCloudBackendService
    def __init__(self, aws_target_group: Optional[Union[AWSTargetGroup, Mapping]] = ..., google_backend_service: Optional[Union[GoogleCloudBackendService, Mapping]] = ...) -> None: ...

class OnlineComputeConfig(_message.Message):
    __slots__ = ["aws_compute_instance_group", "colocated_compute", "google_compute_instance_group", "remote_compute"]
    AWS_COMPUTE_INSTANCE_GROUP_FIELD_NUMBER: ClassVar[int]
    COLOCATED_COMPUTE_FIELD_NUMBER: ClassVar[int]
    GOOGLE_COMPUTE_INSTANCE_GROUP_FIELD_NUMBER: ClassVar[int]
    REMOTE_COMPUTE_FIELD_NUMBER: ClassVar[int]
    aws_compute_instance_group: AWSComputeInstanceGroup
    colocated_compute: ColocatedComputeConfig
    google_compute_instance_group: GoogleCloudComputeInstanceGroup
    remote_compute: RemoteFunctionComputeConfig
    def __init__(self, colocated_compute: Optional[Union[ColocatedComputeConfig, Mapping]] = ..., remote_compute: Optional[Union[RemoteFunctionComputeConfig, Mapping]] = ..., aws_compute_instance_group: Optional[Union[AWSComputeInstanceGroup, Mapping]] = ..., google_compute_instance_group: Optional[Union[GoogleCloudComputeInstanceGroup, Mapping]] = ...) -> None: ...

class RemoteFunctionComputeConfig(_message.Message):
    __slots__ = ["function_uri", "id", "name"]
    FUNCTION_URI_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    function_uri: str
    id: str
    name: str
    def __init__(self, id: Optional[str] = ..., name: Optional[str] = ..., function_uri: Optional[str] = ...) -> None: ...
