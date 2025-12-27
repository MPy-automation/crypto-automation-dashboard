def set_schedule():
    from s_program_01_config import PYTHON_PATH, SCRIPT_PATH
    import subprocess

    tr_value = f'"{PYTHON_PATH}" "{SCRIPT_PATH}"'

    cmd = [
        "schtasks",
        "/create",
        "/tn", "Crypto Analyse",
        "/tr", tr_value,
        "/sc", "onlogon",
        "/rl", "HIGHEST",
        "/it",
        "/delay", "0000:30",
        "/f"
    ]

    subprocess.run(cmd)

