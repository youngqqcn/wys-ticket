from pprint import pprint
import traceback
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxNzY1YmUwYmVmMDY0NDk5YWEzNGE4MDUwNWQ4ZTk4MiIsInVzZXJJZCI6IjE3NjViZTBiZWYwNjQ0OTlhYTM0YTgwNTA1ZDhlOTgyIiwibmFtZSI6IuWumOe9keaVo-WuoiIsInRlbmFudElkIjoiOGYyMjY0NWIwYmY5ZDZhNzhhYjQ3ZDk5ZmI1YzhjZmYiLCJtZXJjaElkIjoiYWY3MjRmZmJlMGNmNGYxZmJmZDNkMDU5ZWNmMzFjMGIiLCJleHAiOjE3MjcxNzIwMDV9.nCg_KkhVkn-Bg0ig9yAWJre6nqoh9dtLh2KRHZUV8Dw"


def get_available_times_batch(date: str):

    rsp = requests.post(
        url="https://xcx.wyschina.com/gateway/applet/raft/scheduleTimes/get-available-times",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/9079",
            "Token": TOKEN,
            "Content-Type": "application/json",
        },
        json={
            "tenantId": "8f22645b0bf9d6a78ab47d99fb5c8cff",
            "merchId": "af724ffbe0cf4f1fbfd3d059ecf31c0b",
            "scheduleDate": date,
            "goodsIdList": "E18a2ilk9vuk00",
        },
    )
    return rsp.json()


def create_general_order(date_str: str, scheduleTimesId: str):

    data = {
        "contactCardNo": "431103199509076937",
        "contactCardType": "1",
        "contactMobile": config['contactMobile'],
        "contactName": config['contactName'],
        "merchId": "af724ffbe0cf4f1fbfd3d059ecf31c0b",
        "saleStationCode": "s_wechat",
        "uniteTripCreateList": [],
        "uniteRaftCreateList": [],
        "unitePackagesCreateList": [
            {
                "goodsId": "E18a2ilk9vuk00",
                "useStartDate": "2024-10-02",
                "scheduleTimesId": scheduleTimesId,
                "orderCreateItemList": [
                    {
                        "orderRaftCreateList": [
                            {
                                "goodsId": "H1866117t03c00",
                                "quantity": 1,
                                "scheduleTimesId": scheduleTimesId,
                            }
                        ],
                        "orderTripCreateList": [
                            {"goodsId": "A1865tl1lm3k00", "useStartDate": "2024-10-02"},
                            {"goodsId": "A1875rta011k00", "useStartDate": "2024-10-02"},
                        ],
                        "visitor": {
                            "visitorName": config['visitorName1'],
                            "visitorCertificateTypeName": "身份证",
                            "visitorCertificateType": "1",
                            "visitorCertificateNo": config['visitorCertificateNo1'],
                            "visitorMobile": config['contactMobile'],
                            "addShow": False,
                            "faceId": None,
                            "targetFaceId": None,
                            "lifePhotoUrl": None,
                            "visitorCertificateImgUrl": None,
                        },
                    }
                ],
                "scheduleDate": "2024-10-02",
            }
        ],
        "useStartDate": "2024-10-02",
        "takeTicketPassword": "199597",
        "saleLocationId": None,
    }

    # pprint(data)

    rsp = requests.post(
        url="https://xcx.wyschina.com/gateway/applet/order/unite/create-general-order",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Token": TOKEN,
            "Content-Type": "application/json",
        },
        json=data,
    )
    return rsp.json()


def search_time_id(datas, date_str: str, begin_time_str: str):

    for d in datas:
        if d["beginTime"] == begin_time_str and date_str == d["scheduleDate"]:
            return d["id"]

    raise ""


def main():

    date_str = "2024-10-02"
    time_str = "07:10"

    try:
        # 获取可用场次
        rsp = get_available_times_batch(date_str)
        pprint(rsp)

        # 获取场次列表
        times = rsp["data"]
        if len(times) == 0:
            print("竹筏场次为空")
            return

        # 查找场次id
        time_id = search_time_id(times, date_str, time_str)
        if time_id == "":
            print("未找到场次id: {}, {}".format(date_str, time_str))
            return

        print("找到场次{},{}, time_id: {}".format(date_str, time_str, time_id))

        # 创建订单
        # rsp = create_general_order(date_str=date_str, scheduleTimesId=time_id)
        # print("创建订单结果:{}".format(rsp))
    except Exception as e:
        # print(e)
        traceback.print_exc()
    pass


if __name__ == "__main__":
    main()
