import logging
import sys
import subprocess
import time

from helpers import constants
from infra_cmd.infra_cmd import (
    yaml_to_dict,
    dict_to_yaml,
    send_cmd,
    wait_expected_result,
)

log = logging.getLogger()
log.setLevel(logging.DEBUG)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log.addHandler(stream)


def input_string(string_text, default_value, expected_string=()):
    while True:
        string_var = str(input(f"{string_text} ({default_value}): ") or default_value)
        string_var = string_var.replace(" ", "")
        if string_var in expected_string or len(expected_string) == 0:
            return string_var


def create_new_prject():
    project_name = input_string(
        string_text="Enter project name expected ",
        default_value="fio-project",
    )
    send_cmd(f"oc new-project {project_name}")
    return project_name


def create_pvc(project_name=None):
    pvc_name = str(input("Enter pvc name (pvc-test) : ") or "pvc-test")
    pvc_mode_number = str(
        input(
            "Choose pvc access Mode (RWO)\n"
            "1.ACCESS_MODE_RWO\n"
            "2.ACCESS_MODE_ROX\n"
            "3.ACCESS_MODE_RWX\n"
            "Choose pvc access Mode:"
        )
        or "1"
    )
    if pvc_mode_number == "1":
        pvc_mode = "ReadWriteOnce"
    elif pvc_mode_number == "2":
        pvc_mode = "ReadOnlyMany"
    elif pvc_mode_number == "3":
        pvc_mode = "ReadWriteMany"
    pvc_capacity_number = str(
        input("Enter pvc capacity [only number] in Gi (5Gi) : ") or "5"
    )
    pvc_capacity = f"{pvc_capacity_number}Gi"
    storage_class_name_number = str(
        input(
            "Choose storageclass name or write the sc name "
            "(ocs-storagecluster-ceph-rbd)\n"
            "1.ocs-storagecluster-ceph-rbd\n"
            "2.ocs-storagecluster-cephfs\n"
            "other[write storage class name]\n"
            "Choose storage class name:"
        )
        or "1"
    )
    if storage_class_name_number == "1":
        storage_class_name = "ocs-storagecluster-ceph-rbd"
    elif storage_class_name_number == "2":
        storage_class_name = "ocs-storagecluster-cephfs"
    else:
        storage_class_name = storage_class_name_number

    pvc_dic = yaml_to_dict("configurations/pvc.yaml")
    pvc_dic["metadata"]["name"] = pvc_name
    pvc_dic["metadata"]["namespace"] = project_name
    pvc_dic["spec"]["accessModes"] = [pvc_mode]
    pvc_dic["spec"]["storageClassName"] = storage_class_name
    pvc_dic["spec"]["resources"]["requests"]["storage"] = pvc_capacity
    pvc_yaml = dict_to_yaml(pvc_dic)
    cmd = f"oc -n {project_name} create -f {pvc_yaml} -o yaml"
    send_cmd(cmd=cmd)
    cmd = f"oc -n {project_name} get pvc {pvc_name}"
    wait_expected_result(
        sleep=3,
        timeout=30,
        cmd=cmd,
        expected_string="Bound",
        expected_error=f"pvc {pvc_name} does not on Bound state",
    )
    return pvc_name


def create_pvc_interactive():
    pvc_name = str(input("Enter pvc name (pvc-test) : ") or "pvc-test")
    pvc_mode_number = str(
        input(
            "Choose pvc access Mode (RWO)\n"
            "1.ACCESS_MODE_RWO\n"
            "2.ACCESS_MODE_ROX\n"
            "3.ACCESS_MODE_RWX\n"
            "Choose pvc access Mode:"
        )
        or "1"
    )
    if pvc_mode_number == "1":
        pvc_mode = "ReadWriteOnce"
    elif pvc_mode_number == "2":
        pvc_mode = "ReadOnlyMany"
    else:
        pvc_mode = "ReadWriteMany"
    pvc_capacity_number = str(
        input("Enter pvc capacity [only number] in Gi (5Gi) : ") or "5"
    )
    pvc_capacity = f"{pvc_capacity_number}Gi"
    storage_class_name_number = str(
        input(
            "Choose storageclass name or write the sc name "
            "(ocs-storagecluster-ceph-rbd)\n"
            "1.ocs-storagecluster-ceph-rbd\n"
            "2.ocs-storagecluster-cephfs\n"
            "other[write storage class name]\n"
            "Choose storage class name:"
        )
        or "1"
    )
    if storage_class_name_number == "1":
        storage_class_name = "ocs-storagecluster-ceph-rbd"
    elif storage_class_name_number == "2":
        storage_class_name = "ocs-storagecluster-cephfs"
    else:
        storage_class_name = storage_class_name_number
    return pvc_name, pvc_mode, pvc_capacity, storage_class_name


def create_multiple_pvc(project_name=None):
    pvc_name = str(input("Enter pvc name (pvc-test) : ") or "pvc-test")
    pvc_mode_number = str(
        input(
            "Choose pvc access Mode (RWO)\n"
            "1.ACCESS_MODE_RWO\n"
            "2.ACCESS_MODE_ROX\n"
            "3.ACCESS_MODE_RWX\n"
            "Choose pvc access Mode:"
        )
        or "1"
    )
    if pvc_mode_number == "1":
        pvc_mode = "ReadWriteOnce"
    elif pvc_mode_number == "2":
        pvc_mode = "ReadOnlyMany"
    else:
        pvc_mode = "ReadWriteMany"
    pvc_capacity_number = str(
        input("Enter pvc capacity [only number] in Gi (5Gi) : ") or "5"
    )
    pvc_capacity = f"{pvc_capacity_number}Gi"
    storage_class_name_number = str(
        input(
            "Choose storageclass name or write the sc name "
            "(ocs-storagecluster-ceph-rbd)\n"
            "1.ocs-storagecluster-ceph-rbd\n"
            "2.ocs-storagecluster-cephfs\n"
            "other[write storage class name]\n"
            "Choose storage class name:"
        )
        or "1"
    )
    if storage_class_name_number == "1":
        storage_class_name = "ocs-storagecluster-ceph-rbd"
    elif storage_class_name_number == "2":
        storage_class_name = "ocs-storagecluster-cephfs"
    else:
        storage_class_name = storage_class_name_number

    pvc_dic = yaml_to_dict("configurations/pvc.yaml")
    pvc_dic["metadata"]["name"] = pvc_name
    pvc_dic["metadata"]["namespace"] = project_name
    pvc_dic["spec"]["accessModes"] = [pvc_mode]
    pvc_dic["spec"]["storageClassName"] = storage_class_name
    pvc_dic["spec"]["resources"]["requests"]["storage"] = pvc_capacity
    pvc_yaml = dict_to_yaml(pvc_dic)
    cmd = f"oc -n {project_name} create -f {pvc_yaml} -o yaml"
    send_cmd(cmd=cmd)
    cmd = f"oc -n {project_name} get pvc {pvc_name}"
    wait_expected_result(
        sleep=3,
        timeout=30,
        cmd=cmd,
        expected_string="Bound",
        expected_error=f"pvc {pvc_name} does not on Bound state",
    )
    return pvc_name


def create_pref_pod(project_name, pvc_name):
    pod_name = str(input("Enter pod name (pod-test) : ") or "pod-test")
    pod_dic = yaml_to_dict("configurations/perf_pod.yaml")
    pod_dic["metadata"]["namespace"] = project_name
    pod_dic["spec"]["volumes"][0]["persistentVolumeClaim"]["claimName"] = pvc_name
    pod_dic["metadata"]["name"] = pod_name
    pod_yaml = dict_to_yaml(pod_dic)
    cmd = f"oc -n {project_name} create -f {pod_yaml} -o yaml"
    send_cmd(cmd=cmd)
    cmd = f"oc -n {project_name} get pods {pod_name}"
    wait_expected_result(
        sleep=7,
        timeout=100,
        cmd=cmd,
        expected_string="Running",
        expected_error=f"pod {pod_name} does not on Running state",
    )
    return pod_name


def run_fio(project_name, pod_name):
    rw_mode = str(input("Enter readwrite mode (randrw) : ") or "randrw")
    block_size_number = str(input("Enter block size [only number in K] (4K) : ") or "4")
    block_size = f"{block_size_number}K"
    jobs_num = str(input("Enter number of jobs [only number] (1) : ") or "1")
    run_time = str(input("Enter runtime (100 sec) [only number] : ") or "100")
    file_size_number = str(input("Enter file size (2GB) [only number] : ") or "2")
    file_size = f"{file_size_number}GB"
    is_verify = str(input("Add verify flag? (Yes/No): ") or "Yes")
    verify = "--verify=crc32c" if "y" in is_verify.lower() else ""
    cmd = (
        f"oc -n {project_name} rsh {pod_name} fio --name=fio-rand-readwrite --filename=/mnt/fio-rand-readwrite "
        f"--readwrite={rw_mode} --bs={block_size} --direct=0 --numjobs={jobs_num}"
        f" --time_based=1 --runtime={run_time} --size={file_size} --iodepth=4 --invalidate=1 --fsync_on_close=1 "
        f"--rwmixread=75 --ioengine=libaio {verify} --output-format=json"
    )
    send_cmd(cmd=cmd, print_cmd=True)
    return pod_name


def delete_pod(project_name, pod_name):
    cmd = f"oc delete pod {pod_name} -n {project_name} --force"
    send_cmd(cmd=cmd, print_cmd=True)


def delete_pvc(project_name, pvc_name):
    cmd = f"oc delete pvc {pvc_name} -n {project_name}"
    send_cmd(cmd=cmd, print_cmd=True)


def delete_project(project_name):
    cmd = f"oc delete project {project_name}"
    send_cmd(cmd=cmd, print_cmd=True)


def get_ocp_version():
    cmd = f"oc version"
    version_output = send_cmd(cmd=cmd, print_cmd=True)
    return version_output.splitlines()[1]


def get_ocs_version():
    cmd = f"oc describe csv odf-operator.v4.10.0 -n openshift-storage | grep full_version="
    version_output = send_cmd(cmd=cmd, print_cmd=True)
    return version_output.split()[1]


def get_ceph_tool_pod_name():
    cmd = f"oc get pods -n openshift-storage | grep rook-ceph-tools-"
    tool_pod = send_cmd(cmd=cmd, print_cmd=True)
    return tool_pod.split()[0]


def get_ceph_versions():
    tool_pod_name = get_ceph_tool_pod_name()
    cmd = f"oc rsh -n openshift-storage {tool_pod_name} ceph versions"
    return send_cmd(cmd=cmd, print_cmd=True)


def get_worker_node_names():
    cmd = "oc get nodes | grep worker | awk '{print $1}'"
    workers = send_cmd(cmd=cmd, print_cmd=False)
    f = filter(None, workers.split("\n"))
    return list(f)


def wait_pods_status(
    namespace=constants.OPENSHIFT_STORAGE_NAMESPACE,
    pattern="",
    number_of_pods=1,
    expected_mode=constants.STATUS_RUNNING,
    sleep=20,
    timeout=120,
):
    while timeout > 0:
        if len(pattern) > 0:
            output = subprocess.run(
                f"oc get pods -n {namespace} |grep {pattern}",
                shell=True,
                check=False,
                stdout=subprocess.PIPE,
            )
        else:
            output = subprocess.run(
                f"oc get pods -n {namespace}",
                shell=True,
                check=False,
                stdout=subprocess.PIPE,
            )

        output_str = str(output.stdout)
        if number_of_pods == count_freq(pat=expected_mode, txt=output_str):
            return True
        time.sleep(sleep)
        timeout -= sleep
    return False


def count_freq(pat, txt):
    pat_len = len(pat)
    txt_len = len(txt)
    res = 0
    for i in range(txt_len - pat_len + 1):
        j = 0
        while j < pat_len:
            if txt[i + j] != pat[j]:
                break
            j += 1
        if j == pat_len:
            res += 1
            j = 0
    return res


def input_func(text="", default_value="", is_num=True, expected_values=None):
    while True:
        input_value = str(input(f"{text} ({default_value}): ") or default_value)
        if is_num and not input_value.isnumeric():
            log.info("Please enter number")
            continue
        if expected_values and input_value not in expected_values:
            log.info(f"Please enter expected values {expected_values}")
            continue
        return input_value
