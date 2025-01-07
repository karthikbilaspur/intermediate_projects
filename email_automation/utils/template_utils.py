from jinja2 import Environment, FileSystemLoader

def render_template(template_loader, template_name, data):
    template = template_loader.get_template(template_name)
    return template.render(data)