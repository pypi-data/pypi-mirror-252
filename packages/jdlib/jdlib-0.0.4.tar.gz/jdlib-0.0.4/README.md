# jdlib

## Upload

```
# increment version in setup.py
python setup.py sdist
twine upload dist/jdlib-VERSION.tar.gz
```

## Release Notes

- 0.0.4
    - Fix `APIException` error
- 0.0.3
    - Create base view
- 0.0.2
    - Add `.dockerignore` and `.gitignore` to project template
- 0.0.1
    - Add command processing
    - Generate new project from template
