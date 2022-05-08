from interactive_scripts.helpers import (
    create_new_prject,
    create_pvc,
    create_pref_pod,
    run_fio,
    delete_pod,
    delete_project,
    delete_pvc,
)

if __name__ == "__main__":
    project_name = create_new_prject()
    number_of_fio = str(input("number of fios? (2): ") or "2")
    pvc_name = create_pvc(project_name)
    pod_name = create_pref_pod(project_name, pvc_name)
    run_fio(project_name, pod_name)
    delete_leftovers = str(input("Delete leftovers? (Yes/No): ") or "Yes")
    if "y" in delete_leftovers.lower():
        delete_pod(project_name, pod_name)
        delete_pvc(project_name, pvc_name)
        delete_project(project_name)
