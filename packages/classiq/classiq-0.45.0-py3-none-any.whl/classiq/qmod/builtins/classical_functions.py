# This file was generated automatically - do not edit manually

from classiq.qmod.qmod_parameter import CArray, CBool, CInt, CReal
from classiq.qmod.symbolic import symbolic_function

from .structs import *


def qft_const_adder_phase(
    bit_index: CInt,
    value: CInt,
    reg_len: CInt,
) -> CReal:
    return symbolic_function(bit_index, value, reg_len, return_type=CReal)


def molecule_problem_to_hamiltonian(
    problem: MoleculeProblem,
) -> CArray[PauliTerm]:
    return symbolic_function(problem, return_type=CArray[PauliTerm])


def fock_hamiltonian_problem_to_hamiltonian(
    problem: FockHamiltonianProblem,
) -> CArray[PauliTerm]:
    return symbolic_function(problem, return_type=CArray[PauliTerm])


def grid_entangler_graph(
    num_qubits: CInt,
    schmidt_rank: CInt,
    grid_randomization: CBool,
) -> CArray[CArray[CInt]]:
    return symbolic_function(
        num_qubits, schmidt_rank, grid_randomization, return_type=CArray[CArray[CInt]]
    )


def hypercube_entangler_graph(
    num_qubits: CInt,
) -> CArray[CArray[CInt]]:
    return symbolic_function(num_qubits, return_type=CArray[CArray[CInt]])


def log_normal_finance_post_process(
    finance_model: LogNormalModel,
    estimation_method: FinanceFunction,
    probability: CReal,
) -> CReal:
    return symbolic_function(
        finance_model, estimation_method, probability, return_type=CReal
    )


def gaussian_finance_post_process(
    finance_model: GaussianModel,
    estimation_method: FinanceFunction,
    probability: CReal,
) -> CReal:
    return symbolic_function(
        finance_model, estimation_method, probability, return_type=CReal
    )


__all__ = [
    "qft_const_adder_phase",
    "molecule_problem_to_hamiltonian",
    "fock_hamiltonian_problem_to_hamiltonian",
    "grid_entangler_graph",
    "hypercube_entangler_graph",
    "log_normal_finance_post_process",
    "gaussian_finance_post_process",
]
