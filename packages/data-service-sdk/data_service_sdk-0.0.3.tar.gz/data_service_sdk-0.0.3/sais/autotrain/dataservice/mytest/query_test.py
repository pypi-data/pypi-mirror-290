# from sais.autotrain.dataservice.auth.auth_info import EnvVarCredentialsProvider
# from sais.autotrain.dataservice.config.const import ENDPOINT
# from sais.autotrain.dataservice.handler.query_handler import QueryStationRelatedHandler, QueryNWPHandler
# from sais.autotrain.dataservice.model.data_model import QueryStationRequest, QueryObservationRequest, QueryNWPRequest

from sais.autotrain.dataservice import EnvVarCredentialsProvider
from sais.autotrain.dataservice import ENDPOINT
from sais.autotrain.dataservice import QueryStationRelatedHandler, QueryNWPHandler
from sais.autotrain.dataservice import QueryStationRequest, QueryObservationRequest, QueryNWPRequest

# query_station_related = QueryStationRelatedHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# query_station_result = query_station_related.execute_query_station(QueryStationRequest(
#     # ids=["1"],
#     provinces=["山东"],
#     page=1,
#     page_size=10,
#     query_type=0
# ))
# print(f"Query station result: {query_station_result}")
#
# query_observation_result = query_station_related.execute_query_observation(QueryObservationRequest(
#     ids=["1"],
#     # provinces=["山东"],
#     start_time="2023-01-01 00:00:05",
#     end_time="2024-01-01 00:00:05",
#     page=1,
#     page_size=10,
#     query_type=0
# ))
# print(f"Query observation result: {query_observation_result}")


# 全页遍历
# page = 1
# page_size = 1000
# while True:
#     query_observation_result_item = query_station_related.execute_query_observation(QueryObservationRequest(
#         ids=["1"],
#         # provinces=["山东"],
#         start_time="2023-01-01 00:00:05",
#         end_time="2024-07-01 00:00:05",
#         page=page,
#         page_size=page_size,
#         query_type=0
#     ))
#     if len(query_observation_result_item.records) == 0:
#         break
#     else:
#         print(f"Query observation result: {query_observation_result_item}")
#     page += 1




query_nwp = QueryNWPHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
query_nwp.execute_query(query_params=QueryNWPRequest(
    src="ec/gfs",
    start_time="24010100",
    period_interval=24,
    period=365,
    start_hour=0,
    end_hour=24,
    forecast_interval=1,
    coords=[{"req_lat": 35.0, "req_lon": 109.9}],
    vars=[
        "tp",
        "t2m"
    ],
    levels=[
        "309",
        "387",
        "899",
        "484",
        "565",
        "268",
        "644",
        "100",
        "500",
        "374",
        "322",
        "261",
        "600"
    ]))