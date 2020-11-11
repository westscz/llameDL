youtube_vendor = lambda url: "youtube" in url


def get_supported_vendors() -> []:
    return [youtube_vendor]
