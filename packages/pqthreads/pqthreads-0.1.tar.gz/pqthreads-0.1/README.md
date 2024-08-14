# Pqthreads

Pqthreads exposes class interfaces from the main GUI Thread in another
QThread in Qt for Python. In doing so, it facilitates communication between the
main (GUI) thread and a dedicated `QThread`s as offered by [Qt for Python (PySide)](https://wiki.qt.io/Qt_for_Python).

## Usage

In order to use pqhreads, you'll first need a GUI implementation (with Qt for
Python) whose interface you'd like to expose. This usually would be a class that derives from e.g.
[QMainWindow](https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QMainWindow.html). A very basic example class called `FigureWindow` can be found in [window.py](pqthreads/examples/window.py).

Using a class that inherites from [containers.WorkerItem](pqthreads/containers.py) you then choose which methods and attributes are exposed. An examples of this would be the class `FigureWorker` in [worker.py](pqthreads/examples/worker.py).

Using the GUI implementation `FigureWindow` and worker threads exposure class
`FigureWorker` the utilities from [decorator.py](pqthreads/decorator.py) can be
used to create a custom decorator:

```python
from pqthreads import decorator

DecoratorCore = decorator.DecoratorCore
DecoratorCore.add_agent('figure', window.FigureWindow, FigureWorker)
decorator_example = decorator.Decorator(DecoratorCore)
``` 

Any decorated function now runs in the worker thread, while all GUI elements run
in the (main) GUI thread.

To simplify access to worker class interfaces, a helper function is useful. This
also illustrates how to create and access new GUI elements:

```python
from pqthreads import decorator

def figure(*args, **kwargs):
    """ Create, raise or modify FigureWorker objects """
    container = controllers.worker_refs.get('figure')
    if not args:
        return container.create(**kwargs)
    figure_worker = args[0]
    container.current = figure_worker
    return figure_worker
```

This can finally be used to to expose GUI implementation in an existing python
program that will run in another worker thread.

```
@decorator_example
def main():
    fig = worker.figure(title='Initial title')
    fig.change_title(title='Another title')
    fig.close()
```

## Pittfalls

As illustrated in the previous section worker class interfaces are accessed
through the so-called `worker_refs`, which is provided in the module [`controllers`](pqthreads/controllers.py). All interfaces are provided as weak references. As soon as the decorated function is exited, the weak references will invalidate! Therefore, it's recommended to decorate the function that encompases the whole python program in question.

The module [`controllers`](pqthreads/controllers.py) also comes with an object
called ``gui_refs` that stores weak references to the GUI objects. These also will invalidate when the decorated function is left.

Finally, one should not access the `worker_refs` from the (main) GUI thread and also not access `gui_refs` from the worker thread. This can lead to trace errors and all sorts of undefined behavior. You have been warned!


## Design

Pqthreads separates the GUI elements from all programming elements in
`QThread`s. Since Qt demands that the main thread is used for GUI elements, all
other programming functionalities are moved into a dedicated `QThread`. This
shall be called the worker threads.

The following schematic depicts this design.

![Pqthreads design](doc/design.svg)

Communication between the GUI and worker threads is solely done using
Signal/Slot connections. This is facilitated by the `GUIAgent`s and
`WorkerAgent`s.

The interface of a GUI Object is exposed by means of a Worker Object in the
Worker Thread.

It is possible expose the interface of multiple types of GUI Objects (in the
shown schematic `FigureWindow` and `GraphWindow`), which requires multiple
`Worker`- and `GUIAgent`s. These are held the `GUIAgency` and `WorkerAgency`
respectively.

For each type of GUI/Worker object pair, it's also possible to instantiate
multiple objects (of the same type). GUI and Worker objects are held in the
`GUIItemContainer` and `WorkerItemContainer` respectively.

## License

An MIT style license applies for `pqthreads`, see the [LICENSE](LICENSE)
file for more details.
