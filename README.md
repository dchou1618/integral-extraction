# Integral Extraction

## Description

Recent work surrounding math problem solving using large language models (LLMs) has been centered around performance improvement by prompting or reprompting, data augmentations, or extending capabilities to multimodal settings. Although papers address evaluation of LLMs on math word problems and other comprehensive benchmarks such as GSM8k or the MATH dataset, not as many benchmark models on calculus-specific tasks. The gap can be addressed with a robust data creation pipeline, which is what this repository aims to accomplish. The main contribution is starter code for .

<img width="1196" alt="Screenshot 2024-09-23 at 10 47 54 AM" src="https://github.com/user-attachments/assets/3bc4dfac-5138-4f4a-8bd3-3dac7c4476b9">

## Setup 

Run `python latex_extraction.py -m ./message.txt -p ./prompt.txt -pp /path/to/poppler/Library/bin/` to extract the latex from MIT integration bee pdf at `./integrationbee` using poppler.

## Discussion

The current dataset creation pipeline can be improved through direct extraction of latex from the PDF when the text is vectorized. However, using vision models may be favored in scenarios where the math problem in the PDFs are contained in unstructured contents that is harder to extract reliably. This pipeline may also be adapted with an OCR layer to extract scanned problems in pdfs.
