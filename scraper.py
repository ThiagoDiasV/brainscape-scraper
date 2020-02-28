from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from sys import argv
from typing import List
import csv
from string import ascii_letters, digits
import os
from colorama import Fore
from random import choice


def create_webdriver_instance() -> WebDriver:
    """
    Creates an instance of Chrome webdriver
    """

    return webdriver.Chrome()


def get_main_url(chrome_webdriver: WebDriver, url: str) -> None:
    """
    Access main url from Brainscape website
    """

    chrome_webdriver.get(url)
    chrome_webdriver.maximize_window()


def login_website(chrome_webdriver: WebDriver, email: str, password: str) -> None:
    """
    Login at Brainscape
    """

    chrome_webdriver.find_element_by_class_name("login-link").click()
    chrome_webdriver.find_element_by_id("email").send_keys(email)
    chrome_webdriver.find_element_by_id("password").send_keys(password)
    chrome_webdriver.find_element_by_xpath(
        "//span[contains(@class, 'label') and text() = 'Log In']"
    ).click()
    sleep(3)


def find_parent_decks(
    chrome_webdriver: WebDriver, parent_deck_class: str
) -> List[WebElement]:
    """
    Find parent deck class > li
    """
    parent_deck_element = chrome_webdriver.find_element_by_class_name("user-packs")
    children = parent_deck_element.find_elements_by_tag_name("li")
    return children


def get_children_decks(
    chrome_webdriver: WebDriver, child: WebElement
) -> List[WebElement]:
    """
    Get the list of decks of each parent deck
    """
    parent_element = chrome_webdriver.find_element_by_class_name("deck-list")
    decks = parent_element.find_elements_by_class_name("dashboard-deck-row")
    return decks


def get_images_from_cards(card: WebElement, card_side: str) -> str:
    """
    If a card element has an image this function will get this img tag
    """
    try:
        parent_element = card.find_element_by_class_name(card_side)
        img_element = parent_element.find_element_by_tag_name("img")
        src_img = img_element.get_attribute("src")
        return f'\n<br><img src="{src_img}" >'
    except NoSuchElementException:
        return ""


def get_audio_from_cards(card:WebElement, card_side:str) -> str:
    """
    If a card element has audio with it this function will get this audio tag
    """
    try:
        parent_element = card.find_element_by_class_name(card_side)
        audio_element = parent_element.find_element_by_tag_name("audio")
        audio_source_element = audio_element.find_element_by_tag_name("source")
        src_audio = audio_source_element.get_attribute("src")
        return f'\n<audio controls><source src="{src_audio} type="audio/mpeg"></audio><br>'
    except NoSuchElementException:
        return ""


def get_card_text_img_audio_data(card: WebElement, card_side: str) -> str:
    """
    Get the card text
    """
    card_img_tag = get_images_from_cards(card, card_side)
    card_audio_tag = get_audio_from_cards(card, card_side)
    card_info = card.find_element_by_class_name(card_side)
    card_text = card_audio_tag + "\n" + card_info.text.replace("Play", "") + "\n" + card_img_tag
    return card_text


def get_file_name_for_csv_files(chrome_webdriver: WebDriver) -> str:
    """
    Get filename for csv file
    """
    raw_text = chrome_webdriver.find_element_by_class_name("new-modal-title").text
    valid_chars = f"-_.(){ascii_letters}{digits}ÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑáàâãéèêíïóôõöúçñ "
    filename = "".join(char for char in raw_text if char in valid_chars)
    return filename


def get_cards_info_of_deck(chrome_webdriver: WebDriver, deck: WebElement):
    """
    Get the cards info of each deck
    """

    try:
        glasses_icon = deck.find_element_by_class_name("ion-ios-glasses-outline")
        glasses_icon.click()
        sleep(2)
        cards_window_selection = chrome_webdriver.find_element_by_class_name(
            "preview-card-table"
        )
        cards_list = cards_window_selection.find_elements_by_class_name("preview-card")
        csv_file_name = get_file_name_for_csv_files(chrome_webdriver).replace("Preview", "").strip()
        path = os.getcwd()
        path_csv = f"{path}/csv_sem_utf8_delimiter_virgula/"
        try:
            os.mkdir(path_csv)
        except OSError:
            pass
        with open(f"{path_csv}{csv_file_name}.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            for card in cards_list:
                front_info = get_card_text_img_audio_data(card, "front")
                back_info = get_card_text_img_audio_data(card, "back")
                writer.writerow([front_info, back_info])
        color_options = [
                Fore.GREEN, Fore.MAGENTA, Fore.CYAN, Fore.BLUE, Fore.YELLOW
            ]
        print(choice(color_options) + f"{csv_file_name}.csv salvo!")

        chrome_webdriver.find_element_by_class_name("close-button").click()
    except NoSuchElementException:
        pass


def main():
    chrome = create_webdriver_instance()
    get_main_url(chrome, "https://www.brainscape.com/")
    login_website(chrome, argv[1], argv[2])
    children = find_parent_decks(chrome, "user-packs")
    for child in children:
        child.click()
        sleep(2)
        try:
            decks_list = get_children_decks(chrome, child)
        except NoSuchElementException:
            sleep(5)
            decks_list = get_children_decks(chrome, child)
        for deck in decks_list:
            try:
                get_cards_info_of_deck(chrome, deck)
            except NoSuchElementException:
                sleep(5)
                get_cards_info_of_deck(chrome, deck)

    print(Fore.GREEN + "Terminei!")
    sleep(60)


main()
