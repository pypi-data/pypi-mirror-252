# TODO
* 여유될때, extractor 부분 좀더 구조화 가능.
* 또한, 각 Resource에서 비디오, 채널등 특화된 추출 코드들을 Extractor로 옮기고, YoutubeBasicInfoExtractor를 상속해서 구성하면
  훨씬 깔끔할듯
* 필요하면, TorNetwork를 이용해서 접근 IP를 감출 수 있음


# References - thanks
[**pyyoutube**]  https://github.com/sns-sdks/python-youtube/tree/a531987cf5f426170399f227ca07a85ecba1358f
[Youtube-Local] https://github.com/search?q=repo%3Auser234683%2Fyoutube-local%20request_comments&type=code
[Youtube-DL] https://github.com/ytdl-org/youtube-dl/blob/be008e657d79832642e2158557c899249c9e31cd/youtube_dl/extractor/common.py#L1014
[Youtube-Crawler] https://github.com/jaryeonge/youtube-crawler/blob/5af1421ed4a76a1b9ca57ea968c936e63395675f/src/crawling_module/vod_meta.py#L141
[Youtube-Search-Python] https://github.com/GHOSTEPROG-OFFICIAL/youtube-search-python/blob/main/youtubesearchpython/core/comments.py
[Mining] https://github.com/medialab/minet/tree/82d862dbd434d6535a6bec23cfb7c35d864440c0

# Update
```bash
pip install --upgrade ytvs
```


# Build and publish
```bash
poetry build  # Build
python -m twine upload --skip-existing dist/*   # Deployment
```

