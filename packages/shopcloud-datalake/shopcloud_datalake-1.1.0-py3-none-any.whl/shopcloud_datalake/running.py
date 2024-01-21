from shopcloud_secrethub import SecretHub

from . import erps, helpers, storages, tables, warehouses


def main(**kwargs) -> int:
    debug = kwargs.get("debug", False)
    hub = SecretHub(user_app="shopcloud-datalake")

    project = kwargs.get("project")
    location = kwargs.get("location")
    partition_date = kwargs.get("partition_date")

    storage_adapter_manager = storages.StorageAdapterManager(
        hub,
        debug=debug,
        config={
            "project": project,
            "location": location,
        }
    )
    bucket_data = storage_adapter_manager.get(storages.GoogleCloudStorageAdapter.NAME, bucket_type="data")
    bucket_config = storage_adapter_manager.get(storages.GoogleCloudStorageAdapter.NAME, bucket_type="config")

    table = kwargs.get("table")
    datas = (
        [table]
        if table is not None
        else [
            x.replace(".yaml", "")
            for x in bucket_config.list()
            if x.endswith(".yaml")
        ]
    )
    datas = [
        helpers.Pipeline(
            name="table-loading", _for=x, raise_exception=True
        )
        for x in datas
    ]
    datas = [
        x.step(
            "table:load-config",
            lambda y: tables.TableConfig.create_from_config(y._for, bucket_config),
        )
        for x in datas
    ]

    erp_adapter_manager = erps.ErpAdapterManager(
        hub,
        debug=debug,
        config={
            "request_page_limit": kwargs.get("request_page_limit", 5000),
            "max_workers": kwargs.get("max_workers", 4),
        },
    )
    warehouse_adapter_manager = warehouses.WarehouseManager(
        hub,
        debug=debug,
        config={
            "project": project,
            "location": location,
        }
    )
    datas = [
        x.step(
            "table:init",
            lambda y: tables.Table(
                config=y.data,
                erp_adapter=erp_adapter_manager.get(y.data.erp_adapter),
                warehouse_adapter=warehouse_adapter_manager.get(
                    warehouses.WarehouseBigQueryAdapter.NAME
                ),
                storage_data=bucket_data,
                storage_config=bucket_config,
                partition_date=partition_date,
            ),
        )
        for x in datas
    ]
    datas = [
        x.step(
            "table:proceed",
            lambda y: y.data.proceed(debug=debug),
        )
        for x in datas
    ]

    for p in datas:
        if p.is_success:
            print(
                helpers.bcolors.OKGREEN
                + f"+ {p.name} {p._for} {p.data.stats}"
                + helpers.bcolors.ENDC
            )
        else:
            print(
                helpers.bcolors.FAIL
                + f"+ {p.name} {p._for} {p.steps[-1]['exception']}"
                + helpers.bcolors.ENDC
            )

    return 0
