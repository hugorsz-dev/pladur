# Pladur - Non-selectable text analyzed with AI.

This system allows you to make queries through AI to the text displayed on the screen of a specific window. It is aimed at video games or other types of programs where the text is not selectable. To achieve this goal, it uses the Tesseract Open Source OCR Engine and its Python library, pythesseract.

## Installation of Tesseract OCR
> [!warning]
> Although the queries will be executed through an API, the image-to-text conversion using Tesseract will be performed locally. Therefore, if you do not have a computer with sufficient power, you may experience slowdowns
- To do this, you need to have the program installed in a known location, which should be listed in the config.json file. Downloadale at: https://github.com/UB-Mannheim/tesseract/wiki
- And within that folder, in "tessdata" should be the "spa.traineddata" file (or the language of your preference), downloadable at: https://github.com/tesseract-ocr/tessdata

## Configuration
- The file `config.json` will establish the path to be accessed to run Tesseract, the query made by the AI, and the name of the window. It is essential that it is correctly filled out to avoid errors during execution.
- The file `headers.json` contains information regarding the API through which the flow of information will be redirected. The format is in RAPID API format. Any system with a compatible format can be used, or you can modify the code as needed!

## Execution
With the program open, run main.py. Every time the window loses focus, the command terminal will return the output from the AI.

## Diagram 
The operation of the program can be summarized in the following diagram.

![diagram](https://github.com/hugoruizsanchez/pladur/assets/120595249/6bf4717c-1140-4dd5-9226-573d65e974bd)

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.
