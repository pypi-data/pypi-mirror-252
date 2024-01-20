# Runtime Builder

Sometimes python developers want to include compiled output or other binary blob artifacts in their wheels. The source materials for this output is checked into git, but the blobs are not, since they're not source material and are at risk getting out of sync with the source distribution.

When building the wheel, the blobs need to be generated. But it may also be nice to rebuild the blobs if the source have changed at runtime to automate a step of the edit/test cycle.

This project lets you declare a single configuration describing how to build the artifacts, and build them at runtime during the development cycle or at wheel build time.

## Example

There are example projects in `tests/project_template_enscons` and `tests/project_template_setuptools`.

```
tests/project_template_setuptools
├── README.md
├── proj
│   ├── bar.source
│   ├── foo.source
│   ├── run_test.py
│   └── runtime_build
├── pyproject.toml.template
├── setup.py
├── test_pip_install.sh
└── test_pip_install_editable.sh
```

This examples uses `setuptools` and `setup.py` to build. The `setup.py` and `runtime_build` files work together to make available artifacts built from the `.source` files.

```
project_template_enscons
├── README.md
├── SConstruct
├── proj
│   ├── bar.source
│   ├── foo.source
│   ├── run_test.py
│   └── runtime_build
├── pyproject.toml.template
├── test_pip_install.sh
└── test_pip_install_editable.sh
```

Note that this example uses `enscons` to build, as `setuptools` does not easily allow fine-grained control of the contents of the `sdist` and `wheel` files. In particular, this example takes pains to include the source files `runtime_build`, `foo.source` and `bar.source` in the sdist but not the wheel.


### Configuration

Artifacts to be build must be declared in a `runtime_build` file located in the destination module of the artifacts. Each submodule can have zero or one of these build files. In the `project_template` example above, `bar.source` and `foo.source` each produce an output in the `proj` submodule, and `runtime_build` defines what the artifacts are.

This configuration file can be loaded at build time or at run time, so it *cannot* import anything that isn't made available in the `build-system.requires` section of `pyproject.toml`. In particular, it cannot import anything from the project being built since it has to be built before it can be installed in the build package, leading to a bootstrap problem.

Here is the example from above:

```python
from pathlib import Path
from typing import Callable


class MultiplyBuild:
    def __init__(self, factor: int) -> None:
        self.factor = factor

    def __call__(self, target_path: Path):
        source_path = target_path.with_suffix(".source")
        t = int(open(source_path).read())
        with open(target_path, "w") as f:
            f.write(f"{t * self.factor}")


def count_build(target_path: Path) -> None:
    source_path = target_path.with_suffix(".source")
    t = open(source_path).read()
    with open(target_path, "w") as f:
        f.write(f"{len(t)}\n")


BUILD_ARGUMENTS: dict[str, Callable[[Path], None]] = {
    "foo.val": MultiplyBuild(50),
    "bar.count": count_build,
}
```

The key is to return a `dict` object called `BUILD_ARGUMENTS` that has `str` keys corresponding to artifacts, and `Callable` values. The `Callable` should generate the given artifact.

These examples could potentially build the artifacts every time they are referenced. If a build takes long enough, you may want to add code to only build when necessary to speed the edit/test cycle.

### Build-time

The `runtime_builder` wheel is primarily a build-time dependency. If you want to take advantage of the run-time building, you need to install it in your runtime virtual environment. However, it generally should not be installed in the release version of your package.

Add it to your `pyproject.toml` file:

```toml
[build-system]
requires = ["runtime_builder", ...]
```

In the `SConstruct` file is the following line:

`built_items = build_all_items_for_package("proj")`

This returns the list of artifacts as a list of `Path` objects. These files must be included in the final wheel.

### Runtime

To use the dynamic build capabilities at runtime, use something like this boilerplate function:

```python
try:
    from runtime_builder import build_on_demand
except ImportError:
    # `runtime_builder` is an optional dependency for development only
    def build_on_demand(*args):
        pass


def load_resource(
    resource_path: str,
    package: Package,
) -> bytes:
    build_on_demand(package, resource_path)
    with as_file(files(package).joinpath(resource_path)) as target_path:
        return target_path.read_bytes()
```

This checks for presence of `runtime_builder`, and invokes it if available before accessing the resource.
