# danbailo Cookiecutter Template

This repository uses the [cookiecutter](https://www.cookiecutter.io/) tool to
manage the template for creating new projects.

## cookiecutter

This tool uses [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) to write the
template settings and we can easily define which values ​​we want to "replace" in the
creation of a new project. We just need to write the file `cookiecutter.json` and declare which
properties must be replaced in the new template.

Example:
```json
{
    "some-variable": "foo",
    "python-file": "main",
    "common-file": "file"
}
```

Therefore, in the template directory, all places that are declared with ``{{some-variable}}``, ``{{python-file}}`` or ``{{common-file}}`` will be generated with the new name defined at the time of execution.

It is still possible to apply [Jinja filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#list-of-builtin-filters) to customize specific names from within the template.

Example:
- ``{{some-variable|lower}}`` - in the template this value will be generated in lowercase
- ``{{some-variable|upper}}`` - in the template this value will be generated in uppercase

## Requisites

Just install the cookiecutter using pip

```bash
pip install cookiecutter
```

## How to use

Call the `cookiecutter` in terminal passing the directory where it contains a cookiecutter template that configures the `cookiecutter.json` file.

# Presenting

<video width="1366" height="768" controls>
  <source src="assets/presenting.mp4" type="video/mp4">
</video>