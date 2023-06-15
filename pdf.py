import json
from jinja2 import Environment, FileSystemLoader
import pdfkit


def render_pdf(data):
    """
       Render a PDF file from an HTML template.

       Args:
           data (dict): The data to be passed to the HTML template.

       Returns:
           bool: True if the PDF is generated successfully, False otherwise.
    """
    # Load the HTML template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('files/template_r.html')

    # Render the template with JSON data
    rendered_html = template.render(data=data)

    # Save the rendered HTML to a temporary file
    with open('temp.html', 'w') as temp_file:
        temp_file.write(rendered_html)

    # Convert the HTML to PDF
    pdfkit.from_file('temp.html', 'resume.pdf')

    # Clean up the temporary file
    import os
    os.remove('temp.html')

    print("PDF generated successfully.")
    return True