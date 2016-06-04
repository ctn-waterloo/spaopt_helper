import nengo
import numpy as np

from . import optimization

def optimize_radius(net, magnitude=1, Simulator=nengo.Simulator):
    assert isinstance(net, nengo.networks.EnsembleArray)

    sp_subdimensions = net.dimensions_per_ensemble
    sp_dimensions = net.n_ensembles * sp_subdimensions

    for ens in net.ea_ensembles:
        distortion = optimization.get_distortion(Simulator, ens)
        radius = optimization.find_optimal_radius(
                distortion, sp_dimensions, sp_subdimensions)
        ens.radius = magnitude * radius


def optimize_all(model, Simulator=nengo.Simulator):
    for net in model.all_networks:
        if isinstance(net, nengo.spa.State):
            optimize_radius(net.state_ensembles, magnitude=1,
                            Simulator=Simulator)
            if net.represent_identity:
                net.state_ensembles.ea_ensembles[0].radius = 1
        elif isinstance(net, nengo.spa.Bind):
            #TODO: this is giving a different result than spaopt-v4
            mag = net.input_magnitude
            optimize_radius(net.cc.product.sq1, magnitude=mag * np.sqrt(2),
                            Simulator=Simulator)
            optimize_radius(net.cc.product.sq2, magnitude=mag * np.sqrt(2),
                            Simulator=Simulator)
        elif isinstance(net, nengo.spa.Compare):
            mag = net.input_magnitude
            optimize_radius(net.product.sq1, magnitude=mag * np.sqrt(2),
                            Simulator=Simulator)
            optimize_radius(net.product.sq2, magnitude=mag * np.sqrt(2),
                            Simulator=Simulator)






