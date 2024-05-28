import argparse
import matplotlib.pyplot as plt
import numpy as np

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


def update_euler(dt, beta, k):
    global s, i, r
    s += -beta * s * i * dt
    i += (beta * s * i - k * i) * dt
    r += k * i * dt


def k_calculator(s, i, beta, k, dt):
    k_s = (-beta * s * i) * dt
    k_i = (beta * s * i - k * i) * dt
    k_r = (k * i) * dt
    return k_s, k_i, k_r


def update_runge_kutta(dt, beta, k):
    global s, i, r

    K1_s, K1_i, K1_r = k_calculator(s, i, beta, k, dt)
    K2_s, K2_i, K2_r = k_calculator(s + 0.5 * K1_s, i + 0.5 * K1_i, beta, k, dt)
    K3_s, K3_i, K3_r = k_calculator(s + 0.5 * K2_s, i + 0.5 * K2_i, beta, k, dt)
    K4_s, K4_i, K4_r = k_calculator(s + K3_s, i + K3_i, beta, k, dt)

    s += (K1_s + 2 * K2_s + 2 * K3_s + K4_s) / 6
    i += (K1_i + 2 * K2_i + 2 * K3_i + K4_i) / 6
    r += (K1_r + 2 * K2_r + 2 * K3_r + K4_r) / 6


def run_simulation(method, dt, beta, k, tfinal, s0, i0, r0):
    global s, i, r, s_result, i_result, r_result
    initialize(s0, i0, r0)  # Use passed values for initialization
    for _ in range(int(tfinal/dt)):
        if method == 'euler':
            update_euler(dt, beta, k)
        elif method == 'runge-kutta':
            update_runge_kutta(dt, beta, k)
        observe()

def calculate_error(euler_s, euler_i, euler_r, runge_s, runge_i, runge_r):
    error_s = np.abs(np.array(euler_s) - np.array(runge_s))
    error_i = np.abs(np.array(euler_i) - np.array(runge_i))
    error_r = np.abs(np.array(euler_r) - np.array(runge_r))
    return error_s, error_i, error_r

def main():
    parser = argparse.ArgumentParser(
        description='Simulate infectious disease spread using Euler or Runge-Kutta method')
    parser.add_argument('--s0', type=float, default=0.99,help='Initial susceptible population')
    parser.add_argument('--i0', type=float, default=0.01,help='Initial infected population')
    parser.add_argument('--r0', type=float, default=0.0,help='Initial recovered population')
    parser.add_argument('--beta', type=float, default=0.3, help='Infection rate')
    parser.add_argument('--k', type=float, default=0.1, help='Recovery rate')
    parser.add_argument('--t', type=float, default=10.0, help='Total time')
    parser.add_argument('--dt', type=float, default=0.01, help='Time step')
    parser.add_argument('--f', type=str, default=None,help='File with variables')
    parser.add_argument('--method', type=str, choices=['euler', 'runge-kutta'], default=None, help='Simulation method')
    parser.add_argument('--h', action='help',help='Show this help message and exit')

    args = parser.parse_args()

    params = {}
    if args.f:
        with open(args.f, 'r') as file:
            for line in file:
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

    beta = params['beta']
    k = params['k']
    tfinal = params['tfinal']
    dt = params['dt']
    s0 = params['s0']
    i0 = params['i0']
    r0 = params['r0']

    if args.method:
        run_simulation(args.method, dt, beta, k, tfinal, s0, i0, r0)
        plt.plot(s_result, label=f'Susceptible ({args.method})')
        plt.plot(i_result, label=f'Infected ({args.method})')
        plt.plot(r_result, label=f'Recovered ({args.method})')

        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.title(f'Disease Spread Simulation - {args.method}')
        plt.legend()
        plt.grid()
        plt.savefig(f'results/disease_population_{args.method}.png')
        plt.show()
    else:
        run_simulation('euler', dt, beta, k, tfinal, s0, i0, r0)
        plt.plot(s_result, label='Susceptible (Euler)')
        plt.plot(i_result, label='Infected (Euler)')
        plt.plot(r_result, label='Recovered (Euler)')
        euler_s, euler_i, euler_r = s_result.copy(), i_result.copy(), r_result.copy()
        s_result.clear()
        i_result.clear()
        r_result.clear()
        run_simulation('runge-kutta', dt, beta, k, tfinal, s0, i0, r0)
        plt.plot(s_result, label='Susceptible (Runge-Kutta)')
        plt.plot(i_result, label='Infected (Runge-Kutta)')
        plt.plot(r_result, label='Recovered (Runge-Kutta)')

        plt.xlabel('Time')
        plt.ylabel('Population')
        plt.title('Disease Spread Simulation - Euler vs Runge-Kutta')
        plt.legend()
        plt.grid()
        plt.savefig('results/disease_population_comparison.png')
        plt.show()

        error_s, error_i, error_r = calculate_error(euler_s, euler_i, euler_r, s_result, i_result, r_result)
        plt.figure()
        plt.plot(error_s, label='Error in Susceptible')
        plt.plot(error_i, label='Error in Infected')
        plt.plot(error_r, label='Error in Recovered')
        plt.xlabel('Time')
        plt.ylabel('Error')
        plt.title('Error of Euler')
        plt.legend()
        plt.grid()
        plt.savefig('results/error_euler.png')
        plt.show()



if __name__ == '__main__':
    main()
