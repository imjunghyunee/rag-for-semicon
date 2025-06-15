# Chapter 3: Introduction to the Quantum Theory of Solids

In the last chapter, we applied quantum mechanics and Schrödinger’s wave equation to determine the behavior of electrons in the presence of various potential functions. We found one important characteristic of an electron bound to an atom or bound within a finite space to be that the electron can take on only discrete values of energy; that is, the energies are quantized. We also discussed the Pauli exclusion principle, which stated that only one electron is allowed to occupy any given quantum state. In this chapter, we will generalize these concepts to the electron in a crystal lattice.

One of our goals is to determine the electrical properties of a semiconductor material, which we will then use to develop the current–voltage characteristics of semiconductor devices. Toward this end, we have two tasks in this chapter: to determine the properties of electrons in a crystal lattice and to determine the statistical characteristics of the very large number of electrons in a crystal.

## 3.0 | Preview

In this chapter, we will:

-   Develop the concept of allowed and forbidden electron energy bands in a single-crystal material, and describe conduction and valence energy bands in a semiconductor material.
-   Discuss the concept of negatively charged electrons and positively charged holes as two distinct charge carriers in a semiconductor material.
-   Develop electron energy versus momentum curves in a single-crystal material, which yields the concept of direct and indirect bandgap semiconductor materials.
-   Discuss the concept of effective mass of an electron and a hole.
-   Derive the density of quantum states in the allowed energy bands.
-   Develop the Fermi-Dirac probability function, which describes the statistical distribution of electrons among the allowed energy levels, and define the Fermi energy level.

## 3.1 Allowed and Forbidden Energy Bands

In the last chapter, we considered the one-electron, or hydrogen, atom. That analysis showed that the energy of the bound electron is quantized: Only discrete values of electron energy are allowed. The radial probability density for the electron was also determined. This function gives the probability of finding the electron at a particular distance from the nucleus and shows that the electron is not localized at a given radius. We can extrapolate these single-atom results to a crystal and qualitatively derive the concepts of allowed and forbidden energy bands. We will then apply quantum mechanics and Schrödinger’s wave equation to the problem of an electron in a single crystal. We find that the electronic energy states occur in bands of allowed states that are separated by forbidden energy bands.

### 3.1.1 Formation of Energy Bands

Figure 3.1a shows the radial probability density function for the lowest electron energy state of the single, noninteracting hydrogen atom, and Figure 3.1b shows the same probability curves for two atoms that are in close proximity to each other. The wave functions of the electrons of the two atoms overlap, which means that the two electrons will interact. This interaction or perturbation results in the discrete quantized energy level splitting into two discrete energy levels, schematically shown in Figure 3.1c. The splitting of the discrete state into two states is consistent with the Pauli exclusion principle.

A simple analogy of the splitting of energy levels by interacting particles is the following. Two identical race cars and drivers are far apart on a race track. There is no interaction between the cars, so they both must provide the same power to achieve a given speed. However, if one car pulls up close behind the other car, there is an interaction called draft. The second car will be pulled to an extent by the lead car. The lead car will therefore require more power to achieve the same speed since it is pulling the second car, and the second car will require less power since it is being pulled by the lead car. So there is a “splitting” of power (energy) of the two interacting race cars. (Keep in mind not to take analogies too literally.)

**Figure 3.1** (a) Probability density function of an isolated hydrogen atom. (b) Overlapping probability density functions of two adjacent hydrogen atoms. (c) The splitting of the \( n = 1 \) state.

|            |            |                 |
| ---------- | ---------- | --------------- |
| (a)        | (b)        | (c)             |
| \( p(r) \) | \( p(r) \) | \( p(r) \)      |
| \( r \)    | \( d_0 \)  | \( d_0 \)       |
|            |            | Electron energy |
|            |            | \( n = 1 \)     |
|            |            | \( n = 1 \)     |

**Figure 3.2** The splitting of an energy state into a band of allowed energies.

Now, if we somehow start with a regular periodic arrangement of hydrogen-type atoms that are initially very far apart, and begin pushing the atoms together, the initial quantized energy level will split into a band of discrete energy levels. This effect is shown schematically in Figure 3.2, where the parameter \( r_0 \) represents the equilibrium interatomic distance in the crystal. At the equilibrium interatomic distance, there is a band of allowed energies, but within the allowed band, the energies are at discrete levels. The Pauli exclusion principle states that the joining of atoms to form a system (crystal) does not alter the total number of quantum states regardless of size. However, since no two electrons can have the same quantum number, the discrete energy must split into a band of energies in order that each electron can occupy a distinct quantum state.

We have seen previously that, at any energy level, the number of allowed quantum states is relatively small. In order to accommodate all of the electrons in a crystal, we must have many energy levels within the allowed band. As an example, suppose that we have a system with \( 10^9 \) one-electron atoms and also suppose that, at the equilibrium interatomic distance, the width of the allowed energy band is 1 eV. For simplicity, we assume that each electron in the system occupies a different energy level and, if the discrete energy states are equidistant, then the energy levels are separated by \( 10^{-9} \) eV. This energy difference is extremely small, so that for all practical purposes, we have a quasi-continuous energy distribution through the allowed energy band. The fact that \( 10^{-9} \) eV is a very small difference between two energy states can be seen from the following example.

Consider again a regular periodic arrangement of atoms, in which each atom now contains more than one electron. Suppose the atom in this imaginary crystal contains electrons up through the \(n = 3\) energy level. If the atoms are initially very far apart, the electrons in adjacent atoms will not interact and will occupy the discrete energy levels. If these atoms are brought closer together, the outermost electrons in the \(n = 3\) energy shell will begin to interact initially, so that this discrete energy level will split into a band of allowed energies. If the atoms continue to move closer together, the electrons in the \(n = 2\) shell may begin to interact and will also split into a band of allowed energies. Finally, if the atoms become sufficiently close together, the innermost electrons in the \(n = 1\) level may interact, so that this energy level may also split into a band of allowed energies. The splitting of these discrete energy levels is qualitatively shown in Figure 3.3. If the equilibrium interatomic distance is \(r_0\), then we have bands of allowed energies that the electrons may occupy separated by bands of forbidden energies. This energy-band splitting and the formation of allowed and forbidden bands is the energy-band theory of single-crystal materials.

The actual band splitting in a crystal is much more complicated than indicated in Figure 3.3. A schematic representation of an isolated silicon atom is shown in Figure 3.4a. Ten of the 14 silicon atom electrons occupy deep-lying energy levels close to the nucleus. The four remaining valence electrons are relatively weakly bound and are the electrons involved in chemical reactions. Figure 3.4b shows the band splitting of silicon. We need only consider the \(n = 3\) level for the valence.

**Figure 3.3** Schematic showing the splitting of three energy states into allowed bands of energies.

**Figure 3.4** (a) Schematic of an isolated silicon atom. (b) The splitting of the 3s and 3p states of silicon into the allowed and forbidden energy bands.  
_(From Shockley [6].)_

Electrons, since the first two energy shells are completely full and are tightly bound to the nucleus. The 3s state corresponds to \( n = 3 \) and \( l = 0 \) and contains two quantum states per atom. This state will contain two electrons at \( T = 0 \) K. The 3p state corresponds to \( n = 3 \) and \( l = 1 \) and contains six quantum states per atom. This state will contain the remaining two electrons in the individual silicon atom.

As the interatomic distance decreases, the 3s and 3p states interact and overlap. At the equilibrium interatomic distance, the bands have again split, but now four quantum states per atom are in the lower band and four quantum states per atom are in the upper band. At absolute zero degrees, electrons are in the lowest energy state, so that all states in the lower band (the valence band) will be full and all states in the upper band (the conduction band) will be empty. The bandgap energy \( E_g \) between the top of the valence band and the bottom of the conduction band is the width of the forbidden energy band.

We have discussed qualitatively how and why bands of allowed and forbidden energies are formed in a crystal. The formation of these energy bands is directly related to the electrical characteristics of the crystal, as we will see later in our discussion.

### 3.1.2 The Kronig–Penney Model

In the previous section, we discussed qualitatively the splitting of allowed electron energies as atoms are brought together to form a crystal. The concept of allowed and forbidden energy bands can be developed more rigorously by considering quantum mechanics and Schrödinger’s wave equation. It may be easy for the reader to “get lost” in the following derivation, but the result forms the basis for the energy-band theory of semiconductors.

The potential function of a single, noninteracting, one-electron atom is shown in Figure 3.5a. Also indicated on the figure are the discrete energy levels allowed for the electron. Figure 3.5b shows the same type of potential function for the case when several atoms in close proximity are arranged in a one-dimensional array. The potential functions of adjacent atoms overlap, and the net potential function for this case is shown in Figure 3.5c. It is this potential function we would need to use in Schrödinger’s wave equation to model a one-dimensional single-crystal material.

The solution to Schrödinger’s wave equation, for this one-dimensional single-crystal lattice, is made more tractable by considering a simpler potential function. Figure 3.6 is the one-dimensional Kronig–Penney model of the periodic potential function, which is used to represent a one-dimensional single-crystal lattice. We need to solve Schrödinger’s wave equation in each region. As with previous quantum mechanical problems, the more interesting solution occurs for the case when \( E < V_0 \), which corresponds to a particle being bound within the crystal. The electrons are contained in the potential wells, but we have the possibility of tunneling between wells. The Kronig–Penney model is an idealized periodic potential representing a one-dimensional single crystal, but the results will illustrate many of the important features of the quantum behavior of electrons in a periodic lattice.

To obtain the solution to Schrödinger’s wave equation, we make use of a mathematical theorem by Bloch. The theorem states that all one-electron wave functions, for problems involving periodically varying potential energy functions, must be of the form

\[
\psi(x) = u(x)e^{j k x}
\]

(3.1)

\*Indicates sections that will aid in the total summation of understanding of semiconductor devices, but may be skipped the first time through the text without loss of continuity.

\(^1\)Other techniques, such as the nearly free electron model, can be used to predict the energy-band theory of semiconductor materials. See, for example, Kittel [3] or Wolfe et al. [14].

**Figure 3.5**

-   (a) Potential function of a single isolated atom.
-   (b) Overlapping potential functions of adjacent atoms.
-   (c) Net potential function of a one-dimensional single crystal.

**Figure 3.6**
The one-dimensional periodic potential function of the Kronig–Penney model.

-   **(a)**: Shows the potential function \( V(x) \) for a single atom with energy levels \( E_1, E_2, E_3, E_4 \).
-   **(b)**: Illustrates overlapping potential functions for multiple atoms.
-   **(c)**: Depicts the net potential function for a one-dimensional crystal.

The potential function \( V(x) \) is shown with periodic barriers and wells, representing the Kronig–Penney model. The potential is periodic with intervals \( -a-b \) to \( a+b \), with potential \( V_0 \) in the barriers.

The parameter \( k \) is called a constant of motion and will be considered in more detail as we develop the theory. The function \( u(x) \) is a periodic function with period \( (a + b) \).

We stated in Chapter 2 that the total solution to the wave equation is the product of the time-independent solution and the time-dependent solution, or

\[
\Psi(x, t) = \psi(x)\phi(t) = u(x)e^{ikx} \cdot e^{-iEt/\hbar}
\]

(3.2)

which may be written as

\[
\Psi(x, t) = u(x)e^{i(kx-Et/\hbar)}
\]

(3.3)

This traveling-wave solution represents the motion of an electron in a single-crystal material. The amplitude of the traveling wave is a periodic function and the parameter \( k \) is also referred to as a wave number.

We can now begin to determine a relation between the parameter \( k \), the total energy \( E \), and the potential \( V_0 \). If we consider region I in Figure 3.6 (0 < x < a) in which \( V(x) = 0 \), take the second derivative of Equation (3.1), and substitute this result into the time-independent Schrödinger’s wave equation given by Equation (2.13), we obtain the relation

\[
\frac{d^2u(x)}{dx^2} + 2ijk \frac{du(x)}{dx} - (k^2 - \alpha^2)u(x) = 0
\]

(3.4)

The function \( u_1(x) \) is the amplitude of the wave function in region I and the parameter \( \alpha \) is defined as

\[
\alpha^2 = \frac{2mE}{\hbar^2}
\]

(3.5)

Consider now a specific region II, \(-b < x < 0\), in which \( V(x) = V_0 \), and apply Schrödinger’s wave equation. We obtain the relation

\[
\frac{d^2u(x)}{dx^2} + 2ijk \frac{du(x)}{dx} - \left[k^2 - \frac{2mV_0}{\hbar^2}\right]u(x) = 0
\]

(3.6)

where \( u_2(x) \) is the amplitude of the wave function in region II. We may define

\[
\frac{2m}{\hbar^2}(E - V_0) = \alpha^2 - \frac{2mV_0}{\hbar^2} = \beta^2
\]

(3.7)

so that Equation (3.6) may be written as

\[
\frac{d^2u(x)}{dx^2} + 2ijk \frac{du(x)}{dx} - (k^2 - \beta^2)u(x) = 0
\]

(3.8)

Note that from Equation (3.7), if \( E \geq V_0 \), the parameter \( \beta \) is real, whereas if \( E < V_0 \), then \( \beta \) is imaginary.

The solution to Equation (3.4), for region I, is of the form

\[
u_1(x) = Ae^{\alpha x} + Be^{-\alpha x} \quad \text{for} \quad (0 < x < a)
\]

(3.9)

and the solution to Equation (3.8), for region II, is of the form

\[
u_2(x) = Ce^{\beta x} + De^{-\beta x} \quad \text{for} \quad (-b < x < 0)
\]

(3.10)

Since the potential function \( V(x) \) is everywhere finite, both the wave function \( \psi(x) \) and its first derivative \( \partial \psi(x)/\partial x \) must be continuous. This continuity condition implies that the wave amplitude function \( u(x) \) and its first derivative \( \partial u(x)/\partial x \) must also be continuous.

If we consider the boundary at \( x = 0 \) and apply the continuity condition to the wave amplitude, we have

\[
u_1(0) = u_2(0)
\]

(3.11)

Substituting Equations (3.9) and (3.10) into Equation (3.11), we obtain

\[
A + B = C - D = 0
\]

(3.12)

Now applying the condition that

\[
\frac{du*1}{dx}\bigg|*{x=0} = \frac{du*2}{dx}\bigg|*{x=0}
\]

(3.13)

we obtain

\[
(\alpha - k)A - (\alpha + k)B = (\beta - K)C + (\beta + K)D = 0
\]

(3.14)

We have considered region I as \( 0 < x < a \) and region II as \(-b < x < 0\). The periodicity and the continuity condition mean that the function \( u_1 \), as \( x \to a \), is equal to the function \( u_2 \), as \( x \to -b \). This condition may be written as

\[
u_1(a) = u_2(-b)
\]

(3.15)

Applying the solutions for \( u_1(x) \) and \( u_2(x) \) to the boundary condition in Equation (3.15) yields

\[
Ae^{\alpha a} + Be^{-\alpha a} = Ce^{\beta b} - De^{-\beta b} = 0
\]

(3.16)

The last boundary condition is

\[
\frac{du*1}{dx}\bigg|*{x=a} = \frac{du*2}{dx}\bigg|*{x=-b}
\]

(3.17)

which gives

\[
(\alpha - k)Ae^{\alpha a} - (\alpha + k)Be^{-\alpha a} = (\beta - K)Ce^{\beta b} + (\beta + K)De^{-\beta b} = 0
\]

(3.18)

We now have four homogeneous equations, Equations (3.12), (3.14), (3.16), and (3.18), with four unknowns as a result of applying the four boundary conditions. In a set of simultaneous, linear, homogeneous equations, there is a nontrivial solution if, and only if, the determinant of the coefficients is zero. In our case, the coefficients in question are the coefficients of the parameters \( A, B, C, \) and \( D \).

The evaluation of this determinant is extremely laborious and will not be considered in detail. The result is

\[
-\frac{(\alpha^2 + \beta^2)}{2\alpha \beta} (\sin \alpha a \sin \beta b) + (\cos \alpha a \cos \beta b) = \cos k(a + b)
\]

(3.19)

Equation (3.19) relates the parameter \( k \) to the total energy \( E \) (through the parameter \( \alpha \)) and the potential function \( V_0 \) (through the parameter \( \beta \)).

As we mentioned, the more interesting solutions occur for \( E < V_0 \), which applies to the electron bound within the crystal. From Equation (3.7), the parameter \( \beta \) is then an imaginary quantity. We may define

\[
\beta = j\gamma
\]

where \( \gamma \) is a real quantity. Equation (3.19) can be written in terms of \( \gamma \) as

\[
\gamma^2 - \frac{\alpha^2}{\alpha\gamma} (\sin \alpha a)(\sinh \gamma b) + (\cos \alpha a)(\cosh \gamma b) = \cos k(a + b)
\]

Equation (3.21) does not lend itself to an analytical solution, but must be solved using numerical or graphical techniques to obtain the relation between \( k, E, \) and \( V_0 \).

The solution of Schrödinger’s wave equation for a single bound particle resulted in discrete allowed energies. The solution of Equation (3.21) will result in a band of allowed energies.

To obtain an equation that is more susceptible to a graphical solution and thus will illustrate the nature of the results, let the potential barrier width \( b \rightarrow 0 \) and the barrier height \( V_0 \rightarrow \infty \), but such that the product \( bV_0 \) remains finite. Equation (3.21) then reduces to

\[
\left( \frac{mV_0ba}{\hbar^2} \right) \frac{\sin \alpha a}{\alpha a} + \cos \alpha a = \cos ka
\]

We may define a parameter \( P' \) as

\[
P' = \frac{mV_0ba}{\hbar^2}
\]

Then, finally, we have the relation

\[
P' \frac{\sin \alpha a}{\alpha a} + \cos \alpha a = \cos ka
\]

Equation (3.24) again gives the relation between the parameter \( k \), total energy \( E \) (through the parameter \( \alpha \)), and the potential barrier \( bV_0 \). We may note that Equation (3.24) is not a solution of Schrödinger’s wave equation but gives the conditions for which Schrödinger’s wave equation will have a solution. If we assume that the crystal is infinitely large, then \( k \) in Equation (3.24) can assume a continuum of values and must be real.
