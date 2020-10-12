import requests, json
from bs4 import BeautifulSoup
import pandas as pd

class Scraper:
    def __init__(self, query):
        self.API_URL = 'https://map.naver.com/v5/api/search'

        self.graphql_url = 'https://pcmap-api.place.naver.com/place/graphql'

        self.header = {
            'authority': 'pcmap-api.place.naver.com',
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
                        '리뷰갯수': item['reviewCount'],
                        '전화번호': item['tel'],
                        '도로명': item['roadAddress'],
                        '지번': item['address'],
                        'id': item['id']
                    }
                    data['별점'] = self.get_stars(data['id'])
                    scraped_items.append(data)
                i = i + 1
            except KeyError:
                break
        df = pd.DataFrame(data=scraped_items, columns=['id','업체명', '별점', '리뷰갯수','업종','전화번호','도로명','지번'])
        df.to_csv('output.csv', encoding='utf-8-sig')
        return df
    
    def get_stars(self, id):
        query = "query getVisitorReviews($input: VisitorReviewsInput, $id: String) {↵  visitorReviews(input: $input) {↵    items {↵      id↵      rating↵      author {↵        id↵        nickname↵        from↵        imageUrl↵        objectId↵        url↵        __typename↵      }↵      body↵      thumbnail↵      media {↵        type↵        thumbnail↵        __typename↵      }↵      tags↵      status↵      visitCount↵      viewCount↵      visited↵      created↵      reply {↵        editUrl↵        body↵        editedBy↵        created↵        replyTitle↵        __typename↵      }↵      originType↵      item {↵        name↵        code↵        options↵        __typename↵      }↵      language↵      highlightOffsets↵      translatedText↵      businessName↵      showBookingItemName↵      showBookingItemOptions↵      bookingItemName↵      bookingItemOptions↵      __typename↵    }↵    starDistribution {↵      score↵      count↵      __typename↵    }↵    hideProductSelectBox↵    total↵    __typename↵  }↵  visitorReviewStats(input: {businessId: $id}) {↵    id↵    name↵    review {↵      avgRating↵      totalCount↵      scores {↵        count↵        score↵        __typename↵      }↵      imageReviewCount↵      __typename↵    }↵    visitorReviewsTotal↵    ratingReviewsTotal↵    __typename↵  }↵  visitorReviewThemes(input: {businessId: $id}) {↵    themeLists {↵      name↵      key↵      __typename↵    }↵    __typename↵  }↵}↵".replace("↵", '\n')
        data = {
            "operationName": "getVisitorReviews",
            "query": query,
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
        r = requests.post(self.graphql_url, json=data, headers=self.header).json()
        star = r['data']['visitorReviewStats']['review']['avgRating']
        return star

            
    def get_list_info(self, query, page):
        payload= {
            'query': query,
            'caller': 'pcweb',
            'displayCount': 50,
            'page': page,
            'type': 'all',
            'isPlaceRecommendationReplace': 'true',
            'lang': 'ko'
        }
        r = requests.get(self.API_URL, params=payload, headers=self.header).json()
        # r.encoding = 'utf-8'
        return r

    # def get_location_info(self, query, start):
    #     header = {
    #         'authority': 'pcmap-api.place.naver.com',
    #         'accept-encoding': 'gzip, deflate, br',
    #         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    #     }

    #     query = "query getRestaurants($input: RestaurantsInput, $isNmap: Boolean!, $isBounds: Boolean!) {↵  restaurants(input: $input) {↵    total↵    items {↵      ...RestaurantItemFields↵      easyOrder {↵        easyOrderId↵        easyOrderCid↵        businessHours {↵          weekday {↵            start↵            end↵            __typename↵          }↵          weekend {↵            start↵            end↵            __typename↵          }↵          __typename↵        }↵        __typename↵      }↵      baemin {↵        businessHours {↵          deliveryTime {↵            start↵            end↵            __typename↵          }↵          closeDate {↵            start↵            end↵            __typename↵          }↵          temporaryCloseDate {↵            start↵            end↵            __typename↵          }↵          __typename↵        }↵        __typename↵      }↵      yogiyo {↵        businessHours {↵          actualDeliveryTime {↵            start↵            end↵            __typename↵          }↵          bizHours {↵            start↵            end↵            __typename↵          }↵          __typename↵        }↵        __typename↵      }↵      __typename↵    }↵    nlu {↵      ...NluFields↵      __typename↵    }↵    brand {↵      name↵      isBrand↵      type↵      menus {↵        order↵        id↵        images {↵          url↵          desc↵          __typename↵        }↵        name↵        desc↵        price↵        isRepresentative↵        detailUrl↵        orderType↵        catalogId↵        source↵        menuId↵        nutrients↵        allergies↵        __typename↵      }↵      __typename↵    }↵    optionsForMap @include(if: $isBounds) {↵      maxZoom↵      minZoom↵      includeMyLocation↵      maxIncludePoiCount↵      center↵      spotId↵      __typename↵    }↵    __typename↵  }↵}↵↵fragment RestaurantItemFields on RestaurantSummary {↵  id↵  dbType↵  name↵  businessCategory↵  category↵  description↵  hasBooking↵  hasNPay↵  x↵  y↵  distance↵  imageUrl↵  imageUrls↵  imageCount↵  phone↵  virtualPhone↵  routeUrl↵  streetPanorama {↵    id↵    pan↵    tilt↵    lat↵    lon↵    __typename↵  }↵  roadAddress↵  address↵  commonAddress↵  blogCafeReviewCount↵  bookingReviewCount↵  totalReviewCount↵  bookingReviewScore↵  bookingUrl↵  bookingBusinessId↵  talktalkUrl↵  options↵  promotionTitle↵  agencyId↵  businessHours↵  microReview↵  tags↵  priceCategory↵  broadcastInfo {↵    program↵    date↵    menu↵    __typename↵  }↵  michelinGuide {↵    year↵    star↵    comment↵    url↵    hasGrade↵    isBib↵    alternateText↵    __typename↵  }↵  broadcasts {↵    program↵    menu↵    episode↵    broadcast_date↵    __typename↵  }↵  tvcastId↵  naverBookingCategory↵  saveCount↵  uniqueBroadcasts↵  isDelivery↵  markerLabel @include(if: $isNmap) {↵    text↵    style↵    __typename↵  }↵  imageMarker @include(if: $isNmap) {↵    marker↵    markerSelected↵    __typename↵  }↵  isTableOrder↵  isPreOrder↵  isTakeOut↵  bookingDisplayName↵  bookingVisitId↵  bookingPickupId↵  popularMenuImages {↵    name↵    price↵    bookingCount↵    menuUrl↵    menuListUrl↵    imageUrl↵    isPopular↵    usePanoramaImage↵    __typename↵  }↵  visitorReviewCount↵  visitorReviewScore↵  detailCid {↵    c0↵    c1↵    c2↵    c3↵    __typename↵  }↵  streetPanorama {↵    id↵    pan↵    tilt↵    lat↵    lon↵    __typename↵  }↵  __typename↵}↵↵fragment NluFields on Nlu {↵  queryType↵  user {↵    gender↵    __typename↵  }↵  queryResult {↵    ptn0↵    ptn1↵    region↵    spot↵    tradeName↵    service↵    selectedRegion {↵      name↵      index↵      x↵      y↵      __typename↵    }↵    selectedRegionIndex↵    otherRegions {↵      name↵      index↵      __typename↵    }↵    property↵    keyword↵    queryType↵    nluQuery↵    businessType↵    cid↵    branch↵    franchise↵    titleKeyword↵    location {↵      x↵      y↵      default↵      longitude↵      latitude↵      dong↵      si↵      __typename↵    }↵    noRegionQuery↵    priority↵    showLocationBarFlag↵    themeId↵    filterBooking↵    repRegion↵    repSpot↵    dbQuery {↵      isDefault↵      name↵      type↵      getType↵      useFilter↵      hasComponents↵      __typename↵    }↵    type↵    category↵    __typename↵  }↵  __typename↵}↵".replace("↵","\n")
        
    #     data = {
    #         'operationName': "getRestaurants",
    #         'query': query,
    #         'variables': {'input': {
    #             'deviceType': "pcmap",
    #             'display': 50,
    #             'isNmap': False,
    #             'query': query,
    #             'start': start
    #         },
    #         'isBounds': True,
    #         'isNmap': False
    #         }
    #     }
    #     r = requests.post(self.API_URL, headers=header, json=data).json()
        
    #     

    #     
    #     with open('newgangnam.json', 'w', encoding='utf-8') as f:
    #         result = json.dumps(r, indent=4, sort_keys=True, ensure_ascii=False)
    #         f.write(result)

    #     return
    
    def get_items_info(self, items):
        scraped_items = []
        for item in items:
            data = {
                '업체명': item['name'],
                '업종': (',').join(item['category']),
                '별점': None,
                '리뷰갯수': item['reviewCount'],
                '전화번호': item['tel'],
                '도로명': item['roadAddress'],
                '지번': item['address'],
                '우편번호': None,
                'id': item['id']
            }
        scraped_items.append(data)
        return scraped_items
