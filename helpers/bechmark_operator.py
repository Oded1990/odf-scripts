import time
import git
import tempfile
from subprocess import run

from infra_cmd.infra_cmd import logging, send_cmd
from helpers import constants
from infra_cmd.infra_cmd import yaml_to_dict, dict_to_yaml
from helpers.helpers import wait_pods_status


class BenchmarkOperatorFIO(object):
    def __init__(
        self,
        jobs="read",
        read_runtime=30,
        bs="4096KiB",
        storageclass=constants.DEFAULT_STORAGECLASS_RBD,
        file_size=1,
        pvc_size=2,
        servers=2,
        timeout_completed=500,
    ):
        self.timeout_completed = timeout_completed
        self.local_repo = tempfile.mkdtemp()
        self.crd_data = yaml_to_dict("configurations/benchmark_fio.yaml")
        self.crd_data["spec"]["workload"]["args"]["jobs"] = jobs
        self.crd_data["spec"]["workload"]["args"]["samples"] = 1
        self.crd_data["spec"]["workload"]["args"]["read_runtime"] = read_runtime
        self.crd_data["spec"]["workload"]["args"]["bs"] = bs
        self.crd_data["spec"]["workload"]["args"]["storageclass"] = storageclass
        self.crd_data["spec"]["workload"]["args"]["filesize"] = f"{file_size}GiB"
        self.crd_data["spec"]["workload"]["args"]["storagesize"] = f"{pvc_size}Gi"
        self.crd_data["spec"]["workload"]["args"]["servers"] = servers

    def clone_benchmark_operator(self):
        logging(text=f"clone {constants.BMO_REPO} to {self.local_repo}")
        git.Repo.clone_from(constants.BMO_REPO, self.local_repo)

    def deploy(self):
        """
        Deploy the benchmark-operator
        """
        run("make deploy", shell=True, check=True, cwd=self.local_repo)

    def create_benchmark_operator(self):
        benchmark_yaml = dict_to_yaml(self.crd_data)
        send_cmd(
            cmd=f"oc -n {constants.BENCHMARK_OPERATOR_NAMESPACE} create -f {benchmark_yaml} -o yaml",
            print_cmd=True,
        )

    def wait_for_wl_to_complete(self):
        if not wait_pods_status(
            namespace=constants.BENCHMARK_OPERATOR_NAMESPACE,
            pattern="client",
            number_of_pods=1,
            expected_mode=constants.STATUS_COMPLETED,
            sleep=40,
            timeout=self.timeout_completed,
        ):
            logging(
                text=f"fio-client pod did not move to running state after {self.timeout_completed} sec",
                type="error",
            )
            raise Exception(
                f"fio-client pod did not move to running state after {self.timeout_completed} sec"
            )

    def run_fio_benchmark_operator(self):
        self.clone_benchmark_operator()
        self.deploy()
        self.create_benchmark_operator()
        self.wait_for_wl_to_complete()

    def cleanup(self):
        """
        Clean up the cluster from the benchmark operator project
        """
        # Reset namespace to default
        send_cmd("oc project openshift-storage")
        logging("Delete the benchmark-operator project")
        run("make undeploy", shell=True, check=True, cwd=self.local_repo)
        time.sleep(10)
