import re
import sys

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


    
def new_entry(title, content):
    """
    Creates a new encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    an error is raised.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        sys.exit("Error: File already exists with that title!")
    
    else:
        # Add title to md file
        md_title = f"#{title}\n\n"
        new_content = md_title + content
        default_storage.save(filename, ContentFile(new_content))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
