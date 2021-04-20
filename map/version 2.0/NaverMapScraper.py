import requests
import json
from bs4 import BeautifulSoup
import pandas as pd


class NaverMapScraper:
    def __init__(self, query):
        self.API_URL = 'https://map.naver.com/v5/api/search'

        self.graphql_url = 'https://pcmap-api.place.naver.com/place/graphql'

        self.header = {
            'authority': 'map.naver.com',
            'method': 'GET',
            'scheme': 'https',
            'referer': 'https://map.naver.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        self.query = query

    def scrape_info(self):
        scraped_items = []
        r = self.get_list_info(self.query, 1)
        i = 1
        while True:
            response = self.get_list_info(self.query, i)
            try:
                items = response['result']['place']['list']
                for item in items:
                    data = {
                        '업체명': item['name'],
                        '업종': (',').join(item['category']),
                        '블로그리뷰': item['reviewCount'],
                        '전화번호': item['tel'],
                        '도로명': item['roadAddress'],
                        '지번': item['address'],
                        'id': item['id']
                    }
                    if item['category'] == None:
                        data['업종'] = ""
                    else:
                        data['업종'] = (',').join(item['category'])
                    info = self.get_more_info(data['id'])
                    data['별점'] = info['star']
                    data['방문뷰'] = info['review']
                    scraped_items.append(data)
                i = i + 1
            except KeyError:
                break
        df = pd.DataFrame(data=scraped_items, columns=[
                          '업체명', '별점', '방문뷰', '블로그리뷰', '업종', '전화번호', '도로명', '지번'])
        df.to_csv(f'result/{self.query}.csv',
                  encoding='utf-8-sig', index=False)
        return df

    def get_more_info(self, id):
        query = "query getVisitorReviews($input: VisitorReviewsInput, $id: String) {↵  visitorReviews(input: $input) {↵    items {↵      id↵      rating↵      author {↵        id↵        nickname↵        from↵        imageUrl↵        objectId↵        url↵        __typename↵      }↵      body↵      thumbnail↵      media {↵        type↵        thumbnail↵        __typename↵      }↵      tags↵      status↵      visitCount↵      viewCount↵      visited↵      created↵      reply {↵        editUrl↵        body↵        editedBy↵        created↵        replyTitle↵        __typename↵      }↵      originType↵      item {↵        name↵        code↵        options↵        __typename↵      }↵      language↵      highlightOffsets↵      translatedText↵      businessName↵      showBookingItemName↵      showBookingItemOptions↵      bookingItemName↵      bookingItemOptions↵      __typename↵    }↵    starDistribution {↵      score↵      count↵      __typename↵    }↵    hideProductSelectBox↵    total↵    __typename↵  }↵  visitorReviewStats(input: {businessId: $id}) {↵    id↵    name↵    review {↵      avgRating↵      totalCount↵      scores {↵        count↵        score↵        __typename↵      }↵      imageReviewCount↵      __typename↵    }↵    visitorReviewsTotal↵    ratingReviewsTotal↵    __typename↵  }↵  visitorReviewThemes(input: {businessId: $id}) {↵    themeLists {↵      name↵      key↵      __typename↵    }↵    __typename↵  }↵}↵"
        data = {
            "operationName": "getVisitorReviews",
            "query": query.replace("↵", '\n'),
            "variables": {
                "id": f"{id}",
                "input": {
                    "bookingBusinessId": None,
                    "businessId": f"{id}",
                    "display": 1,
                    "includeContent": True,
                    "order": None,
                    "page": 1,
                    "theme": "allTypes"
                }
            }
        }
        r = requests.post(self.graphql_url, json=data,
                          headers={
                              'authority': 'pcmap-api.place.naver.com',
                              'method': 'POST',
                              'scheme': 'https',
                              'referer': f'https://map.naver.com/v5/api/sites/summary/{id}?lang=ko',
                              'user-agent': self.header['user-agent']
                          }).json()
        info = {
            'star': r['data']['visitorReviewStats']['review']['avgRating'],
            'review': r['data']['visitorReviewStats']['visitorReviewsTotal']
        }
        return info

    def get_list_info(self, query, page):
        payload = {
            'query': query,
            'caller': 'pcweb',
            'displayCount': 50,
            'page': page,
            'type': 'all',
            'isPlaceRecommendationReplace': 'true',
            'lang': 'ko'
        }
        r = requests.get(self.API_URL, params=payload,
                         headers=self.header)
        # r.encoding = 'utf-8'
        return r.json()

    def scrape_restaurants(self, **kwargs):
        # kwargs = {'order': 배달(delivery), 'postCode': 우편번호, 'url': 홈페이지 }
        scraped_items = []
        i = 1  # start
        n = 0  # items
        while True:
            r = self.get_restaurants(self.query, i, kwargs['order'])
            items = r['data']['restaurants']['items']
            total = int(r['data']['restaurants']['total'])
            for item in items:
                data = {
                    '업체명': item["name"],
                    '전화번호': item["phone"],
                    '주소': item["address"],
                    'id': item["id"]
                }
                if kwargs['postCode'] == True:
                    data['우편번호'] = self.get_postcode(item["address"])
                if kwargs['url'] == True:
                    urlList = self.get_summary(item["id"])
                    for url in urlList:
                        data[f"{urlList.index(url)}"] = url["url"]
                df = pd.DataFrame([data], columns=list(data.keys()))
            i = i+50
            if n >= total:
                break

    def get_summary(self, id):
        URL = f"https://map.naver.com/v5/api/sites/summary/{id}?lang=ko"
        r = requests.get(URL, headers=self.header).json()

        urlList = r['urlList']  # url 리스트
        with open("summary.json", "w", encoding="utf-8-sig") as f:
            f.write(json.dumps(r, sort_keys=True, indent=4, ensure_ascii=False))
        return urlList

    def get_postcode(self, address):
        URL = "https://search.naver.com/search.naver"
        params = {
            "where": "nexearch",
            "ie": "utf8",
            "X_CSA": "address_search",
            "query": address+" 우편번호"
        }
        r = requests.get(URL, params=params, headers=self.header)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            section = soup.find("div", {"id": "loc-main-section-root"})
            p_code = section.find(
                "span", {"class": "_49NYn"}).text.strip("우편번호")
        except:
            return ""
        return p_code

    def get_restaurants(self, location, start, **kwargs):
        query = "query getRestaurants($input: RestaurantsInput, $isNmap: Boolean!, $isBounds: Boolean!) {↵  restaurants(input: $input) {↵    total↵    items {↵      ...RestaurantItemFields↵      easyOrder {↵        easyOrderId↵        easyOrderCid↵        businessHours {↵          weekday {↵            start↵            end↵            __typename↵          }↵          weekend {↵            start↵            end↵            __typename↵          }↵          __typename↵        }↵        __typename↵      }↵      baemin {↵        businessHours {↵          deliveryTime {↵            start↵            end↵            __typename↵          }↵          closeDate {↵            start↵            end↵            __typename↵          }↵          temporaryCloseDate {↵            start↵            end↵            __typename↵          }↵          __typename↵        }↵        __typename↵      }↵      yogiyo {↵        businessHours {↵          actualDeliveryTime {↵            start↵            end↵            __typename↵          }↵          bizHours {↵            start↵            end↵            __typename↵          }↵          __typename↵        }↵        __typename↵      }↵      __typename↵    }↵    nlu {↵      ...NluFields↵      __typename↵    }↵    brand {↵      name↵      isBrand↵      type↵      menus {↵        order↵        id↵        images {↵          url↵          desc↵          __typename↵        }↵        name↵        desc↵        price↵        isRepresentative↵        detailUrl↵        orderType↵        catalogId↵        source↵        menuId↵        nutrients↵        allergies↵        __typename↵      }↵      __typename↵    }↵    optionsForMap @include(if: $isBounds) {↵      maxZoom↵      minZoom↵      includeMyLocation↵      maxIncludePoiCount↵      center↵      spotId↵      __typename↵    }↵    __typename↵  }↵}↵↵fragment RestaurantItemFields on RestaurantSummary {↵  id↵  dbType↵  name↵  businessCategory↵  category↵  description↵  hasBooking↵  hasNPay↵  x↵  y↵  distance↵  imageUrl↵  imageUrls↵  imageCount↵  phone↵  virtualPhone↵  routeUrl↵  streetPanorama {↵    id↵    pan↵    tilt↵    lat↵    lon↵    __typename↵  }↵  roadAddress↵  address↵  commonAddress↵  blogCafeReviewCount↵  bookingReviewCount↵  totalReviewCount↵  bookingReviewScore↵  bookingUrl↵  bookingHubUrl↵  bookingHubButtonName↵  bookingBusinessId↵  talktalkUrl↵  options↵  promotionTitle↵  agencyId↵  businessHours↵  microReview↵  tags↵  priceCategory↵  broadcastInfo {↵    program↵    date↵    menu↵    __typename↵  }↵  michelinGuide {↵    year↵    star↵    comment↵    url↵    hasGrade↵    isBib↵    alternateText↵    __typename↵  }↵  broadcasts {↵    program↵    menu↵    episode↵    broadcast_date↵    __typename↵  }↵  tvcastId↵  naverBookingCategory↵  saveCount↵  uniqueBroadcasts↵  isDelivery↵  isCvsDelivery↵  markerLabel @include(if: $isNmap) {↵    text↵    style↵    __typename↵  }↵  imageMarker @include(if: $isNmap) {↵    marker↵    markerSelected↵    __typename↵  }↵  isTableOrder↵  isPreOrder↵  isTakeOut↵  bookingDisplayName↵  bookingVisitId↵  bookingPickupId↵  popularMenuImages {↵    name↵    price↵    bookingCount↵    menuUrl↵    menuListUrl↵    imageUrl↵    isPopular↵    usePanoramaImage↵    __typename↵  }↵  visitorReviewCount↵  visitorReviewScore↵  detailCid {↵    c0↵    c1↵    c2↵    c3↵    __typename↵  }↵  streetPanorama {↵    id↵    pan↵    tilt↵    lat↵    lon↵    __typename↵  }↵  __typename↵}↵↵fragment NluFields on Nlu {↵  queryType↵  user {↵    gender↵    __typename↵  }↵  queryResult {↵    ptn0↵    ptn1↵    region↵    spot↵    tradeName↵    service↵    selectedRegion {↵      name↵      index↵      x↵      y↵      __typename↵    }↵    selectedRegionIndex↵    otherRegions {↵      name↵      index↵      __typename↵    }↵    property↵    keyword↵    queryType↵    nluQuery↵    businessType↵    cid↵    branch↵    franchise↵    titleKeyword↵    location {↵      x↵      y↵      default↵      longitude↵      latitude↵      dong↵      si↵      __typename↵    }↵    noRegionQuery↵    priority↵    showLocationBarFlag↵    themeId↵    filterBooking↵    repRegion↵    repSpot↵    dbQuery {↵      isDefault↵      name↵      type↵      getType↵      useFilter↵      hasComponents↵      __typename↵    }↵    type↵    category↵    menu↵    __typename↵  }↵  __typename↵}↵"
        if kwargs['order'] == True:
            order = "배달"
        else:
            order = "off"
        data = {
            "operationName": "getRestaurants",
            "query": query.replace("↵", '\n'),
            "variables": {
                "input": {
                    "deviceType": "pcmap",
                    "display": 50,
                    "isNmap": False,
                    "order": order,
                    "query": location,
                    "start": start,
                },
                "isBounds": True,
                "isNmap": False
            }
        }
        r = requests.post(self.graphql_url, json=data,
                          headers=self.header).json()
        with open("restaurants.json", "w", encoding="utf-8-sig") as f:
            f.write(json.dumps(r, sort_keys=True, indent=4, ensure_ascii=False))
        return r
