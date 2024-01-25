# Action Trees


![coverage](https://gitlab.com/roxautomation/action-trees/badges/main/coverage.svg)
![build status](https://gitlab.com/roxautomation/action-trees/badges/main/pipeline.svg)


---

**Documentation**: [https://roxautomation.gitlab.io/action-trees](https://roxautomation.gitlab.io/action-trees)

**Source Code**: [https://gitlab.com/roxautomation/action-trees](https://gitlab.com/roxautomation/action-trees)


---

# Summary

*Action Trees* is a Python framework for orchestrating hierarchical, asynchronous actions. It enables the structuring of complex processes into manageable, interdependent tasks that can be executed sequentially or in parallel, simplifying the management and execution of multi-step workflows.


## Action Trees vs. Behavior Trees

Behavior Trees (BTs) and Action Trees (ATs) use a tree-like structure but have different goals. BTs make choices about *what to do next* based on current situations, which is great for tasks needing quick decisions. ATs are about *executing* complex tasks efficiently, with a focus on robust error-handling errors and asynchronous operation.
In short, BTs are for making decisions, while ATs are for carrying out tasks effectively.


## Example - Coffee maker

Let's simulate a coffee making machine with these action hierarchy:


    - cappuccino_order
        - prepare
            - initialize
            - clean
        - make_cappuccino
            - boil_water
            - grind_coffee


An implementation would look like this:

```python
import asyncio
from action_trees import ActionItem


class AtomicAction(ActionItem):
    """Basic machine action with no children."""

    def __init__(self, name: str, duration: float = 0.1):
        super().__init__(name=name)
        self._duration = duration

    async def _on_run(self):
        await asyncio.sleep(self._duration)


class PrepareMachineAction(ActionItem):
    """Prepare the machine."""

    def __init__(self):
        super().__init__(name="prepare")
        self.add_child(AtomicAction(name="initialize"))
        self.add_child(AtomicAction(name="clean"))

    async def _on_run(self):
        # sequentially run children
        await self.get_child("initialize").start()
        await self.get_child("clean").start()


class MakeCappuccinoAction(ActionItem):
    """Make cappuccino."""

    def __init__(self):
        super().__init__(name="make_cappuccino")
        self.add_child(AtomicAction(name="boil_water"))
        self.add_child(AtomicAction(name="grind_coffee"))

    async def _on_run(self):
        # simultaneously run children
        await self.start_children_parallel()


class CappuccinoOrder(ActionItem):
    """High-level action to make a cappuccino."""

    def __init__(self):
        super().__init__(name="cappuccino_order")
        self.add_child(PrepareMachineAction())
        self.add_child(MakeCappuccinoAction())

    async def _on_run(self):
        for child in self.children:
            await child.start()


# create root order
order = CappuccinoOrder()
# start tasks in the background
await order.start()


```


# Development

**Please develop inside the container**, this will ensure all the required checks (`pylint` & `mypy`) as well as formatting (`black`)

If you are not familiar with devcontainers, read [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers) first

1. Clone this repository
2. open dir in *VS Code* `vscode .`
3. rebuild and reopen in container (you'll need `Dev Containers` extension)

**note**: if a container with `devcontainer` name already exists, an error will occur. You can remove it with
`docker container prune -f`


### What goes where

* `gitlab-ci.yml` - gitlab ci script
* `init_container.sh` script to initialize container for development.
* `setup.py` - main packge setup file
* `docs` - documentation, uses mkdocs
* `install` - scripts for preparing host system

### Version control

Version control is done with git tags using `setuptools_scm`

use `git tag v1.2.3` to update version number. Use `git describe` to show current version.

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code.

run `serve_docs.sh` from inside the container to build and serve documentation.

**note:** `pyreverse` creates images of packages and classes in `docs/uml/..`

### Pre-commit

optional. Add `precommit install` to `init_container.sh` if required.

This project was forked from [cookiecutter template](https://gitlab.com/roxautomation/python-template) template.
