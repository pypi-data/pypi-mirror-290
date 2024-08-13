import requests
import base64
from urllib.parse import urlparse
from pathlib import Path
import puremagic


def image_to_data_uri(image_path_or_url):
    # Determine if the input is a URL or a local file path
    parsed_url = urlparse(image_path_or_url)
    if parsed_url.scheme in ["http", "https"]:
        response = requests.get(image_path_or_url)
        content_type = response.headers.get("Content-Type", "image/jpeg")
        image_data = response.content
    else:
        # Assume it's a local file path
        path = Path(image_path_or_url)
        if not path.is_file():
            raise FileNotFoundError(f"The file at {image_path_or_url} does not exist.")
        with open(path, "rb") as f:

            content_types_ = puremagic.magic_stream(f)
            if content_types_:
                content_type = content_types_[0].mime_type
            else:
                return ""
            image_data = f.read()
        if not content_type:
            # Check this is in an allowed list?
            return "wtf"

        # Encode the image data to base64
        base64_data = base64.b64encode(image_data).decode("utf-8")

    # Create the data URI
    data_uri = f"data:{content_type};base64,{base64_data}"

    return data_uri
