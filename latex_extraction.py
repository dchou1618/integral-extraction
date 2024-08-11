import openai
from dotenv import dotenv_values
import base64
import certifi
import httpx
from PIL import Image
import json
from tqdm import tqdm

import os
import requests
import base64
from io import BytesIO
import argparse
import time
import logging

from openai import AzureOpenAI


from pdf2image import convert_from_path
import os


# Configuration
config = dotenv_values(".env")
GPT4V_KEY = config["OPENAI_API_KEY"]


def PIL_to_image(pil_img):
    buffer = BytesIO()
    pil_img.save(buffer, format="JPEG")
    encoded_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_string


def generate(system_message, prompt, encoded_image, api_key, api_endpoint):
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    payload = {
        "messages": [
            {
                "role": "system",
                "content": system_message,
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    },
                ],
            },
        ],
        "temperature": 0,
    }

    response = requests.post(api_endpoint, headers=headers, json=payload)
    time.sleep(1.0)
    return response.json()["choices"][0]["message"]["content"]


def extract_latex(
    pdf_path, poppler_path, prompt, system_message, api_key, api_endpoint
):
    response = dict()
    for pdf_fname in os.listdir(pdf_path):
        start = time.time()
        curr_path = os.path.join(pdf_path, pdf_fname)
        images_from_path = convert_from_path(curr_path, poppler_path=poppler_path)
        base64_lst = [PIL_to_image(pil_img) for pil_img in images_from_path]
        latex_lst = [
            generate(system_message, prompt, encoded_image, api_key, api_endpoint)
            for encoded_image in tqdm(base64_lst)
        ]
        response[pdf_fname] = latex_lst
        end = time.time()
        logger.info(
            f"{pdf_fname} took {end-start} seconds to run.\nIntegral Latex:{latex_lst}\n\n"
        )
    with open("integrals-2.json", "w") as f:
        json.dump(response, f)
    return response


def read_from_file(fname):
    with open(fname, "r") as f:
        contents = f.read()
    return contents


if __name__ == "__main__":
    logger = logging.getLogger("Latex Extraction")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    parser = argparse.ArgumentParser(
        prog="Latex Extraction",
        description="Extracts Latex for Integrals in Images",
    )
    parser.add_argument("-p", "--prompt")
    parser.add_argument("-m", "--message")
    parser.add_argument("-pp", "--poppler_path")
    config = dotenv_values(".env")
    GPT4V_KEY = config["OPENAI_API_KEY"]
    GPT4V_ENDPOINT = "https://dev-eastus2-bia-openai-01.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

    args = parser.parse_args()
    sys_msg = read_from_file(args.message)
    prompt = read_from_file(args.prompt)
    poppler_path = args.poppler_path
    extract_latex(
        "./integrationbee", poppler_path, prompt, sys_msg, GPT4V_KEY, GPT4V_ENDPOINT
    )
