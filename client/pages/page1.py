from codecs import encode

import pandas as pd
from navigation import make_sidebar
import aiohttp
import asyncio
import streamlit as st
from tempfile import NamedTemporaryFile
from constants import Constants

make_sidebar()



async def upload_file(url, tmp_file):
    async with aiohttp.ClientSession() as session:
        headers = {'Authorization': f"Bearer {st.session_state["access"]}"
        ,
            'Content-type': Constants.content_type.format(Constants.boundary)
        }
        dataList = []
        dataList.append(encode('--' + Constants.boundary))
        dataList.append(encode('Content-Disposition: form-data; name=file_uploaded; filename={0}'.format(Constants.file_name)))
        fileType = 'text/csv'
        dataList.append(encode('Content-Type: {}'.format(fileType)))
        dataList.append(encode(''))
        dataList.append(tmp_file.read())
        dataList.append(encode('--' + Constants.boundary + '--'))
        dataList.append(encode(''))
        body = b'\r\n'.join(dataList)
        payload = body
        async with session.post(url, data=payload, headers=headers) as response:
            return await response.json()


async def main(tmp_file):
    response_text = await upload_file(Constants.upload_url, tmp_file)
    if isinstance(response_text, dict) and response_text.get('data'):
        df = pd.DataFrame(response_text.get('data'))
        st.success("Success")
        st.write(df)
    else:
        st.error(response_text)

csv_file = st.file_uploader("Upload an csv file", type=["csv"])



if csv_file is not None:
    with NamedTemporaryFile() as tmp_file:
        tmp_file.write(csv_file.read())
        tmp_file.seek(0)
        asyncio.run(main(tmp_file))