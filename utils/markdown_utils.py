from markdownify import MarkdownConverter

def convert_html_to_markdown(html_content):
    #markdown_content = markdownify.markdownify(html_content)
    # use only * for bullets since + doesn't work in discord
    md_convert = MarkdownConverter(bullets='*')
    markdown_content = md_convert.convert(html_content)
    return markdown_content
