
import os
import datetime
from jinja2 import Template
import openai
import sillynamegenerator.sillynamegenerator as sillynamegenerator


def get_famous_names_from_date(month, day):

    my_api_key = os.environ.get("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=my_api_key)
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            store=True,
            messages=[
                {"role": "user", "content": f"Name 3 famous people born on {month} {day}. Just return the names as a comma separated list."}
            ]
        )
        name = completion.choices[0].message.content
    except openai.error.OpenAIError as e:
        print(f"An OpenAI error occurred: {e}")
        name = "Unknown"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        name = "Unknown"
    print(completion.choices[0].message)

    names = completion.choices[0].message.content
    names_list = names.split(",")
    print (names_list)
    return names_list


def get_silly_name(firstname, lastname):
    silly_name_gen = sillynamegenerator.PoopypantsSillyNameGenerator()

    return silly_name_gen.lookup(firstname, lastname)
    #print(f"{firstname} {lastname}'s silly name is {silly_name_gen.lookup(firstname, lastname)}")


def update_page(date, names_dict):
    template_str = """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Fun Fact</title>
    </head>
    <body>
        <h1>Today's date is: {{ date }}</h1>
        <h2>Fun Fact</h2>
        <p>Famous people born on this day:</p>
        <ul>
            {% for name in names_dict.keys() %}
                <li>{{ name }} aka {{ names_dict[name] }} </li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    template = Template(template_str)
    rendered_html = template.render(date=date, names_dict=names_dict)

    file_to_update = "output/index.html"
    with open(file_to_update, "w") as f:
        f.write(rendered_html)



def main():
    # Example usage:

    # print_poopy_name('Dav', 'Pilkey')
    # print_poopy_name('Lionel', 'Messi')
    # print_poopy_name('Cristiano', 'Rolaldo')
    # print_poopy_name('Albert', 'Einstein')

    year = datetime.datetime.now().strftime("%Y")

    month_name = datetime.datetime.now().strftime("%b")

    day_of_month = datetime.datetime.now().strftime("%d")

    print(f"Date: {month_name} {day_of_month}, {year}")

    famous_names_list = get_famous_names_from_date(month_name, day_of_month)

    names_dict = {}
    for name in famous_names_list:
        name = name.strip()
        name = name.rstrip(".")
        names_dict[name] = get_silly_name(name.split()[0], name.split()[1])
        print(f"{name} --> {names_dict[name]}")

    update_page(f"{month_name} {day_of_month}, {year}", names_dict)
    # Laugh hysterically

if __name__ == "__main__":
    main()
