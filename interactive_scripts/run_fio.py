from interactive_scripts.helpers import create_new_prject, create_pvc, create_pref_pod, run_fio

if __name__ == "__main__":
    project_name = create_new_prject()
    create_pvc(project_name)
    create_pref_pod()
    run_fio()


