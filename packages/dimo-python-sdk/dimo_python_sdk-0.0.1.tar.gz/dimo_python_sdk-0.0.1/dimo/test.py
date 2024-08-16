from dimo import DIMO
from dotenv import load_dotenv # REMOVE!!
import os # REMOVE !!
import asyncio
load_dotenv()

dimo = DIMO("Production")


# PUBLIC ENDPOINTS
# async def test_public_endpoints():

    # device_makes = await dimo.device_definitions.list_device_makes()
    # print("DEVICE MAKES: ", device_makes)

    # by_id = await dimo.device_definitions.get_by_id(id='26G4j1YDKZhFeCsn12MAlyU3Y2H')
    # print(by_id)

    # barretts_car_by_mmy = await dimo.device_definitions.get_by_mmy(
    #     make="Hyundai",
    #     model="Tucson",
    #     year=2022
    # )
    # print("HYUNDAI TUCSON: ", barretts_car_by_mmy)

    # count = await dimo.identity.count_dimo_vehicles()
    # print(count)

#     listvd = await dimo.identity.list_vehicle_definitions_per_address(address="0x48f6EdC54Ae0706b5e6cFC33C342B49bf2dDb939",limit=2)
#     print(listvd)


# if __name__ == "__main__":
#         asyncio.run(test_public_endpoints())

# # GET ACCESS TOKEN
async def auth_routes():
    authHeader = await dimo.auth.get_token(
                client_id='0xeAa35540a94e3ebdf80448Ae7c9dE5F42CaB3481',
                domain='http://localhost:8082',
                private_key=os.getenv("private_key")
    )
    access_token = authHeader["access_token"]

# GET PRIVILEGE TOKEN
    privileged_token_req = await dimo.token_exchange.exchange(access_token, privileges=[1,3,4], token_id=17)
    privileged_token = privileged_token_req['token']
    print("USE THIS ONE:  ", privileged_token)

# "0x48f6EdC54Ae0706b5e6cFC33C342B49bf2dDb939"

# TELEMETRY TESTS
    # try:
    #     anything = await dimo.telemetry.get_daily_signals_autopi(token=privileged_token, token_id=21957, start_date="2024-07-20T18:32:12Z", 
    #         end_date="2024-07-31T18:32:12Z")
    #     print(anything)
    # except Exception as e:
    #     print(f"An error occurred: {e}")

# BEARER AUTHENTICATION w/ ACCESS_TOKEN - SAMPLE ENDPOINTS
    # my_events = await dimo.events.get_events(access_token)
    # print("My events: ", my_events)


# TEST IDENTITY 
    # my_dev_vehicles_query = """
    #            query {
    #             vehicles(filterBy: { privileged: "0xeAa35540a94e3ebdf80448Ae7c9dE5F42CaB3481" }, first: 100) {
    #                 nodes {
    #                 tokenId
    #                 definition {
    #                     make
    #                     model
    #                     year
    #                 }
    #                 },
    #                 totalCount
    #                 }
    #             }"""
    # dev_vehicles = await dimo.identity.query(query=my_dev_vehicles_query, token=privileged_token)
    # print(dev_vehicles)

# TEST TELEMETRY
    # latest_signals = await dimo.telemetry.get_signals_latest(token=privileged_token, token_id=17)
    # print(latest_signals)

# BEARER AUTHENTICATION w/ PRIVILEGE_TOKEN - SAMPLE ENDPOINTS
    # bk_vehicle_history = await dimo.device_data.get_v1_vehicle_history(privileged_token, token_id=17)
    # print("My vehicle history: ", bk_vehicle_history)

if __name__ == "__main__":
        asyncio.run(auth_routes())
