from typing import Tuple, Union

_MAXIMAL_MACHINE_PRECISION: int = 20
MAX_FRACTION_PLACES: int = 8


def signed_int_to_unsigned(number: int) -> int:
    """Return the integer value of a signed int if it would we read as un-signed in binary representation"""
    if number >= 0:
        return number

    not_power2 = abs(number) & (abs(number) - 1) != 0
    return number + 2 ** (number.bit_length() + 1 * not_power2)


def _binary_to_int(bin_rep: str, is_signed: bool) -> int:
    negative_offset: int = -(2 ** len(bin_rep)) * (bin_rep[0] == "1") * is_signed
    return int(bin_rep, 2) + negative_offset


def binary_to_float(
    bin_rep: str, fraction_part_size: int = 0, is_signed: bool = False
) -> float:
    return _binary_to_int(bin_rep, is_signed) / 2**fraction_part_size


def binary_to_float_or_int(
    bin_rep: str, fraction_part_size: int = 0, is_signed: bool = False
) -> Union[float, int]:
    if fraction_part_size == 0:
        return _binary_to_int(bin_rep, is_signed)
    return binary_to_float(bin_rep, fraction_part_size, is_signed)


def _get_fraction_places(*, binary_value: str, machine_precision: int) -> int:
    fraction_places = machine_precision
    for bit in reversed(binary_value):
        if bit == "1" or fraction_places == 0:
            return fraction_places
        fraction_places -= 1
    return fraction_places


def get_int_representation_and_fraction_places(
    float_value: float, *, machine_precision: int = MAX_FRACTION_PLACES
) -> Tuple[int, int]:
    int_val = signed_int_to_unsigned(int(float_value * 2**machine_precision))
    if int_val == 0:
        return 0, 0
    fraction_places = _get_fraction_places(
        binary_value=bin(int_val)[2:], machine_precision=machine_precision
    )
    int_val = int_val >> (machine_precision - fraction_places)
    return int_val, fraction_places


def fraction_places(
    float_value: float, *, machine_precision: int = MAX_FRACTION_PLACES
) -> int:
    int_val = signed_int_to_unsigned(int(float_value * 2**machine_precision))
    if int_val == 0:
        return 0
    return _get_fraction_places(
        binary_value=bin(int_val)[2:], machine_precision=machine_precision
    )


def _bit_length(integer_representation: int) -> int:
    return 1 if integer_representation == 0 else integer_representation.bit_length()


def binary_string(
    float_value: float, *, machine_precision: int = _MAXIMAL_MACHINE_PRECISION
) -> str:
    int_val, _ = get_int_representation_and_fraction_places(
        float_value=float_value, machine_precision=machine_precision
    )
    bin_rep = bin(int_val)[2:]
    size_diff = size(
        float_value=float_value, machine_precision=machine_precision
    ) - len(bin_rep)
    extension_bit = "0" if float_value >= 0 else "1"
    return bin_rep[::-1] + extension_bit * size_diff


def integer_part_size(
    float_value: float, *, machine_precision: int = MAX_FRACTION_PLACES
) -> int:
    int_val, fraction_places = get_int_representation_and_fraction_places(
        float_value=float_value, machine_precision=machine_precision
    )
    return max(_bit_length(int_val) - fraction_places, 0)


def size(float_value: float, *, machine_precision: int = MAX_FRACTION_PLACES) -> int:
    int_val, fraction_places = get_int_representation_and_fraction_places(
        float_value=float_value, machine_precision=machine_precision
    )
    return max(_bit_length(int_val), fraction_places)


def bounds_to_integer_part_size(
    lb: float, ub: float, *, machine_precision: int = MAX_FRACTION_PLACES
) -> int:
    lb, ub = min(lb, ub), max(lb, ub)
    ub_integer_part_size: int = integer_part_size(
        float_value=ub, machine_precision=machine_precision
    )
    lb_integer_part_size: int = integer_part_size(
        float_value=lb, machine_precision=machine_precision
    )
    if lb == 0:
        return ub_integer_part_size
    if ub == 0:
        return lb_integer_part_size
    is_extra_bit_needed = lb < 0 < ub and ub_integer_part_size >= lb_integer_part_size
    return max(ub_integer_part_size + 1 * is_extra_bit_needed, lb_integer_part_size)


def limit_fraction_places(number: float, *, machine_precision: int) -> float:
    bin_rep = binary_string(number, machine_precision=machine_precision)[::-1]
    frac_places = fraction_places(number, machine_precision=machine_precision)
    return binary_to_float(
        bin_rep=bin_rep, fraction_part_size=frac_places, is_signed=number < 0
    )
