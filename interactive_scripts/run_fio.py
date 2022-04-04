from interactive_scripts.helpers import create_new_prject, create_pvc, create_pref_pod, run_fio

if __name__ == "__main__":
    project_name = create_new_prject()
    pvc_name = create_pvc(project_name)
    pod_name = create_pref_pod(project_name, pvc_name)
    run_fio(project_name, pod_name)


