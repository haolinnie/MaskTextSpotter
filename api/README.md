# API for Mask TextSpotter


## API Endpoints

- [Upload image](#upload)
- [Download image](#download)


### Upload

Upload an image for inference by posting the PNG image to this endpoint.

URL: `baseURL/api/upload`

Type: `POST`

Returns two fields:
    * words: words spotted in the picture
    * img: An image name (use the [download](#download) endpoint to download it)

```json
{
    "words": ["hello", "world"]
    "img": "abcdefg.png"
}

```

### Download

Download the inference image with annotated texts. Append the image name to the url below.

URL: `baseURL/api/download/<image name>`

Type: `GET`
