import argparse
import matplotlib.pyplot as plt


def initialize(s0, i0, r0):
    global s, i, r, s_result, i_result, r_result
    s = s0
    i = i0
    r = r0
    s_result = [s]
    i_result = [i]
    r_result = [r]


def observe():
    global s, i, r, s_result, i_result, r_result
    s_result.append(s)
    i_result.append(i)
    r_result.append(r)


def update(dt, beta, k):
    global s, i, r
    s += -beta * s * i * dt
    i += (beta * s * i - k * i) * dt
    r += k * i * dt


def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description='Euler method for evolution of infectious disease in a population')

    # Add the parameters positional/optional
    parser.add_argument('--s0', type=float, default=0.99,help='Initial susceptible population')
    parser.add_argument('--i0', type=float, default=0.01,help='Initial infected population')
    parser.add_argument('--r0', type=float, default=0.0,help='Initial recovered population')
    parser.add_argument('--beta', type=float, default=0.3,help='Infection rate')
    parser.add_argument('--k', type=float, default=0.1, help='Recovery rate')
    parser.add_argument('--t', type=float, default=10.0, help='Total time')
    parser.add_argument('--dt', type=float, default=0.01, help='Time step')
    parser.add_argument('--f', type=str, default=None,help='file with variables')
    parser.add_argument('--h', action='help',help='show this help message and exit')

    # Parse the arguments
    args = parser.parse_args()

    params = {}
    if args.f:
        with open(args.f, 'r') as file:
            for line in file:
                # split whitespace and = sign
                key, value = line.strip().split(' = ')
                params[key] = float(value)
    else:
        params['s0'] = args.s0
        params['i0'] = args.i0
        params['r0'] = args.r0
        params['beta'] = args.beta
        params['k'] = args.k
        params['tfinal'] = args.t
        params['dt'] = args.dt

    print(params)
    beta = params['beta']
    k = params['k']
    tfinal = params['tfinal']
    dt = params['dt']

    initialize(params['s0'], params['i0'], params['r0'])

    for _ in range(int(tfinal/dt)):
        update(dt, beta, k)
        observe()

    plt.plot(s_result, label='Susceptible')
    plt.plot(i_result, label='Infected')
    plt.plot(r_result, label='Recovered')
    plt.xlabel('Time')
    plt.ylabel('Population')
    plt.title('Disease Spread Evolution  - Euler Method')
    plt.legend()
    plt.grid()
    plt.savefig('results/disease_population_euler.png')
    plt.show()


if __name__ == '__main__':
    main()
