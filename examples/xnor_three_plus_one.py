from threeplusone import ThreePlusOneMLP, xnor

for epsilon in (0.0, 1.0):
    net = ThreePlusOneMLP(epsilon=epsilon)
    result = net.fit(xnor())

    print(f"\nepsilon={epsilon}")
    print(result)
    print("hidden groups:", net.hidden_groups())
    print("hidden spread:", net.hidden_spread())

    for x, target in xnor():
        print(x, target, round(net.predict(x), 6))
