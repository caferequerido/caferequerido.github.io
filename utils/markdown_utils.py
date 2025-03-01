def generate_markdown(the_date, names_dict):

        # <h1>Today's date is: {{ the_date }}</h1>
        # <h2>Fun Fact</h2>
        # <p>Famous people born on this day:</p>
        # <ul>
        #     {% for name in names_dict.keys() %}
        #         <li>{{ name }} aka {{ names_dict[name] }} </li>
        #     {% endfor %}
        # </ul>

    markdown = f"# Today's date is: {the_date}\n\n## Fun Fact\n\nFamous people born on this day:\n\n"
    for name in names_dict.keys():
        markdown += f"- {name} aka {names_dict[name]}\n"
    return markdown

