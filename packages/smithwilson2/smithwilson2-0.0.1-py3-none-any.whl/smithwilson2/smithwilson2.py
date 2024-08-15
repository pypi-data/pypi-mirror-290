"""
INFORMATION:
This code file can be used to extrapolate forward rates using the method developed by EIOPA.
Using as input observed forward rates for the next 20 (or other value) years,
the code extrapolates these rates for a given timeframe, e.g., 80 years.

The main other parameters are:
ufr (ultimate forward rate): the rate the extrapolation of forward rates should ultimately converge to
alpha: the speed at which the fitted rates converge to the ufr.
t2: the convergence maturity, that is, the point at which fitted forward rates should have
converged to the ufr, where we specify how close this convergence needs to be.
Tau: The convergence tolerance in basis points. The fitted forward rates are constrained to be
less or equal than Tau basis points away from the ufr at the convergence maturity.

CODE ORIGIN:
The entirety of this code was written by Kilian de Ridder.
The code reproduces the VBA code EIOPA provides for use in excel.

QUICK INSTRUCTIONS:
Enter the following parameters in the following section. Then run the whole code.

If you want to write to csv, the very last lines of this file have to be un-commented.
"""
from math import log
import numpy as np
import pandas as pd

def extrapolate_with_sw(rates_obs, ufr, t2, Tau, extrapolation_target, nrofcoup, instrument, alfamin):
    # SOME PREPARATIONS -----------------------------------------------------------
    umax = len(rates_obs)  # The maximum maturity based on observed rates
    nrofrates = len(rates_obs)  # The number of observed rates
    if instrument == "Zero":
        nrofcoup = 1  # Set number of coupons to 1 if the instrument is "Zero" (no coupon payments)
    umax_nrofcoup = int(umax * nrofcoup)  # Total periods considering coupon payments
    lnUFR = np.log(1 + ufr)  # Natural log of 1 + ufr, used later in calculations

    # u (vector of maturities)
    u = np.arange(1, nrofrates + 1)  # Creates a vector of maturities from 1 to the number of rates

    def hh(z):
        # Helper function used in the calculation of hmat
        return (z + np.exp(-z)) / 2

    def hmat(u, v):
        # Calculates the h-matrix element based on the hh function
        return hh(u + v) - hh(abs(u - v))

    # Calculate the Q matrix we need later
    def calculate_Q():
        # Initialize the Q matrix
        Q = np.zeros((nrofrates, umax_nrofcoup))

        if instrument == "Zero":
            # For Zero-coupon bonds, Q is calculated based on a single payment at maturity
            for i in range(nrofrates):
                if u[i] <= umax_nrofcoup:  # Ensure the index is within bounds
                    Q[i, u[i] - 1] = np.exp(-lnUFR * u[i]) * ((1 + rates_obs[i]) ** u[i])

        elif instrument in ["Swap", "Bond"]:
            # For Swaps and Bonds, Q is calculated considering multiple coupon payments
            for i in range(nrofrates):
                for j in range(u[i] * nrofcoup):
                    Q[i, j] = np.exp(-lnUFR * (j + 1) / nrofcoup) * rates_obs[i] / nrofcoup
                Q[i, u[i] * nrofcoup - 1] = np.exp(-lnUFR * u[i]) * (1 + rates_obs[i] / nrofcoup)

        return Q

    Q = calculate_Q()  # Calculate the Q matrix

    # FINDING OPTIMAL ALPHA -----------------------------------------------------------
    # Replication of the Galfa function from VBA
    def Galfa(alfa, Q, mm, umax, nrofcoup, t2, Tau):
        """
        This function calculates the difference between g(alpha) and Tau (output1),
        as well as the gamma vector needed for further calculations.
        """
        Tau = Tau / 10000  # Convert Tau from basis points to a decimal

        h = np.zeros((umax_nrofcoup, umax_nrofcoup))  # Initialize the h matrix

        for i in range(1, umax_nrofcoup + 1):
            for j in range(1, umax_nrofcoup + 1):
                h[i-1, j-1] = hmat(alfa * i / nrofcoup, alfa * j / nrofcoup)  # Fill h matrix

        temp1 = np.ones((mm, 1)) - np.sum(Q, axis=1, keepdims=True)  # Intermediate vector for solving system

        # Solve for b (using the linear system Q @ h @ Q.T * b = temp1)
        b = np.linalg.solve(Q @ h @ Q.T, temp1)

        # Calculate gamma (intermediate result used in the main calculations)
        gamma = Q.T @ b

        # Calculate kappa, which is used to adjust the convergence
        temp2 = np.sum(gamma * np.arange(1, umax_nrofcoup + 1).reshape(-1, 1) / nrofcoup)
        temp3 = np.sum(gamma * np.sinh(alfa * np.arange(1, umax_nrofcoup + 1).reshape(-1, 1) / nrofcoup))
        kappa = (1 + alfa * temp2) / temp3

        # Calculate the output, which is the difference between the adjusted alpha and the tolerance
        output1 = alfa / abs(1 - kappa * np.exp(t2 * alfa)) - Tau
        return output1, gamma   

    # Define the AlfaScan function, which performs a finer search for optimal alpha:
    def AlfaScan(lastalfa, stepsize, Q, mm, umax, nrofcoup, t2, Tau):
        # Refines the search for the optimal alpha by decreasing the stepsize
        for alfa in np.arange(lastalfa + stepsize / 10 - stepsize, lastalfa, stepsize / 10):
            galfa_output = Galfa(alfa, Q, mm, umax, nrofcoup, t2, Tau)
            if galfa_output[0] <= 0:
                break

        output = [alfa, galfa_output[1]]
        return output

    def find_optimal_alfa(alfamin, Q, nrofrates, umax, nrofcoup, t2, Tau, precision=6):
        # First attempt to find an optimal alpha with a given minimum value
        galfa_output = Galfa(alfamin, Q = Q, mm = nrofrates, umax = 20, nrofcoup = 1, t2 = 20, Tau = 1)

        if galfa_output[0] < 0:
            # If the initial alpha is already optimal, return it
            alfa = alfamin
            gamma = galfa_output[1]
        else:
            # Otherwise, perform a broader search for the optimal alpha
            stepsize = 0.1
            alfa = alfamin + stepsize
            while alfa <= 20:
                galfa_output = Galfa(alfa, Q, nrofrates, umax, nrofcoup, t2, Tau)
                if galfa_output[0] <= 0:
                    break
                alfa += stepsize

            # Fine-tune the alpha using the AlfaScan function
            for i in range(precision - 1):
                alfascanoutput = AlfaScan(alfa, stepsize, Q, nrofrates, umax, nrofcoup, t2, Tau)
                alfa = alfascanoutput[0]
                stepsize /= 10

            gamma = alfascanoutput[1]
            return alfa, gamma

    alfa, gamma = find_optimal_alfa(alfamin, Q, nrofrates, umax, nrofcoup, t2, Tau)

    # We have found the optimal alpha

    # THE CORE OF THE SMITH-WILSON FUNCTION ---------------------------------------------
    # Calculate the discount factors, spot rates, forward rates, etc.

    def build_h_and_g_matrices(alfa, umax, nrofcoup):
        # Initialize the h and g matrices for use in discount and rate calculations
        h = np.zeros((extrapolation_target + 1, umax * nrofcoup))
        g = np.zeros((extrapolation_target + 1, umax * nrofcoup))

        # Populate the h and g matrices based on alpha and coupon frequency
        for i in range(extrapolation_target + 1):
            for j in range(1, umax * nrofcoup + 1):
                h[i, j-1] = hmat(alfa * i, alfa * j / nrofcoup)  # Populate h matrix
                if (j / nrofcoup) > i:
                    g[i, j-1] = alfa * (1 - np.exp(-alfa * j / nrofcoup) * np.cosh(alfa * i))
                else:
                    g[i, j-1] = alfa * np.exp(-alfa * i) * np.sinh(alfa * j / nrofcoup)

        return h, g

    h, g = build_h_and_g_matrices(alfa = alfa, umax = umax, nrofcoup = nrofcoup)

    def calculate_outputs():
        # Calculate the discount factors, spot rates, forward rates, etc.

        # Calculate intermediate values using h and gamma
        temptempdiscount = np.dot(h, gamma)  # Intermediate discount calculation
        tempdiscount = temptempdiscount.flatten()
        temptempintensity = np.dot(g, gamma)  # Intermediate intensity calculation
        tempintensity = temptempintensity.flatten()
        temp = np.sum((1 - np.exp(-alfa * np.arange(1, umax_nrofcoup + 1) / nrofcoup)) * gamma.flatten()[:umax_nrofcoup])

        # Initialize output arrays
        discount = np.zeros(extrapolation_target + 1)
        yldintensity = np.zeros(extrapolation_target + 1)
        yldintensity[0] = lnUFR - alfa * temp  # Initial yield intensity
        discount[0] = 1
        discount[1] = np.exp(-lnUFR) * (1 + tempdiscount[1])

        # Calculate the discount factors for each period
        for i in range(2, extrapolation_target + 1):
            discount[i] = np.exp(-lnUFR * i) * (1 + tempdiscount[i])

        # Calculate the yield intensity
        yldintensity = np.zeros(extrapolation_target + 1)
        yldintensity[0] = lnUFR - alfa * temp
        yldintensity[1] = lnUFR - np.log(1 + tempdiscount[1])

        zeroac = np.zeros(extrapolation_target + 1)  # Initialize zero-coupon annual compounding rates
        fwintensity = np.zeros(extrapolation_target + 1)  # Initialize forward intensity
        forwardcc = np.zeros(extrapolation_target + 1)  # Initialize forward rates (continuous compounding)
        forwardac = np.zeros(extrapolation_target + 1)  # Initialize forward rates (annual compounding)

        # Calculate yield intensity for each period
        for i in range(1,extrapolation_target + 1):
            yldintensity[i] = lnUFR - np.log(1 + tempdiscount[i]) / i

        # Calculate forward intensity for each period
        for i in range(0, extrapolation_target + 1):
            fwintensity[i] = lnUFR - tempintensity[i] / (1 + tempdiscount[i])

        # Calculate zero-coupon rates and forward rates for each period
        for i in range(1, extrapolation_target + 1):
            zeroac[i] = (1 / discount[i]) ** (1 / i) - 1
            forwardac[1] = zeroac[1]
            if i > 1:
                forwardac[i] = (discount[i - 1] / discount[i]) - 1

        # Calculate forward rates with continuous compounding for each period
        for i in range(1, extrapolation_target + 1):
            forwardcc[i] = np.log(1 + forwardac[i])

        # Bind results into a DataFrame
        terms_target = np.arange(extrapolation_target + 1)
        combined_df = pd.DataFrame({
            'maturities': terms_target,
            'discount factor': discount,
            'spot intensity': yldintensity,
            'spot rate': zeroac,
            'forward intensity': fwintensity,
            'forward rate cc': forwardcc,
            'forward rate ac': forwardac
        })

        return combined_df

    output = calculate_outputs()  # Calculate and compile all outputs into a DataFrame
    # Print the DataFrame
    return output
