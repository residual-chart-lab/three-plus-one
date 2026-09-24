"""Finite-future phase observability of the actual four-channel tangent.

Run with PYTHONPATH=src and install mpmath for this diagnostic only.
Training checkpoints use the existing binary64 SGD implementation. Their
binary values are then treated as exact inputs to the smooth real SGD map.
High-precision values locate minors; interval arithmetic certifies their
nonvanishing. No saved result is used as a proof input.
"""
import argparse
import hashlib
import itertools
import json
import platform
from pathlib import Path

import mpmath
from mpmath import mp, iv
from threeplusone import (ThreePlusOneMLP, centered_singleton_seed,
                         add_transverse_vector_seed, xnor)
from threeplusone.transverse import epoch_transverse_matrix, branch_ray_phase_derivative

if not __debug__:
    raise RuntimeError('Certificate assertions must remain enabled.')


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def identity(ctx):
    return [[ctx.mpf(int(i == j)) for j in range(4)] for i in range(4)]


def matmul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(4))
             for j in range(4)] for i in range(4)]


def exact_float(ctx, x):
    numerator, denominator = x.as_integer_ratio()
    return ctx.mpf(numerator)/ctx.mpf(denominator)


def lift_state(ctx, net):
    return ([exact_float(ctx,x) for x in net.output_w],
            [[exact_float(ctx,x) for x in row] for row in net.hidden_w])


def sigmoid(ctx, x):
    return 1/(1+ctx.exp(-x))


def step(ctx, state, x, target, learning_rate):
    """Same simultaneous SGD update; K acts on the antisymmetric equal pair."""
    a,w = state
    xhat = [ctx.mpf(1)] + [ctx.mpf(v) for v in x]
    h = [sigmoid(ctx,dot(row,xhat)) for row in w]
    y = sigmoid(ctx,a[0]+dot(a[1:],h))
    d = (target-y)*y*(1-y)
    eta = learning_rate
    pair = 1
    g = h[pair]*(1-h[pair]); gp = g*(1-2*h[pair])
    K = identity(ctx)
    for j in range(3):
        K[0][j+1] = K[j+1][0] = eta*d*g*xhat[j]
        for k in range(3):
            K[j+1][k+1] += eta*d*a[pair+1]*gp*xhat[j]*xhat[k]
    anew = [a[0]+eta*d] + [a[i+1]+eta*d*h[i] for i in range(4)]
    wnew = [[w[i][j]+eta*d*a[i+1]*h[i]*(1-h[i])*xhat[j]
             for j in range(3)] for i in range(4)]
    return (anew,wnew), K


def radius(ctx, state):
    a,w = state
    # On the singleton ray, q_1=q_2 exactly. This form avoids cancellation
    # of separately rounded copies of the two irrational basis coefficients.
    scale = ctx.sqrt(ctx.mpf(2)/3)
    return [scale*(a[1]-a[2])] + [scale*(w[0][j]-w[1][j]) for j in range(3)]


def observations(ctx, net, horizon=3):
    state = lift_state(ctx,net)
    eta = exact_float(ctx,net.learning_rate)
    product = identity(ctx)
    rows,radials,maps = [],[],[]
    for k in range(horizon+1):
        R = radius(ctx,state); norm2 = dot(R,R)
        ell = [r/norm2 for r in R]
        rows.append([sum(ell[i]*product[i][j] for i in range(4)) for j in range(4)])
        radials.append(R)
        if k == horizon: break
        epoch = identity(ctx)
        for x,t in xnor():
            state,K = step(ctx,state,x,ctx.mpf(t),eta)
            epoch = matmul(K,epoch)
        maps.append(epoch)
        product = matmul(epoch,product)
    return rows,radials,maps


def determinant(rows, columns):
    n = len(rows)
    result = 0
    for p in itertools.permutations(range(n)):
        sign = (-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term = sign
        for i in range(n): term *= rows[i][columns[p[i]]]
        result += term
    return result


def strnum(x):
    return mp.nstr(x,40)


def checkpoint(net, epoch):
    assert net.output_w[2] == net.output_w[3]
    assert net.hidden_w[1] == net.hidden_w[2]
    records=[]; selected=[]
    mp.dps=80
    low,_,_=observations(mp,net)
    for size in range(1,5):
        cols=max(itertools.combinations(range(4),size),
                 key=lambda c:abs(determinant(low[:size],c)))
        selected.append(cols)
    mp.dps=120
    high,Rs,Ms=observations(mp,net)
    iv.dps=100
    enclosed,_,_=observations(iv,net)
    for size,cols in enumerate(selected,1):
        dl=determinant(low[:size],cols)
        dh=determinant(high[:size],cols)
        di=determinant(enclosed[:size],cols)
        assert dh != 0
        assert abs((dl-dh)/dh) < mp.mpf('1e-40')
        # Converting interval endpoints to mp is only for display. The
        # nonzero assertion itself compares outward-rounded interval bounds.
        excludes_zero = bool(di.a > 0 or di.b < 0)
        assert excludes_zero, (epoch,size,str(di))
        records.append({'horizon':size-1,'rank':size,'minor_columns':list(cols),
                        'minor_determinant':strnum(dh),
                        'interval_lower_approx':strnum(mp.mpf(di.a)),
                        'interval_upper_approx':strnum(mp.mpf(di.b)),
                        'interval_bounds_binary':[[int(s),str(m),int(e),int(b)]
                                                  for s,m,e,b in di._mpi_],
                        'interval_excludes_zero':excludes_zero})
    ell1=[x/dot(Rs[1],Rs[1]) for x in Rs[1]]
    ell2=[x/dot(Rs[2],Rs[2]) for x in Rs[2]]
    v1=[dot(row,Rs[0]) for row in Ms[0]]
    rho0=dot(ell1,v1)
    # Cross-check the independent high-precision recurrence against the
    # existing package's one-epoch Jacobian and phase diagnostic.
    existing=epoch_transverse_matrix(net,xnor(),representative_unit=1)
    matrix_error=max(abs(float(Ms[0][i][j])-existing[i][j])
                     for i in range(4) for j in range(4))
    phase_error=abs(float(rho0)-branch_ray_phase_derivative(net,xnor()))
    assert matrix_error < 5e-13
    assert phase_error < 5e-13
    rho1=dot(ell2,[dot(row,Rs[1]) for row in Ms[1]])
    hidden=[v1[j]-rho0*Rs[1][j] for j in range(4)]
    recurrence=dot(ell2,[dot(row,hidden) for row in Ms[1]])
    full=dot(high[2],Rs[0])
    assert abs(dot(ell1,hidden)) < mp.mpf('1e-110')
    assert abs(full-rho0*rho1-recurrence) < mp.mpf('1e-110')
    singular=mp.svd(mp.matrix(high),compute_uv=False)
    print('epoch',epoch,'ranks',[r['rank'] for r in records],
          'det4',records[-1]['minor_determinant'],flush=True)
    return {'epoch':epoch,
            'state_hex':{'output':[x.hex() for x in net.output_w],
                         'hidden':[[x.hex() for x in row] for row in net.hidden_w]},
            'rank_certificates':records,
            'observability_rows':[[strnum(x) for x in row] for row in high],
            'singular_values':[strnum(x) for x in singular],
            'existing_implementation_check':{'max_epoch_matrix_error':matrix_error,
                                              'one_epoch_phase_error':phase_error},
            'two_step':{'full_phase_derivative':strnum(full),
                        'product_of_local_phase_derivatives':strnum(rho0*rho1),
                        'hidden_component_current_readout':strnum(dot(ell1,hidden)),
                        'hidden_component_next_readout':strnum(recurrence)}}


def main(output):
    net=ThreePlusOneMLP(epsilon=1,seed_pattern=centered_singleton_seed(4))
    add_transverse_vector_seed(net,direction=(1,0,0,0),amplitude=.1,phase=0)
    checkpoints=(728,10000,100000)
    results=[]
    for epoch in range(1,checkpoints[-1]+1):
        for x,t in xnor(): net.train_one(x,t)
        if epoch in checkpoints: results.append(checkpoint(net,epoch))
    root=Path(__file__).resolve().parents[1]
    sources=[Path(__file__),root/'src/threeplusone/core.py',root/'src/threeplusone/transverse.py',root/'src/threeplusone/datasets.py']
    report={'base_commit':'a88922c79941a4a4be1e69d1b53be3ea21c57748',
            'environment':{'python':platform.python_version(),'mpmath':mpmath.__version__},
            'arithmetic':'Binary64 training checkpoints; exact binary checkpoint inputs to smooth real SGD; 80/120-decimal calculations and 100-decimal outward-rounded interval minors.',
            'scope':'Four-dimensional antisymmetric equal-pair tangent on the prescribed phase-zero branch, fixed ordered XNOR epochs, phase readout along the actual branch residual.',
            'sources_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
            'checkpoints':results,'all_checks_passed':True}
    if output: Path(output).write_text(json.dumps(report,indent=2)+'\n')
    else: print(json.dumps(report,indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output')
    main(parser.parse_args().output)
