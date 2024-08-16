import dataclasses
from datetime import timedelta
from typing import Any, List, Literal, Union, Optional
from launchflow import exceptions
from launchflow.gcp.artifact_registry_repository import (
    ArtifactRegistryRepository,
    RegistryFormat,
)
from launchflow.gcp.compute_engine import (
    AutoHealingPolicy,
    AutoscalingPolicy,
    CPUUtilization,
    HttpHealthCheck,
    NamedPort,
    RegionalAutoscaler,
    RegionalManagedInstanceGroup,
    UpdatePolicy,
)
from launchflow.gcp.custom_domain_mapping import CustomDomainMapping, GCEServiceBackend
from launchflow.gcp.networking import AllowRule, FirewallAllowRule
from launchflow.gcp.service import GCPService
from launchflow.models.enums import ServiceProduct
from launchflow.node import Inputs
from launchflow.resource import Resource
from launchflow.service import DNSOutputs, ServiceOutputs


@dataclasses.dataclass
class ComputeEngineServiceInputs(Inputs):
    machine_type: str
    disk_size_gb: int
    deploy_timeout_sec: float


class ComputeEngineService(GCPService):
    """A service hosted on GCP Compute Engine. This is managed with a mangaged instance group."""

    product = ServiceProduct.GCP_COMPUTE_ENGINE

    def __init__(
        self,
        name: str,
        # build inputs
        build_directory: str = ".",
        build_ignore: List[str] = [],
        dockerfile: str = "Dockerfile",
        # gce inputs
        machine_type: str = "e2-standard-2",
        port: int = 80,
        region: Optional[str] = None,
        disk_size_gb: int = 10,
        update_policy: UpdatePolicy = UpdatePolicy(max_surge_fixed=3),
        # health check inputs
        health_check: Optional[Union[Literal[False], HttpHealthCheck]] = None,
        auto_healing_policy_initial_delay: int = 360,
        # autoscaler
        auto_scaler: Optional[Union[Literal[False], RegionalAutoscaler]] = None,
        # custom domain
        domain: Optional[str] = None,
        # deploy configuraiton
        deploy_timeout: timedelta = timedelta(minutes=15),
    ):
        super().__init__(
            name=name,
            dockerfile=dockerfile,
            build_directory=build_directory,
            build_ignore=build_ignore,
        )
        self.machine_type = machine_type
        self.port = port
        self.region = region
        self.disk_size_gb = disk_size_gb

        auto_healing_policy = None
        if health_check is False:
            self._health_check = None
        elif health_check is None:
            self._health_check = HttpHealthCheck(f"{name}-health-check", port=port)
            auto_healing_policy = AutoHealingPolicy(
                health_check=self._health_check, initial_delay_sec=180
            )
        else:
            self._health_check = health_check
            auto_healing_policy = AutoHealingPolicy(
                health_check=self._health_check, initial_delay_sec=180
            )

        self._mig = RegionalManagedInstanceGroup(
            name,
            region=region,
            auto_healing_policy=auto_healing_policy,
            update_policy=update_policy,
            named_ports=[NamedPort("http", port)],
        )

        if auto_scaler is False:
            self._health_check = None
        elif auto_scaler is None:
            self._auto_scaler = RegionalAutoscaler(
                f"{name}-auto-scaler",
                group_manager=self._mig,
                autoscaling_policies=[
                    AutoscalingPolicy(
                        min_replicas=1,
                        max_replicas=10,
                        cooldown_period=360,
                        cpu_utilization=CPUUtilization(target=0.75),
                    )
                ],
            )
        else:
            self._auto_scaler = auto_scaler
        self._firewall_rule = FirewallAllowRule(
            name=f"{self.name}-allow",
            direction="INGRESS",
            allow_rules=[AllowRule(ports=[port], protocol="tcp")],
            target_tags=[self.name],
            source_ranges=["0.0.0.0/0"],
        )
        self._artifact_registry = ArtifactRegistryRepository(
            f"{name}-repository", format=RegistryFormat.DOCKER
        )
        self.deploy_timeout = deploy_timeout
        self._custom_domain = None
        self.domain = domain
        if self.domain:
            if self._health_check is None:
                raise ValueError("Health check must be provided to use a custom domain")
            self._custom_domain = CustomDomainMapping(
                name=f"{name}-domain-mapping",
                domain=self.domain,
                gce_service_backend=GCEServiceBackend(
                    self._mig, self._health_check, "http"
                ),
            )

    def resources(self) -> List[Resource]:
        resources: List[Resource[Any]] = [
            self._mig,
            self._firewall_rule,
            self._artifact_registry,
        ]
        # TODO: always including the health check causes it to show up twice in the plan
        # but if we don't include it then the update to the mig doesn't show up. For
        # now we just show it twice cause it's not the worst thing in the world
        if self._health_check is not None:
            resources.append(self._health_check)
        if self._auto_scaler is not None:
            resources.append(self._auto_scaler)
        if self._custom_domain is not None:
            resources.append(self._custom_domain)
        return resources

    def inputs(self, *args, **kwargs) -> Inputs:
        return ComputeEngineServiceInputs(
            machine_type=self.machine_type,
            deploy_timeout_sec=self.deploy_timeout.total_seconds(),
            disk_size_gb=self.disk_size_gb,
        )

    def outputs(self) -> ServiceOutputs:
        repo_outputs = self._artifact_registry.outputs()
        if repo_outputs.docker_repository is None:
            raise ValueError("Docker repository not found in artifact registry outputs")
        service_url = None
        dns_outputs = None
        if self._custom_domain is not None:
            service_url = f"https://{self._custom_domain.domain}"
            try:
                custom_domain_outputs = self._custom_domain.outputs()
            except exceptions.ResourceOutputsNotFound:
                raise exceptions.ServiceOutputsNotFound(service_name=self.name)
            dns_outputs = DNSOutputs(
                domain=custom_domain_outputs.registered_domain,
                ip_address=custom_domain_outputs.ip_address,
            )
        return ServiceOutputs(
            service_url=service_url,  # type: ignore
            docker_repository=repo_outputs.docker_repository,
            dns_outputs=dns_outputs,
        )
