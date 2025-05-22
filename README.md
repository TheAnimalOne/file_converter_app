### File Converter App
A fairly simple GUI app that converts files between different formats. Aims to replicate those file conversion websites, like png2pdf, except this runs locally.

To use the app, either run the `pdf_converter/file_converter.py` file or use the `pdf_converter/file_converter.exe` file. The rest of the code is in the `pdf_converter/classes` folder.

The app is basically a Pillow wrapper with a GUI made using PyQt6. The logo was generated using Microsoft Copilot. The exe was made using auto-py-to-exe.

Currently supports converting file/s from:
- png
- jpg

Currently supports converting file/s into:
- png
- jpg
- pdf
- combined pdf
