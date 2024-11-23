from pathlib import Path
import json

UUID2ID_DICT = {
    '014b6780-c3bc-45a6-9937-096bd0b79b62': 'p008',
    '6261cfca-bc45-425a-9386-736a1e84d8c1': 'p013',
    'b034bb2b-1a84-4f67-91f2-9bc36a215d87': 'p015',
    '15a66a3e-9d1e-4aa5-8157-b2d6ec1fa1c7': 'p018',
    '24a032e7-77d4-4de0-910f-fb18c6663f06': 'p028',
    '70e7809a-59c4-43a6-b5a6-bde12670f4d9': 'p037', # Dropped?
    '1c6ec1c8-5756-4320-a3d7-5f18d71a028e': 'p040', # Dropped?
    'baaf8f40-77ef-457e-acf1-e2adaede02de': 'p055',
    '217d24b8-87bf-4d9f-86f1-d5d81dc6749c': 'p060',
    '640b0635-3307-4326-ac1e-8606b117be01': 'p062',
    'a231a2c4-046e-4eb6-8da6-9430e45aa477': 'p067',
    'a06b4a95-205e-491c-bf8a-ec2fd449830e': 'p069',
    '1d1d9b19-3f31-478d-acaf-2bd0e0f8349a': 'p070',
    '79240f85-d4b8-4b94-bb4e-d2d377f1376d': 'p072',
    '58a56074-d27a-42e0-8a09-07a540f149f4': 'p074',
    '7e926289-5364-4586-9822-452a329611ff': 'p076',
    '14a41383-dd7c-43d4-9d05-8051266b70df': 'p079',
    '3aa123d4-787d-44be-865a-b3c6f439e4be': 'p083',
    '46396cdf-358a-43f8-8b7d-47f883303ac6': 'p086',
    '9fe5748c-4a39-475c-9213-380492acf456': 'p088',
    '863ad3e3-d909-45a3-83f7-b75690f1d711': 'p089',
    'ebb87cb2-e3e8-45a2-9730-7d16ed5b1164': 'p090',
    '319d5b4b-a92f-40b5-a55e-b2114576a5b0': 'p092',
    '352584e5-4f9b-4911-9caa-e9f68f967638': 'p095',
    '24cc3fc0-40f1-4acd-9074-a32f1ab0db3f': 'p096',
    'b62d2fa8-712f-4c6f-8549-b6dbcc640827': 'p098',
    'f7b4f31e-f9f3-4d33-8449-d543caf468b5': 'p099',
    '0297e57c-f4b1-4334-a4b5-6d88a2c215b5': 'p102',
    '6df0faae-615b-41d3-8a0c-f7d2ea5a5575': 'p104',
    '9c8a2381-f3fe-460e-ada4-2f2b3a5c24c6': 'p107',
    '12096106-625a-4818-aca0-3aac9d9a7f3d': 'p108',
    'c38633eb-6210-48d8-8320-a2024d5f7804': 'p111',
    '0606bdb0-7be8-437a-9a92-6589368894a1': 'p115',
    '254de8d5-83f7-4ba4-98d5-6d2012b6a26a': 'p116',
    'a92bed96-daa6-481c-8e12-7c98fbf4de5a': 'p118',
    '7618f5e3-a447-4b5a-b7c8-d903a8e69cbe': 'p120',
    'cb1669f6-2962-4866-8f65-414c50252f75': 'p121',
    'e7d22ac2-5ef8-4ef8-8755-1b88a93854a2': 'p123',
    'd24f3da7-0363-4cea-983b-b0160c7f3f81': 'p129',
    '884b3c41-38ec-4e4a-b56f-cd5cc1145945': 'p130',
    'b2629681-2084-489c-85fc-8a26a63e0216': 'p132',
    'fb1304f1-32e0-4a28-b4d4-541bb986e393': 'p134',
    'd8208883-7407-42b7-b511-95924e92919f': 'p136',
    'ccca2755-712f-492d-9d05-1fd83f3c620d': 'p137',
    'e9c93b69-ebe5-4088-9d71-e5feb5bc03ad': 'p138',
    '042dc6cb-fe3b-4d88-9d6a-9872fb55bd50': 'p141',
    '6eab5586-68d0-46af-9a53-549f8432ed9d': 'p142',
    '52ca443c-4638-4b85-b714-3fa70babb599': 'p146',
    '51f752bd-add1-41e0-bd7b-26d62915eb3b': 'p156',
    '89aebe6d-1171-43ad-87df-aba7d5f19f41': 'p164',
    'a4af1fc1-f1b9-4b21-b49c-65140858f1c6': 'p170',
    '64b25346-991f-4524-b953-937e0711c486': 'p171',
    'f215e668-a529-4726-9cd3-ec12b807bb55': 'p172',
    'ce3a1cf3-4128-4994-83be-d1e4dce462fb': 'p177',
    'de6729fb-af6c-46f4-8a47-3d3e016544cc': 'p178',
    'fa820fd5-c79c-460e-97e6-0f5a8d9ecfd8': 'p182',
    'd343d1fc-138b-49e7-8053-36fcbe32ccfa': 'p184',
    '0d30bc09-dc43-4eee-a427-34b3ca6041e6': 'p187',
    '125cce8a-4ea0-478f-8393-c39f518b7e04': 'p188',
    '3eb892f3-2fa0-43d6-85c0-aaf5af76ba55': 'p191',
    'db2ac786-0a6d-4f1b-a8b2-034c8311f0fc': 'p194',
    '1c6d8dab-37f4-482d-aa14-e3b7c2f6aa91': 'p195',
    'ccca2755-712f-492d-9d05-1fd83f3c620d': 'p196',
    'f8abfba3-c338-4592-83a1-5862acdf4ebe': 'p199',
    '48c16a98-819b-40f7-891a-ea8830b3bfae': 'p208'
}

UUIDS = list(UUID2ID_DICT.keys())
IDS = list(UUID2ID_DICT.values())

def uuid2id(uuid):
    return UUID2ID_DICT[uuid]


def getPkgName(uuid):
    filepath = Path('test.json')
    with open(filepath, 'r') as fp:
        data = json.load(fp)

    return data['responses'][uuid]['package_name'] if uuid in data['responses'] else "no response"
