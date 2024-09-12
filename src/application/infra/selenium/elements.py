from selenium.webdriver.common.by import By
from src.domain.entity.element import Element

input_for_new_conversations = Element(
  name="Input for new conversations",
  element_search="//span[@data-icon='new-chat-outline']",
  type=By.XPATH
)

info_not_in_list_contact = Element(
  name="element infomation",
  element_search='_ajzf',
  type=By.CLASS_NAME
)

input_write_message = Element(
  "input message",
  element_search='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]',
  type=By.XPATH
)

messages_conversation = Element(
  "all message",
  element_search="_akbu",
  type=By.CLASS_NAME
)

qrcode_image = Element(
  "qrcode_image",
  element_search='//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas',
  type=By.XPATH,
  time=30
)

page_wpp = Element(
  "page_wpp",
  element_search='//*[@id="app"]/div/div[2]/div[3]/header/header/div/div[1]/h1',
  type=By.XPATH,
  time=3
)

body = Element(
  "body",
  element_search='body',
  type=By.TAG_NAME
)