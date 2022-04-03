import logging
import sys

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


def create_new_prject():
    project_name = str(input("Enter project name (fio-test) : ") or "fio-test")
    send_cmd(f"oc new-project {project_name}")
    return project_name


def create_pvc(project_name=None):
    pvc_name = str(input("Enter pvc name (pvc-test) : ") or "pvc-test")
    print(pvc_name)
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
    print(pvc_mode)
    pvc_capacity_number = str(
        input("Enter pvc capacity [only number] in Gi (5Gi) : ") or "5"
    )
    pvc_capacity = f"{pvc_capacity_number}Gi"
    print(pvc_capacity)
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
    print(storage_class_name)

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


def create_pref_pod():
    project_name = str(input("Enter project name (fio-test) : ") or "fio-test")
    pvc_name = str(input("Enter pvc name (pvc-test) : ") or "pvc-test")
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


def run_fio():
    project_name = str(input("Enter project name (fio-test) : ") or "fio-test")
    pod_name = str(input("Enter pod name (pod-test) : ") or "pod-test")
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
    send_cmd(cmd)
