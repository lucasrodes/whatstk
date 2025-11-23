# Contributing

We are very open to have collaborators. You can freely fork and issue a pull request with your updates!
For other issues/bugs/suggestions, please report it in the [issues section](https://github.com/lucasrodes/whatstk/issues).

## Pull Requests

Pull requests to branch `develop` are accepted. Please link your forks to specific issues (you may want to open an
issue). 


Make sure to test your code before issuing a pull request:

1. Install library in develop mode, 

```bash
make install.dev
```

2. Run test script

```bash
make test
```

However, pull requests will trigger the GitHub Actions CI pipeline, which will run the tests as well.
