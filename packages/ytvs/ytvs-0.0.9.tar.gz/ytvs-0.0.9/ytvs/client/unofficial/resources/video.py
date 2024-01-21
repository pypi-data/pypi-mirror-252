import re

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import NoSuchElementException
from seleniumwire import webdriver as wired_webdriver
from selenium import webdriver
from seleniumwire import webdriver, utils
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


from ytvs.client.unofficial.resources.base_resource import Resource
from ytvs.extractor import YoutubeBasicInfoExtractor
from ytvs.utils import try_get, str_to_int, _search_attribute, _search_attributes


class VideoResource(Resource):
    KIND = 'youtube#video'

    def get_video_by_id(self, video_id: str):
        """
        주어진 비디오 ID에 대한 YouTube 비디오 정보를 조회.
        :param video_id: 정보를 가져올 비디오의 ID.
        :return: 파싱된 비디오 정보.
        """
        # 1. 영상 페이지 요청
        data = self._request_data(video_id)

        # 2. 영상 페이지에서 데이터 추출
        yt_initial_data = YoutubeBasicInfoExtractor.extract_yt_initial_data(data)

        # 3. 데이터 분석 및 파싱
        parsed_data = self._parse_video_data_from_initial_data(yt_initial_data)
        parsed_data_from_html = self._parsed_video_data_from_html_txt(data)

        # 4. 추가 데이터 병합
        parsed_data['items'][0]['id'] = video_id
        parsed_data['items'][0]['snippet']['publishedAt'] = parsed_data_from_html['published_date']
        # parsed_data['id'] = video_id

        # 5. 반환
        return parsed_data

    def _request_data(self, video_id: str):
        """
        YouTube 비디오 페이지의 HTML 데이터를 요청.
        :param video_id: 요청할 비디오의 ID.
        :return: 비디오 페이지의 HTML 텍스트를 반환.
        """
        # 1. Video resource 요청 URL 생성
        url = self.build_video_resource_url(video_id)

        # # 2. Video 페이지 요청 및 데이터 추출
        return self._client.fetch_url(url).decode("utf-8")
        # @TODO: Selenium 으로 유투브 영상 재생 페이지 호출하는 코드. 이 코드를 Client 로 옮겨야함.
        # base_url = self.build_video_resource_url(video_id)
        # options = webdriver.ChromeOptions()
        # options.add_argument('--disable-dev-shm-usage')
        # is_headless = True
        # if is_headless is True:
        #     options.add_argument('headless')
        #     options.add_argument('--no-sandbox')
        #
        # # driver = webdriver.Chrome(options=options)
        # driver = wired_webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # driver.get(base_url)
        # wait = WebDriverWait(driver, 100)
        # h3 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.ytp-time-duration")))
        # video_duration = h3.text
        #
        # html_text = driver.page_source
        return html_text

    def _parsed_video_data_from_html_txt(self, html_text):
        # *******
        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        # date published
        published_date_text = soup.find("meta", itemprop="datePublished")['content']
        # get the duration of the video
        # 광고 영상때문에, HTML 페이지에서는 확실한 영상의 재생시간 획득을 보장할수가 없음...
        # video_duration_text = soup.find("span", {"class": "ytp-time-duration"}).text
        return {'published_date': published_date_text}

    def _parse_video_data_from_initial_data(self, initial_data):
        """
        초기 데이터에서 YouTube 비디오 데이터를 파싱.
        :param initial_data: YouTube 비디오 페이지에서 추출된 초기 데이터.
        :return: 파싱된 비디오 데이터를 반환.
        """
        # 1. 데이터 분석 및 파싱
        contents = try_get(initial_data,
                           lambda x: x['init_data']['contents']['twoColumnWatchNextResults']['results']['results'][
                               'contents'], list) or []

        # 2. Content 획득
        video_primary_video_renderer = _search_attribute(contents, "videoPrimaryInfoRenderer")
        if video_primary_video_renderer:
            video = YoutubeBasicInfoExtractor.extract_video(video_primary_video_renderer)
        else:
            video = {}
        video_secondary_info_renderer = _search_attribute(contents, "videoSecondaryInfoRenderer")
        if video_secondary_info_renderer:
            description = try_get(video_secondary_info_renderer,
                                  lambda x: x['attributedDescription']['content'], str)
            owner = try_get(video_secondary_info_renderer,
                            lambda x: x['owner']['videoOwnerRenderer'], dict)
            owner = YoutubeBasicInfoExtractor.extract_video_owner_renderer(owner)
        else:
            description = None
            owner = {}

        item_section_renderers = _search_attributes(contents, 'itemSectionRenderer')
        comments_header_renderer = _search_attribute(item_section_renderers, "commentsEntryPointHeaderRenderer", max_depth=6)
        comments_header = YoutubeBasicInfoExtractor.extract_comments_header_renderer(comments_header_renderer)

        return {
            'etag': None,
            'kind': 'youtube#videoListResponse',
            'items': [{
                'kind': self.KIND,
                'localizations': None,
                'etag': None,
                'snippet': {
                    'title': try_get(video, lambda x: x['title'], str),
                    'categoryId': None,
                    'channelId': try_get(owner, lambda x: x['channel_id'], str),
                    'channelTitle': try_get(owner, lambda x: x['title'], str),
                    'description': description,
                    'liveBroadcastContent': None,
                    'localized': None,
                    'publishedAt': try_get(video, lambda x: x['published_at'], str),
                    'tags': [],
                    'thumbnails': None,
                    'hashtags': try_get(video, lambda x: x['super_title_links'], list)
                },
                'statistics': {
                    'dislikeCount': None,
                    'commentCount': try_get(comments_header, lambda x: x['comment_count']),
                    'likeCount': try_get(video, lambda x: x['like_count']),
                    'viewCount': try_get(video, lambda x: x['view_count']),
                }
            }],
            'nextPageToken': None,
            'prevPageToken': None,
            'pageInfo': {
                'totalResults': 1,
                'resultsPerPage': 1
            }
        }
