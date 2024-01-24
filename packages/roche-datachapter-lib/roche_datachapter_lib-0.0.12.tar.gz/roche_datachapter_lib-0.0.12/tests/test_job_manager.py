from roche_datachapter_lib.job_manager import JobManager

JM=JobManager()

jobname = 'AB_TestJOB_LUCAS_PYTHON'
user = 'RNUMDMAS\\osirisl'
path = 'C:\\Users\\Lucas\\run_app.bat'
JM.create_or_update_python_job(jobname, user, path)
