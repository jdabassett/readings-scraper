from playwright.sync_api import sync_playwright
import pyperclip
from dotenv import load_dotenv
import os


load_dotenv()


def scrap_code_fellows_reading(str_url:str, str_username:str, str_password:str):
    with sync_playwright() as p:
        obj_browser = p.chromium.launch()
        obj_page = obj_browser.new_page()
        obj_page.goto(str_url)
        obj_page.locator('xpath=//*[@id="pseudonym_session_unique_id"]').fill(str_username)
        obj_page.wait_for_timeout(100)
        obj_page.locator('xpath=//*[@id="pseudonym_session_password"]').fill(str_password)
        obj_page.wait_for_timeout(100)
        # obj_page.screenshot(path="reading0.png",full_page=True)
        obj_page.locator('xpath=//*[@id="login_form"]/div[3]/div[2]/input').click()
        obj_page.wait_for_timeout(5000)
        # obj_page.screenshot(path="reading1.png", full_page=True)

        # retrieve title
        str_title = obj_page.frame_locator('xpath=//*[@id="discussion_topic"]/div[1]/div[2]/div/p[1]/iframe').get_by_role("heading").all_inner_texts()[0].replace("Readings: ","")

        # retrieve all the links
        list_link_locators = obj_page.frame_locator('xpath=//*[@id="discussion_topic"]/div[1]/div[2]/div/p[1]/iframe').get_by_role("link").all()
        list_links_tup = []
        for link_locator in list_link_locators:
            str_link = link_locator.inner_text()
            str_url = link_locator.get_attribute('href')
            list_links_tup.append((str_link,str_url))

        # retrieve all the questions
        list_questions = obj_page.frame_locator('xpath=//*[@id="discussion_topic"]/div[1]/div[2]/div/p[1]/iframe').get_by_role("listitem").all_inner_texts()

        obj_browser.close()
    return str_title, list_links_tup, list_questions


def format_text(title, list_links, list_question):
    str_return = ""
    str_return += f"\n# **Reading Notes: {title}**\n\n"
    str_return += f"\n## Why are these reading important?\n\n```\n```\n\n"
    for link in list_links:
        str_return += f"\n---\n\n## [**{link[0]}:**]({link[1]})\n\n"
    str_return += f"\n---\n\n## READING QUESTIONS:\n\n"
    for question in list_question:
        str_return += f"\n\t1. Prompt: {question}\n\t\t*Solution:\n\n"
    str_return += f"---\n\n## **What I want to learn more about:**\n\n\t1.\n\n---\n---\n---\n"
    return str_return


if __name__ == "__main__":
    str_username = os.getenv('canvas_username')
    str_password = os.getenv('canvas_password')
    str_clipboard = str(pyperclip.paste())
    if "https" in str_clipboard or "canvas" in str_clipboard or "discussion_topics" in str_clipboard:
        str_title, list_links_tup, list_questions = scrap_code_fellows_reading(str_clipboard, str_username, str_password)
        str_full = format_text(str_title, list_links_tup, list_questions)
        with open('reading.md',"w") as file:
            file.write(str_full)
    else:
        raise ValueError('Must copy url to Code Fellows Reading on from Canvas.')
