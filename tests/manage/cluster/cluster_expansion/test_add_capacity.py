import logging

from ocs_ci.framework.testlib import tier1, ManageTest
from ocs_ci.ocs import machine as machine_utils
from ocs_ci.ocs import constants, ocp
from ocs_ci.ocs.resources import pod


logger = logging.getLogger(__name__)


@tier1
class TestAddCapacity(ManageTest):
    def test_add_capacity(self):
        osd_count = pod.get_pod_count(label=constants.OSD_APP_LABEL)
        storage_cluster = machine_utils.get_storage_cluster()
        machine_utils.add_capacity(storagecluster_name=storage_cluster, count=osd_count + 3)
        pod_obj = ocp.OCP(kind=constants.POD)
        assert pod_obj.wait_for_resource(
            condition=constants.STATUS_RUNNING, selector=constants.OSD_APP_LABEL,
            resource_count=osd_count + 3, timeout=600
        )
