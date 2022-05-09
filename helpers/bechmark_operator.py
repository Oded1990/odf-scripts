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

    def wait_for_controller_to_running(self):
        if not wait_pods_status(
            namespace=constants.BENCHMARK_OPERATOR_NAMESPACE,
            pattern="controller",
            number_of_pods=1,
            expected_mode=constants.STATUS_RUNNING,
            sleep=10,
            timeout=60,
        ):
            logging(
                text=f"fio-server pod did not move to running state after {self.timeout_completed} sec",
                type="error",
            )
            out = send_cmd(
                cmd=f"oc get pods -n {constants.BENCHMARK_OPERATOR_NAMESPACE} |grep controller"
            )
            raise Exception(
                f"fio-server pod did not move to running state after {self.timeout_completed} sec {out}"
            )

    def wait_for_servers_to_running(self):
        if not wait_pods_status(
            namespace=constants.BENCHMARK_OPERATOR_NAMESPACE,
            pattern="server",
            number_of_pods=int(self.crd_data["spec"]["workload"]["args"]["servers"]),
            expected_mode=constants.STATUS_RUNNING,
            sleep=40,
            timeout=200,
        ):
            logging(
                text=f"fio-server pod did not move to running state after {self.timeout_completed} sec",
                type="error",
            )
            out = send_cmd(
                cmd=f"oc get pods -n {constants.BENCHMARK_OPERATOR_NAMESPACE} |grep server"
            )
            raise Exception(
                f"fio-server pod did not move to running state after {self.timeout_completed} sec {out}"
            )

    def wait_for_client_to_complete(self):
        if not wait_pods_status(
            namespace=constants.BENCHMARK_OPERATOR_NAMESPACE,
            pattern="client",
            number_of_pods=1,
            expected_mode=constants.STATUS_COMPLETED,
            sleep=10,
            timeout=self.timeout_completed,
        ):
            logging(
                text=f"fio-client pod did not move to running state after {self.timeout_completed} sec",
                type="error",
            )
            out = send_cmd(
                cmd=f"oc get pods -n {constants.BENCHMARK_OPERATOR_NAMESPACE} |grep client"
            )
            raise Exception(
                f"fio-client pod did not move to running state after {self.timeout_completed} sec {out}"
            )

    def run_fio_benchmark_operator(self):
        self.clone_benchmark_operator()
        self.deploy()
        self.wait_for_controller_to_running()
        self.create_benchmark_operator()
        self.wait_for_servers_to_running()
        self.wait_for_client_to_complete()

    def cleanup(self):
        """
        Clean up the cluster from the benchmark operator project
        """
        # Reset namespace to default
        send_cmd("oc project openshift-storage")
        logging("Delete the benchmark-operator project")
        run("make undeploy", shell=True, check=True, cwd=self.local_repo)
        time.sleep(10)
