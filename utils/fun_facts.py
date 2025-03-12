
import datetime
import markdownify
import json
from jinja2 import Template
import sillynamegenerator.sillynamegenerator as sillynamegenerator
from utils import file_utils, openai_utils, discord_utils, markdown_utils


def get_silly_name(firstname, lastname):
    silly_name_gen = sillynamegenerator.PoopypantsSillyNameGenerator()

    return silly_name_gen.lookup(firstname, lastname)
    #print(f"{firstname} {lastname}'s silly name is {silly_name_gen.lookup(firstname, lastname)}")


def generate_final_html(the_date, content):
    template_str = """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Today Things</title>
    </head>
    <body>
        <h1>Today's date is: {{ the_date }}</h1>

        {{ content }}

    </body>
    </html>
    """
    template = Template(template_str)
    rendered_html = template.render(the_date=the_date, content=content)

    return rendered_html


def generate_section_html(section_heading, people_list):
    template_str = """
        <h4>{{ section_heading }}:</h4>
        <ul>
            {% for person in people_list %}
                <li>{{ person['name'] }} aka {{ person['silly_name'] }} 
                <ul>
                <li><p>Born in the year {{ person['birth_year'] }}</p></li>
                <li><p>{{ person['description'] }}</p></li>
                </ul>
                </li>
            {% endfor %}
        </ul>
    """
    template = Template(template_str)
    rendered_html = template.render(section_heading=section_heading, people_list=people_list)

    return rendered_html


def gen_people_list(section_heading, prompt):

    response = openai_utils.openai_chat_structured(prompt)

    print(f"Raw Output : {response}\n")
    # Decode the JSON string into a Python dictionary and get the list of people
    people_list_orig = json.loads(response)["people"]
    people_list = []

    for person in people_list_orig:

        name = person['name'].strip()
        name = name.rstrip(".")
        try:
            first = name.split()[0]
            last = name.split()[1]
        except IndexError:
            # if there's an exception its likely because the person only has 1 name
            first = name.split()[0]
            last = "Doe"
        silly_name = get_silly_name(first, last)
        birth_year = person['birth_year']
        description = person['description']
        people_list.append({"name": name, "silly_name": silly_name, "birth_year": birth_year, "description": description})


    for person in people_list:

        print(f"Name: {person['name']}")
        print(f"Silly Name: {person['silly_name']}")
        print(f"Birth Year: {person['birth_year']}")
        print(f"Description: {person['description']}")
        print("\n")

    html_content = generate_section_html(section_heading, people_list)
    return html_content


def generate_file_scientist(post_to_discord=False):

    year = datetime.datetime.now().strftime("%Y")
    month_name = datetime.datetime.now().strftime("%b")
    day_of_month = datetime.datetime.now().strftime("%d")

    print(f"Date: {month_name} {day_of_month}, {year}")

    ai_prompt_to_get_names_scientist = f"Name 3 famous scientists born on {month_name} {day_of_month}"
    section_heading_scientist = f"Famous scientists born on this day"

    html_content_scientist = gen_people_list(section_heading_scientist, ai_prompt_to_get_names_scientist)    


    # ai_prompt_to_get_names_athelete = f"Name 3 famous athletes born on {month_name} {day_of_month}"
    # section_heading_athlete = f"Famous athletes born on this day"

    # html_content_athlete = gen_people_list(section_heading_athlete, ai_prompt_to_get_names_athelete)    


    # html_content_combined = html_content_scientist + html_content_athlete
    html_content_combined = html_content_scientist

    html_content_final = generate_final_html(f"{month_name} {day_of_month}, {year}", html_content_combined)
    file_utils.save_file(html_content_final, "output/index_scientist.html")
    markdown_content = markdown_utils.convert_html_to_markdown(html_content_final)
    file_utils.save_file(markdown_content, "output/index_scientist.md")

    if post_to_discord:
        discord_utils.send_discord_message(markdown_content)


def generate_file_athlete(post_to_discord=False):

    year = datetime.datetime.now().strftime("%Y")
    month_name = datetime.datetime.now().strftime("%b")
    day_of_month = datetime.datetime.now().strftime("%d")

    print(f"Date: {month_name} {day_of_month}, {year}")

    # ai_prompt_to_get_names_scientist = f"Name 3 famous scientists born on {month_name} {day_of_month}"
    # section_heading_scientist = f"Famous scientists born on this day"

    # html_content_scientist = gen_people_list(section_heading_scientist, ai_prompt_to_get_names_scientist)    


    ai_prompt_to_get_names_athelete = f"Name 3 famous athletes born on {month_name} {day_of_month}"
    section_heading_athlete = f"Famous athletes born on this day"

    html_content_athlete = gen_people_list(section_heading_athlete, ai_prompt_to_get_names_athelete)    


    # html_content_combined = html_content_scientist + html_content_athlete
    html_content_combined = html_content_athlete

    html_content_final = generate_final_html(f"{month_name} {day_of_month}, {year}", html_content_combined)
    file_utils.save_file(html_content_final, "output/index_athlete.html")
    markdown_content = markdown_utils.convert_html_to_markdown(html_content_final)
    file_utils.save_file(markdown_content, "output/index_athlete.md")

    if post_to_discord:
        discord_utils.send_discord_message(markdown_content)


def generate_files(post_to_discord=False):

    generate_file_scientist(post_to_discord)
    generate_file_athlete(post_to_discord)  

