import math


def bend_allowance(params, angle=90):
    return math.radians(angle) * (params.r + params.k * params.t)


def bend_deduction(params, angle = 90):
    return 2*params.ossb(angle) - bend_allowance(params,angle)


def flat_size(params, angle=90):
    bd = bend_deduction(params, angle)
    flat_length = params.length + 2 * params.height - 2 * bd
    flat_width = params.width + 2 * params.height - 2 * bd
    return flat_length, flat_width
