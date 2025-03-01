from jinja2 import Template

def generate_html(the_date, names_dict):
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
                <li>{{ name }} aka {{ names_dict[name] }} </li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    template = Template(template_str)
    rendered_html = template.render(the_date=the_date, names_dict=names_dict)

    return rendered_html


def save_html_page(content, output_file):

    with open(output_file, "w") as f:
        f.write(content)
