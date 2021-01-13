import requests, json, itertools, re
from bs4 import BeautifulSoup
import pandas as pd


class NaverLandScraper:
    def __init__(self, query, filter):
        self.fields = ["단지명","주소","사용승인일","세대수","총주차대수","난방","배정초등학교","단지에서 학교까지","동" ,"매매가격","공급/전용면적","해당층/총층","방수/욕실수","방향","현관구조","입주가능일","매물특징","매물설명","중개사","대표","전화","휴대전화"]
        self.building_keys = [
            "name",
            "address",
            "useApproveYmd",
            "totalHouseHoldCount",
            "parkingPossibleCount",
            "heat",
            "schoolName",
            "walkTime"
        ]
        self.article_keys = [
            "articleName",
            "dealOrWarrantPrc",
            "space",
            "floorInfo",
            "direction",
            "room",
            "entranceTypeName",
            "moveInTypeName",
            "articleFeatureDesc",
            "detailDescription",
            "realtorName",
            "representativeName",
            "representativeTelNo",
            "cellPhoneNo"
        ]
        self.query = query
        self.filter = filter
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        self.coord = self.get_coord()
        self.item_list = self.get_land()
    
    def get_coord(self):
        NAVER_MAP_URL = "https://map.naver.com/v5/api/search"
        payload = {
            "caller": "pcweb",
            "query": self.query,
        }
        headers = {
            "referer": "https://map.naver.com/",
            "user-agent": self.user_agent
        }
        r = requests.get(NAVER_MAP_URL, params=payload, headers=headers).json()["result"]["place"]["boundary"]
        r = list(map(float, r))
        data = {
            "leftLon": r[0],
            "rightLon": r[2],
            "topLat": r[1],
            "bottomLat": r[3],
        }
        return data
    
    def get_cortar(self):
        NAVER_CORTAR_URL = "https://new.land.naver.com/api/cortars"
        payload = {
            "zoom": "16",
            "centerLat": self.coord["centerY"],
            "centerLon": self.coord["centerX"],
        }
        headers = {
            "user-agent": self.user_agent
        }
        r = requests.get(NAVER_CORTAR_URL, params=payload, headers=headers)
        # cortarVertexList = list(itertools.chain(*r["cortarVertexLists"]))
        # lon = []
        # lat = []
        # for cortar in cortarVertexList:
        #     lon.append(cortar[0])
        #     lat.append(cortar[1])
        # cortarVertexList = list(map(sorted,[lon, lat]))
        cortarNo = r.json()["cortarNo"]
        # data = {
        #     "cortarVertexList": cortarVertexList,
        #     "cortarNo": cortarNo
        # }
        return cortarNo

    def get_land(self):
        NAVER_LAND_API_URL = "https://new.land.naver.com/api/complexes/single-markers/2.0"
        payload = {'cortarNo': '', 'zoom': '16', 'priceType': 'RETAIL', 'markerId': '', 'markerType': '', 'selectedComplexNo': '', 'selectedComplexBuildingNo': '', 'fakeComplexMarker': '', 'realEstateType': self.filter, 'tradeType': 'A1', 'tag': '::::::::', 'rentPriceMin': '0', 'rentPriceMax': '900000000', 'priceMin': '0', 'priceMax': '900000000', 'areaMin': '0', 'areaMax': '900000000', 'oldBuildYears': '', 'recentlyBuildYears': '', 'minHouseHoldCount': '', 'maxHouseHoldCount': '', 'showArticle': 'false', 'sameAddressGroup': 'false', 'minMaintenanceCost': '', 'maxMaintenanceCost': '', 'directions': '', 'leftLon': self.coord['leftLon'], 'rightLon': self.coord['rightLon'], 'topLat': self.coord['topLat'], 'bottomLat': self.coord['bottomLat']}
        # payload = {'cortarNo': self.cortar["cortarNo"], 'zoom': '16', 'priceType': 'RETAIL', 'markerId': '', 'markerType': '', 'selectedComplexNo': '', 'selectedComplexBuildingNo': '', 'fakeComplexMarker': '', 'realEstateType': 'APT:ABYG:JGC', 'tradeType': 'A1', 'tag': '::::::::', 'rentPriceMin': '0', 'rentPriceMax': '900000000', 'priceMin': '0', 'priceMax': '900000000', 'areaMin': '0', 'areaMax': '900000000', 'oldBuildYears': '', 'recentlyBuildYears': '', 'minHouseHoldCount': '', 'maxHouseHoldCount': '', 'showArticle': 'false', 'sameAddressGroup': 'false', 'minMaintenanceCost': '', 'maxMaintenanceCost': '', 'directions': '', 'leftLon': '127.0416541', 'rightLon': '127.0691199', 'topLat': '37.5203233', 'bottomLat': '37.5092602'}
        headers = {
            "user-agent": self.user_agent
        }
        r = requests.get(NAVER_LAND_API_URL, params=payload, headers=headers)
        # with open("apt.json", "w", encoding="utf-8-sig") as f:
        #     f.write(json.dumps(r.json(), indent=4, sort_keys=True, ensure_ascii=False))
        item_list = [item["markerId"] for item in r.json()]
        return item_list
    
    
    def extract_building_detail(self, itemNo):
        OVERVIEW_URL = f"https://new.land.naver.com/api/complexes/overview/{itemNo}?complexNo={itemNo}"
        API_URL = f"https://new.land.naver.com/api/complexes/{itemNo}?sameAddressGroup=false"
        SCHOOL_URL = f"https://new.land.naver.com/api/complexes/{itemNo}/schools"
        headers = {
            "user-agent": self.user_agent
        }
        r_overview = requests.get(OVERVIEW_URL, headers=headers).json()
        r_api = requests.get(API_URL, headers=headers).json().get("complexDetail")

        heat = json.load(open('mod.json'))["heat"]

        data = {
            "complexNo": r_api.get("complexNo",''),
            "name": r_overview.get("complexName",''),
            "address": r_api.get("address",'')+" "+r_api.get("detailAddress",''),
            "roadAddress": r_api.get("roadAddressPrefix", "")+" "+r_api.get("roadAddress", ""),
            "useApproveYmd": r_overview.get("useApproveYmd",''),
            "totalHouseHoldCount": str(r_overview.get("totalHouseHoldCount",'')) + f"(총{r_overview.get('totalDongCount','')}개동)",
            "parkingPossibleCount": str(r_api.get("parkingPossibleCount",'')) + f"(세대당 {r_api.get('parkingCountByHousehold','')}대)",
            "heat": heat["heatFuel"].get(r_api.get("heatFuelTypeCode",''),'')+","+heat["heatMethod"].get(r_api.get("heatMethodTypeCode",''),''),
            "articles": []
        }
        # schools
        try:
            r_school = requests.get(SCHOOL_URL, headers=headers).json().get("schools")
            # for school in r_school:
            #     data["schools"].append({"schoolName": school["schoolName"], "walkTime": school["walkTime"]})
            data["schoolName"] = r_school[0]["schoolName"]
            data["walkTime"] = r_school[0]["walkTime"]
        except:
            pass
        # articles
        try:
            data["articles"] = self.extract_building_articles(itemNo)
        except:
            pass
        return data
    
    def extract_building_articles(self, itemNo):
        # ARTICLES_URL = "https://new.land.naver.com/api/articles/complex/{itemNo}"
        URL = f"https://new.land.naver.com/api/articles/complex/{itemNo}?realEstateType={self.filter}&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount&maxHouseHoldCount&showArticle=false&sameAddressGroup=false&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page=1&complexNo={itemNo}&buildingNos=&areaNos=&type=list&order=rank"
        payload = {'realEstateType': 'APT:ABYG:JGC', 'tradeType': 'A1', 'tag': '::::::::', 'rentPriceMin': '0', 'rentPriceMax': '900000000', 'priceMin': '0', 'priceMax': '900000000', 'areaMin': '0', 'areaMax': '900000000', 'oldBuildYears': '', 'recentlyBuildYears': '', 'minHouseHoldCount': '', 'maxHouseHoldCount': '', 'showArticle': 'false', 'sameAddressGroup': 'false', 'minMaintenanceCost': '', 'maxMaintenanceCost': '', 'priceType': 'RETAIL', 'directions': '', 'page': '1', 'complexNo': itemNo, 'buildingNos': '', 'areaNos': '', 'type': 'list', 'order': 'rank'}
        headers = {
            "user-agent": self.user_agent
        }
        r_articles = requests.get(URL, headers=headers).json().get('articleList')
        article_list = []
        for article in r_articles:
            articleNo = article.get("articleNo")
            article_list.append(self.extract_building_articles_detail(articleNo))
        return article_list
    
    def extract_building_articles_detail(self, articleNo):
        ARTICLE_DETAIL_URL = f"https://new.land.naver.com/api/articles/{articleNo}?complexNo="
        headers = {
            "user-agent": self.user_agent
        }
        r_detail = requests.get(ARTICLE_DETAIL_URL, headers=headers).json()
        data = {
            "articleNo": articleNo,
            "articleName": r_detail["articleDetail"]["articleName"],
            "dealOrWarrantPrc": r_detail["articleAddition"]["dealOrWarrantPrc"],
            "space": str(r_detail["articleSpace"].get("exclusiveSpace",""))+"/"+str(r_detail["articleSpace"].get("supplySpace",""))+f'(전용율{str(r_detail["articleSpace"].get("exclusiveRate",""))}%)',
            "floorInfo": r_detail["articleAddition"].get("floorInfo",""),
            "direction": r_detail["articleAddition"].get("direction",""),
            "room": str(r_detail["articleDetail"].get("roomCount",""))+"/"+str(r_detail["articleDetail"].get("bathroomCount","")),
            "entranceTypeName": r_detail["articleFacility"].get("entranceTypeName",""),
            "moveInTypeName": r_detail["articleDetail"].get("moveInTypeName",""),
            "articleFeatureDesc": r_detail["articleAddition"].get("articleFeatureDesc",""),
            "detailDescription":re.sub("[\r\n\t]"," ",r_detail["articleDetail"].get("detailDescription","")),
            "realtorName": r_detail["articleRealtor"].get("realtorName",""),
            "representativeName": r_detail["articleRealtor"].get("representativeName",""),
            "representativeTelNo": r_detail["articleRealtor"].get("representativeTelNo",""),
            "cellPhoneNo": r_detail["articleRealtor"].get("cellPhoneNo","")
        }
        return data

    def start_scraping(self):
        columns=self.building_keys+self.article_keys
        df = pd.DataFrame({}, columns=columns)
        for item in self.item_list:
            result = self.extract_building_detail(item)
            new_df = pd.DataFrame([result], columns=self.building_keys)
            if len(result["articles"]) != 0:
                building_df = pd.concat([new_df]*len(result["articles"]), ignore_index=True)
                article_df = pd.DataFrame(result["articles"], columns=self.article_keys)
                new_df = pd.concat([building_df, article_df], axis=1)
            df = df.append(new_df)
        df.to_csv(f'result/{self.query}.csv', encoding='utf-8-sig', index=False, header=self.fields)
