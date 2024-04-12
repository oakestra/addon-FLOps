import shlex

from flops_manager.utils.sla.components import SlaComponentsWrapper
from flops_manager.utils.types import AppSLA


def generate_sla(components: SlaComponentsWrapper) -> AppSLA:
    core = components.core
    names = core.names
    compute = core.compute

    details = components.details
    resources = details.resources

    sla = {
        "sla_version": "v2.0",
        "customerID": core.customerID,
        "applications": [
            {
                "applicationID": core.app_id,
                "application_name": names.app_name,
                "application_namespace": names.app_namespace,
                "application_desc": details.app_desc,
                "microservices": [],
            }
        ],
    }

    if compute:
        sla["applications"][0]["microservices"].append(
            {
                "microserviceID": "",
                "microservice_name": names.service_name,
                "microservice_namespace": names.service_namespace,
                "virtualization": "container",
                "one_shot": compute.one_shot_service,
                "cmd": ([] if (core.compute.cmd == "") else shlex.split(core.compute.cmd)),
                "memory": resources.memory,
                "vcpus": resources.vcpus,
                "storage": resources.storage,
                "code": compute.code,
                **({"addresses": {"rr_ip": details.rr_ip}} if details.rr_ip else {}),
            }
        )

    return sla
