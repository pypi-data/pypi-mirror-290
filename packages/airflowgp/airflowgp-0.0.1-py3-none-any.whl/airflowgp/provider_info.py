def get_provider_info():
    return {
        "package-name": "airflowgp",
        "name": "greenplum",
        "description": "Airflow Hook for Greenplum",
        "hook-class-names": [
            "airflowgp.hooks.greenplum.GreenplumHook",
        ],
        "connection-types": [
            {'connection-type': "greenplum", 'hook-class-name': "airflowgp.hooks.greenplum.GreenplumHook"}
        ],
        "extra-links": [
            "airflowgp.operators.greenplum.GreenplumOperator"
        ]
    }
