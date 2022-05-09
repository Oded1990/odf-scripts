# StorageClass
DEFAULT_STORAGECLASS_CEPHFS = "ocs-storagecluster-cephfs"
DEFAULT_STORAGECLASS_RBD = "ocs-storagecluster-ceph-rbd"

# Benchmark operator
BMO_NS = "benchmark-operator"
BMO_REPO = "https://github.com/cloud-bulldozer/benchmark-operator"
BMO_LABEL = "kernel-cache-dropper"

# Statuses
STATUS_READY = "Ready"
STATUS_PENDING = "Pending"
STATUS_CONTAINER_CREATING = "ContainerCreating"
STATUS_AVAILABLE = "Available"
STATUS_RUNNING = "Running"
STATUS_TERMINATING = "Terminating"
STATUS_CLBO = "CrashLoopBackOff"
STATUS_BOUND = "Bound"
STATUS_RELEASED = "Released"
STATUS_COMPLETED = "Completed"
STATUS_ERROR = "Error"
STATUS_READYTOUSE = "READYTOUSE"
STATUS_FAILED = "Failed"
STATUS_FAILEDOVER = "FailedOver"
STATUS_RELOCATED = "Relocated"

# namspaces
OPENSHIFT_STORAGE_NAMESPACE = "openshift-storage"
BENCHMARK_OPERATOR_NAMESPACE = "benchmark-operator"

dic_job = {
    "1": "write",
    "2": "read",
    "3": "readwrite",
    "4": "randread",
    "5": "randwrite",
    "6": "randrw",
}

dic_sc = {
    "1": DEFAULT_STORAGECLASS_CEPHFS,
    "2": DEFAULT_STORAGECLASS_RBD,
}

dic_bool = {"1": True, "2": False}
