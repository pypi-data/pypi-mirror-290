# `django-deps`

Analyze dependencies between apps in your Django project.


## Rationale

Large Django projects usually involve lots of custom-made apps that interact with each other.
Over time, as the project grows, it becomes harder to keep track of dependencies between
them. Development slows down, because it's no longer clear how the code should be
structured. Using good practices, like dependency injection, becomes harder if not
impossible. Inevitably, you end up fighting with circular imports.

`django-deps` helps you tackle this problem by visualizing dependencies between the apps in
your project, and ensuring that you don't introduce cycles.


## Installation

You can install directly from GitHub:

```bash
pip install git+https://github.com/piotrekio/django-deps.git
```

Once the package is installed, add `django_deps` to your `INSTALLED_APPS`:

```
INSTALLED_APPS = [
    ...
    "django_deps",
]
```


## How to use it

`django-deps` comes with a management command that you can use in two ways.

First, you can print the list of your apps along with their direct dependencies:

```bash
python manage.py dependencies
```

Second, you can use a flag to only print information about cycles:

```bash
python manage.py dependencies --check
```

If you are using [pre-commit](https://pre-commit.com/), the repository includes
an [example config file](pre-commit-config.yaml.example), which enables a hook that will
block a commit if it introduces a cycle.


## License

See [License](LICENSE).
