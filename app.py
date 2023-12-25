import uvicorn
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import common.config
from parsers.template import template_parser
from extraction.extraction import result_generator
import json
import asyncio

app = FastAPI(debug=common.config.DEBUG)

@app.post('/extraction')
# @logger.catch
async def detection(file: UploadFile = File(...), param: str = File(default=None)):
    data_param = json.loads(param)
    basic_information_template, matrix_template, brand = template_parser(data_param)
    print(matrix_template)
    contents = await file.read()
    result = result_generator(contents.decode('utf-8'), basic_information_template, matrix_template, brand)
    return result

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
