from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Response
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile ,File, Form 
import asyncio
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.chrome.options import Options 

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import time


app = FastAPI()

# Configure CORS to allow any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Set this to True if you need to allow cookies and credentials
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestBody(BaseModel):
    url: str

def open_browser(url: str):
    driver = webdriver.Chrome()
    try: 
         driver.get(url)
         wait = WebDriverWait(driver, 1000)
         original_window = driver.current_window_handle
         print(f"Original window handle: {original_window}")
         time.sleep(5)  #
         all_windows = driver.window_handles
         print(f"All window handles: {all_windows}")
 
         for window in all_windows:
            if window != original_window:
                driver.switch_to.window(window)
                print(f"Switched to new window with handle: {window}")
                break

       # Now you can interact with the new window
         print(f"Current window title: {driver.title}")
        
        # Wait for a few seconds to let the page load (optional, can be customized)
         time.sleep(60)
         #input("Press Enter to quit...")
         #driver.quit()
 
        # Example of interacting with an element (if needed)
        # element = driver.find_element_by_tag_name("h1")
        # print(f"Page heading: {element.text}")
         #input("Press Enter to close the browser window...")
    except Exception as e:
     print(f"Error occurred: {e}")

@app.get("/")
async def root():
    return "Hello, Welcome to the Test Case Generator Fast APIs."

@app.post("/url")
async def launchurl(url: str = Form(default="") ):

    if not url:
        raise HTTPException(status_code=400, detail="Please enter url")
    
    url_new  = url
    driver = webdriver.Chrome()

    # Start the browser interaction in a background thread
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, open_browser, url)
    # Respond immediately to the API client
    return {"message": "Browser is open, press Enter in the terminal to close."}



if __name__ == "__main__":
    port = int(os.getenv("PORT", "5057"))
   # uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
