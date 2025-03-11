
import datetime
import markdownify
from jinja2 import Template
import sillynamegenerator.sillynamegenerator as sillynamegenerator
from utils import file_utils, openai_utils, discord_utils, markdown_utils


def get_silly_name(firstname, lastname):
    silly_name_gen = sillynamegenerator.PoopypantsSillyNameGenerator()

    return silly_name_gen.lookup(firstname, lastname)
    #print(f"{firstname} {lastname}'s silly name is {silly_name_gen.lookup(firstname, lastname)}")


def generate_html(the_date, names_dict, description_dict, birth_year_dict):
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
        <h2>Fun Fact</h2>
        <p>Famous people born on this day:</p>
        <ul>
            {% for name in names_dict.keys() %}
                <li>{{ name }} aka {{ names_dict[name] }} 
                <ul>
                <li><p>Born in the year {{ birth_year_dict[name] }}</p></li>
                <li><p>{{ description_dict[name] }}</p></li>
                </ul>
                </li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    template = Template(template_str)
    rendered_html = template.render(the_date=the_date, names_dict=names_dict, description_dict=description_dict, birth_year_dict=birth_year_dict)

    return rendered_html


def gen_famous_people_list():

    year = datetime.datetime.now().strftime("%Y")
    month_name = datetime.datetime.now().strftime("%b")
    day_of_month = datetime.datetime.now().strftime("%d")

    print(f"Date: {month_name} {day_of_month}, {year}")

    ai_prompt_to_get_names = f"Name 3 famous people born on {month_name} {day_of_month}. Just return the names as a comma separated list."
    ai_prompt_for_description = "Generate a 1 sentence simple description of person"
    ai_prompt_for_birth_year = "What year was this person born, just return the year."

    names = openai_utils.openai_chat(ai_prompt_to_get_names)
    names_list = names.split(",")
    names_dict = {}
    description_dict = {}
    birth_year_dict = {}
    for name in names_list:
        name = name.strip()
        name = name.rstrip(".")
        try:
            first = name.split()[0]
            last = name.split()[1]
        except IndexError:
            # if there's an exception its likely because the person only has 1 name
            first = name.split()[0]
            last = "Doe"

        names_dict[name] = get_silly_name(first, last)
        description_dict[name] = openai_utils.openai_chat(f"{ai_prompt_for_description} {name}")
        birth_year_dict[name] = openai_utils.openai_chat(f"{ai_prompt_for_birth_year} {name}")
        print(f"{name} --> {names_dict[name]}")
        print(f"            --> {description_dict[name]}")
        print(f"            --> {birth_year_dict[name]}")

    html_content = generate_html(f"{month_name} {day_of_month}, {year}", names_dict, description_dict, birth_year_dict)
    file_utils.save_file(html_content, "output/index.html")
    markdown_content = markdown_utils.convert_html_to_markdown(html_content)
    file_utils.save_file(markdown_content, "output/index.md")

    #markdown_content = markdown_utils.generate_markdown(f"{month_name} {day_of_month}, {year}", names_dict, description_dict, birth_year_dict)
    #print(markdown_content)
    #
    # 
    discord_utils.send_discord_message(markdown_content)
