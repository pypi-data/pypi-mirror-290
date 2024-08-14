"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/7/23 9:59
@Function: visualization.py
@Contact: cuijinghao@tgqs.net
"""
from tgqSim.circuit.common_gates import (BASE_SINGLE_GATE,
                                         BASE_DOUBLE_GATE,
                                         BASE_TRIPLE_GATE,
                                         CONTROLLED_GATE,
                                         ROTATION_GATE)

# contain all the gates available, grant each gate a symbol to represent
# for controlled gates, one node is 'C', the other node is its symbol string, e.g. 'NOT'
GATE_SYMBOL_DICT = {'rzz': 'Z', 'ryy': 'Y', 'rxx': 'X',
                    'x': 'PauliX', 'y': 'PauliY', 'z': 'PauliZ',
                    'cp': 'CPhase',
                    'cx': 'NOT', 'cz': 'Z', 'ccx': 'NOT',
                    's': 'S', 'sdg': 'Sdg', 't': 'T', 'tdg': 'Tdg',
                    'h': 'H', 'u3': 'U3',
                    'rx': 'Rx', 'ry': 'Ry', 'rz': 'Rz',
                    'syc': 'SYC',
                    'swap': 'SWAP', 'cswap': 'SWAP', 'iswap': 'ISWAP'}


# class Visualizer:
#     def __init__(self):
#         self.diagram_str = ''
#         self.diagram = ''


def to_text_diagram(gates: list, width: int):
    # [(0, ('h',)), ([0, 1], ('cx',)), (0, ('rz', 0.708)), (0, ('rz', 0.0)), (0, ('rz', -0.5)),
    #  (1, ('u3', 0.708, 0.708, 0.708)), ([0, 1], ('measure',))]
    max_gate_length = max(len(GATE_SYMBOL_DICT[gate[1][0]]) for gate in gates) if gates else 1
    # colum_width refers to gate width, while width refers to the number of qubits
    column_width = max_gate_length + 2
    diagram_str = ['-' * (len(gates) * column_width + 1) for _ in range(width)]
    for col, (qubits, gate) in enumerate(gates):
        print(col, gate, qubits)
        gate = gate[0].lower()
        if isinstance(qubits, int):
            qubits = [qubits]
        # todo: not all two bit gates are control gates, need to consider gates like RXX, ISWAP etc
        # single gate
        if gate in BASE_SINGLE_GATE:
            for q in range(width):
                if q in qubits:
                    diagram_str[q] = (diagram_str[q][:col * column_width + 1]
                                      + f'{GATE_SYMBOL_DICT[gate]}'.center(column_width)
                                      + diagram_str[q][col * column_width + column_width + 1:])
                else:
                    diagram_str[q] = diagram_str[q][:col * column_width + 1] + '|'.center(column_width) + \
                                     diagram_str[q][
                                     col * column_width + column_width + 1:]
        # double gate
        elif gate in BASE_DOUBLE_GATE:
            # for controlled gates
            if gate in CONTROLLED_GATE:
                # by default, first returned result is control bit
                control, target = qubits
                for q in range(width):
                    if q == control:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + f'@'.center(column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
                    elif q == target:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + f'{GATE_SYMBOL_DICT[gate]}'.center(
                            column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
                    elif control < q < target or target < q < control:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + '|'.center(column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
                    else:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + ' '.center(column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
            # for non controlled gates
            else:
                bit0, bit1 = qubits
                for q in range(width):
                    if q == bit0:
                        diagram_str[q] = (diagram_str[q][:col * column_width + 1] +
                                          f'{GATE_SYMBOL_DICT[gate]}'.center(column_width) +
                                         diagram_str[q][col * column_width + column_width + 1:])
                    elif q == bit1:
                        diagram_str[q] = (diagram_str[q][:col * column_width + 1] +
                                          f'{GATE_SYMBOL_DICT[gate]}'.center(column_width) +
                                         diagram_str[q][col * column_width + column_width + 1:])
                    elif bit0 < q < bit1 or bit1 < q < bit0:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + '|'.center(column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
                    else:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + ' '.center(column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
        elif gate in BASE_TRIPLE_GATE:
            pass
    diagram = '\n'.join(diagram_str)
    return diagram


def _single_gate_diagram_str():
    pass


def _double_gate_diagram_str():
    pass


def _triple_gate_diagram_str():
    pass


