from helpers.helpers import input_func
from helpers import constants
from helpers.bechmark_operator import BenchmarkOperatorFIO
from infra_cmd.infra_cmd import logging

if __name__ == "__main__":
    pvc_size = input_func(
        text="Enter PVC size [GiB]",
        default_value="2",
        is_num=True,
        expected_values=None,
    )
    number_servers = input_func(
        text="Enter number of servers [fio pods]",
        default_value="2",
        is_num=True,
        expected_values=None,
    )
    file_size_per_pvc = input_func(
        text="Enter file size per pvc [GiB]",
        default_value="2",
        is_num=True,
        expected_values=None,
    )
    jobs = input_func(
        text="""
Enter Job type:
    1.write
    2.read
    3.readwrite
    4.randread
    5.randwrite
    6.randrw
""",
        default_value="2",
        is_num=True,
        expected_values=["1", "2", "3", "4", "5", "6"],
    )
    job_name = constants.dic_job[jobs]
    read_runtime = input_func(
        text="Enter read runtime",
        default_value="20000",
        is_num=True,
        expected_values=None,
    )
    bs = input_func(
        text="Enter block size [Kib]",
        default_value="4096",
        is_num=True,
        expected_values=None,
    )
    bs_k = f"{bs}KiB"
    storageclass = input_func(
        text="""
Enter Storage Class type:
    1.ocs-storagecluster-cephfs
    2.ocs-storagecluster-ceph-rbd
""",
        default_value="2",
        is_num=True,
        expected_values=["1", "2"],
    )
    storageclass_name = constants.dic_sc[storageclass]
    timeout_completed = input_func(
        text="Enter timeout", default_value="20000", is_num=True, expected_values=None
    )
    run_teardown = input_func(
        text="""
Run teardown at the end of the the script
1.Yes
2.No
""",
        default_value="1",
        is_num=True,
        expected_values=["1", "2"],
    )
    run_teardown_bool = constants.dic_bool[run_teardown]
    benchmark_operator_obj = BenchmarkOperatorFIO(
        jobs=job_name,
        read_runtime=int(read_runtime),
        bs=bs_k,
        storageclass=storageclass_name,
        file_size=file_size_per_pvc,
        pvc_size=pvc_size,
        servers=int(number_servers),
        timeout_completed=500,
    )
    try:
        benchmark_operator_obj.run_fio_benchmark_operator()
        if run_teardown:
            benchmark_operator_obj.cleanup()
    except Exception as e:
        logging(text=e, type="error")
        if run_teardown:
            benchmark_operator_obj.cleanup()
