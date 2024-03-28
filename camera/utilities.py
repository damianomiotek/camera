import platform
import validators

video_formats = ["mp4", "mov", "wmv", "avi", "webm", "avchd ", "swf"]
image_formats = [".avif", ".gif", ".jpg", ".jpeg", ".png", ".svg", ".webp", "PNG"]


def get_directory_separator():
    if platform.system() == "Linux":
        return "/"
    elif platform.system() == "Windows":
        return "\\"
    else:
        return "/"


def check_url_is_valid(url):
    return ("https://www.youtube.com/watch" in url or "https://www.youtube.com/shorts/" in url) and validators.url(url)
