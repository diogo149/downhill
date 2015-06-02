'''Helper functions for rosenbrock optimization examples.'''

import climate
import downhill
import numpy as np
import theano

climate.enable_default_logging()

COLORS = ('#d62728 #1f77b4 #2ca02c #9467bd #ff7f0e '
          '#e377c2 #8c564b #bcbd22 #7f7f7f #17becf').split()


def build(algo, init):
    '''Build and return an optimizer for the rosenbrock function.

    In downhill, an optimizer can be constructed using the build() top-level
    function. This function requires several Theano quantities such as the loss
    being optimized and the parameters to update during optimization.
    '''
    x = theano.shared(np.array(init, 'f'), name='x')
    monitors = []
    if len(init) == 2:
        # this gives us access to the x and y locations during optimization.
        monitors.extend([('x', x[:-1].sum()), ('y', x[1:].sum())])
    return downhill.build(
        algo,
        loss=(100 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2).sum(),
        params=[x],
        inputs=[],
        monitors=monitors,
        monitor_gradients=True)


def build_and_trace(algo, init, limit=100, **kwargs):
    '''Run an optimizer on the rosenbrock function. Return xs, ys, and losses.

    In downhill, optimization algorithms can be iterated over to progressively
    minimize the loss. At each iteration, the optimizer yields a dictionary of
    monitor values that were computed during that iteration. Here we build an
    optimizer and then run it for a fixed number of iterations.
    '''
    kw = dict(min_improvement=0, patience=0, max_gradient_norm=100)
    kw.update(kwargs)
    xs, ys, loss = [], [], []
    for tm, _ in build(algo, init).iteropt([[]], **kw):
        xs.append(tm['x'])
        ys.append(tm['y'])
        loss.append(tm['loss'])
        if len(xs) == limit:
            break
    # Return the optimization up to any failure of patience.
    return xs[:-9], ys[:-9], loss[-9]
