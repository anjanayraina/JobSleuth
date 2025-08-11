import requests
from fastapi import UploadFile, File
from PyPDF2 import PdfReader
from io import BytesIO

async def convert_pdf(file: UploadFile):
    try:
        pdf_bytes = await file.read()

        reader = PdfReader(BytesIO(pdf_bytes))
        total_pages = len(reader.pages)
        print(f"Total pages found: {total_pages}")

        images_in_memory = []

        for page in range(1, total_pages + 1):
            response = requests.post(
                'https://ocr-service-eyu3.onrender.com/ocr/pdf-to-img',
                params={'page_number': page},
                files={'file': (file.filename, pdf_bytes, file.content_type)}
            )

            if response.status_code == 200:
                img_bytes = BytesIO(response.content)
                images_in_memory.append(img_bytes)
                print(f"Stored page {page} in memory")
            else:
                print(f"Failed for page {page}:", response.status_code, response.text)

        return images_in_memory

    except Exception as e:
        print("Error:", e)
        return []

async def image_to_json(file: File()):
    pass
    return []