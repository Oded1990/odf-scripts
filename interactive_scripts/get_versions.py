import logging
import sys

from interactive_scripts import helpers

log = logging.getLogger()
log.setLevel(logging.DEBUG)
stream = logging.StreamHandler(sys.stdout)

if __name__ == "__main__":
    ocp_version = helpers.get_ocp_version()
    ocs_version = helpers.get_ocs_version()
    ceph_version = helpers.get_ceph_versions()
    log.info(
        f"ocp_version:{ocp_version}"
        f"\nocs_version:{ocs_version}"
        f"\nceph_version:{ceph_version}"
    )
