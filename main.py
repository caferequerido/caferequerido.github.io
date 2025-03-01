
import os
import datetime
import openai
import sillynamegenerator.sillynamegenerator as sillynamegenerator
from utils import openai_utils, html_utils, discord_utils, markdown_utils


def get_silly_name(firstname, lastname):
    silly_name_gen = sillynamegenerator.PoopypantsSillyNameGenerator()

    return silly_name_gen.lookup(firstname, lastname)
    #print(f"{firstname} {lastname}'s silly name is {silly_name_gen.lookup(firstname, lastname)}")




def main():

    year = datetime.datetime.now().strftime("%Y")
    month_name = datetime.datetime.now().strftime("%b")
    day_of_month = datetime.datetime.now().strftime("%d")

    print(f"Date: {month_name} {day_of_month}, {year}")

    ai_prompt = f"Name 3 famous people born on {month_name} {day_of_month}. Just return the names as a comma separated list."

    names = openai_utils.openai_chat(ai_prompt)
    names_list = names.split(",")
    names_dict = {}
    for name in names_list:
        name = name.strip()
        name = name.rstrip(".")
        names_dict[name] = get_silly_name(name.split()[0], name.split()[1])
        print(f"{name} --> {names_dict[name]}")

    html_content = html_utils.generate_html(f"{month_name} {day_of_month}, {year}", names_dict)
    html_utils.save_html_page(html_content, "output/index.html")
    markdown_content = markdown_utils.generate_markdown(f"{month_name} {day_of_month}, {year}", names_dict)
    discord_utils.send_discord_message(markdown_content)

if __name__ == "__main__":
    main()
