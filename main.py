
import os
import datetime
from jinja2 import Template
import openai.OpenAI
import sillynamegenerator.sillynamegenerator as sillynamegenerator


def get_famous_name_from_date(month, day):

    my_api_key = os.environ.get("OPENAI_TOKEN")
    client = OpenAI(
    api_key=my_api_key)

    completion = client.chat.completions.create(
    model="gpt-4o",
    store=True,
    messages=[
        {"role": "user", "content": f"Name a famous person born on {month} {day}. Just return the name."}
    ]
    )
    name = completion.choices[0].message.content

    return name


def get_silly_name(firstname, lastname):
    silly_name_gen = sillynamegenerator.PoopypantsSillyNameGenerator()

    return silly_name_gen.lookup(firstname, lastname)
    #print(f"{firstname} {lastname}'s silly name is {silly_name_gen.lookup(firstname, lastname)}")


def update_page_md(date, famous_name, silly_name):
    file_to_update = "output/index.md"

    with open(file_to_update, "w") as f:
        f.write(f"### Today's date is: {date}\n")
        f.write(f"### Fun Fact\n")
        f.write(f"{famous_name} was born on this date.\n\n")
        f.write(f"Their silly name is {silly_name}\n")

    # print(f"Today's date is: {date}")
    # print(f"{famous_name} was born on this date.")
    # print(f"Their silly name is {silly_name}")

def update_page(date, famous_name, silly_name):
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
        <p>{{ famous_name }} was born on this date.</p>
        <p>Their silly name is {{ silly_name }}</p>
    </body>
    </html>
    """
    template = Template(template_str)
    rendered_html = template.render(date=date, famous_name=famous_name, silly_name=silly_name)

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


    famous_person_name = get_famous_name_from_date(month_name, day_of_month)
    #famous_person_name = "Albert Einstein"
    famous_silly_name = get_silly_name(famous_person_name.split()[0], famous_person_name.split()[1])

    update_page(f"{month_name} {day_of_month}, {year}", famous_person_name, famous_silly_name)
    # Laugh hysterically

if __name__ == "__main__":
    main()
