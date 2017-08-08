# Contributing to Arguman

Looking to contribute something to Arguman? We're happy to hear that!
 
This document describes how you can help and guides you through the process.
 
When contributing to this repository, please first [create a relevant issue](https://github.com/arguman/arguman.org/issues/new). 
It will signal others than you want to tackle given challenge and it will be a place to discuss changes. If you then want to contribute to the project with code or translations then pull requests are the standard mechanism.
 
## Pull request process

1. Create an issue for the things you want to do
2. Fork the repo and create a feature branch following `feature/n_issue_slug` template, ie. `feature/329_document_contributing`
3. Make commits of logical units.
4. Write a good commit message
    ```
    #329 Document contributing process

    Contributing.md serves as a go-to resources for everyone willing to
    contribute to the project. It should be clear and document most common
    cases, such as:
    
    - explaining pull request process
    - guidelines for creating issues
    - documenting translation process
    
    [The first line in a commit messages is a real life imperative statement 
    with an issue number. The body describes the behavior without the patch,
    why this is a problem, and how the patch fixes the problem when applied.]
    ```
4. Make sure you have added the necessary tests for your changes
3. Run all the tests to assure nothing else was accidentally broken.
5. Try not to pollute your pull request with unintended changes - keep them simple and small
6. Send a pull request when you feel it is ready to be merged

## Translations

Steps to create translation for a new language, assuming [language's code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) is `xx`:
 
1. Run `python manage.py makemessages -l xx`
2. Translate generated locale file `web/locale/xx/LC_MESSAGES/django.po`
2. Add your language code to `AVAILABLE_LANGUAGES` setting in `web/main/settings.py`
3. Copy `web/templates/about-en.md` file to `about-xx.md` and translate it
4. Compile locale file by running `python manage.py compilemessages -l xx`
5. Send the pull request with all the changes  

### Writing Translatable Code

When adding user-facing strings to your work, follow these guidelines:

- Use full sentences. Strings built up out of concatenated bits are hard to translate.
- Use string formatting instead of interpolation. Ex. _('Creating new user %{name}.') % { name: user.name }
- Use pluralization whenever dynamic numbers are part of translations:
```jinja2
{% trans count=list|length %}
There is {{ count }} {{ name }} object.
{% pluralize %}
There are {{ count }} {{ name }} objects.
{% endtrans %}
```

Check [Django docs](https://docs.djangoproject.com/en/1.7/topics/i18n/translation/)
 and [Jinja2 template docs](http://jinja.pocoo.org/docs/2.9/templates/#i18n-in-templates) for detailed documentation regarding translations.

### Language Corpus

To properly create n-grams it is necessary to have corpus in given language. 
While sending new language please suggest corpus that could be used for that. 
You can start your search with http://www.nltk.org/data.html.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at argumananalizi@gmail.com. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.