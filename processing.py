import re
import numpy as np

class processing:
    @staticmethod
    def from_string(needed_str : str):
        needed_str = needed_str.lower()

        int_pattern = r"^(-)?(\d+)$"
        float_pattern = r"^(-)?(\d+)(\.\d+)?$"
        pattern_for_real_argument = r"^(-?\d+(\.\d+)?|\d+)?([*/])(sin|cos|tan|cot|exp)\((-?\d+(\.\d+)?)\)$"
        pattern_for_not_negative_argument = r"^(-?\d+(\.\d+)?|\d+)?([*/])(sqrt)\((\d+(\.\d+)?)\)$"

        res_match = re.match(int_pattern, needed_str)
        if res_match:
            sgn = -1.0 if res_match.group(1) == "-" else 1.0
            return sgn * float(res_match.group(2))

        res_match = re.match(float_pattern, needed_str)
        if res_match:
            sgn = -1.0 if res_match.group(1) == "-" else 1.0
            return sgn*( float(res_match.group(2))+float(res_match.group(3)) )

        if needed_str == "pi":
            return np.pi

        if needed_str == "-pi":
            return -np.pi

        if needed_str == "e":
            return np.exp(1)

        if needed_str == "-e":
            return -np.exp(1)

        if len(needed_str.split("^"))==2 and needed_str.split("^")[0].isnumeric() and needed_str.split("^")[1].isnumeric():
            return pow(float(needed_str.split("^")[0]), float(needed_str.split("^")[1]))

        res_match = re.match(pattern_for_real_argument, needed_str)
        if res_match:
            sgn = float(res_match.group(1)) if res_match.group(1) else 1.0
            oper = res_match.group(3)
            if oper == "*":
                if res_match.group(4) == "sin":
                    return sgn*np.sin(float(res_match.group(5)))
                elif res_match.group(4) == "cos":
                    return sgn*np.cos(float(res_match.group(5)))
                elif res_match.group(4) == "tan":
                    return sgn*np.tan(float(res_match.group(5)))
                elif res_match.group(4) == "cot":
                    return sgn*1/np.tan(float(res_match.group(5)))
                elif res_match.group(4) == "exp":
                    return sgn*np.exp(float(res_match.group(5)))
            elif oper == "/":
                if res_match.group(4) == "sin":
                    return sgn/np.sin(float(res_match.group(5)))
                elif res_match.group(4) == "cos":
                    return sgn/np.cos(float(res_match.group(5)))
                elif res_match.group(4) == "tan":
                    return sgn/np.tan(float(res_match.group(5)))
                elif res_match.group(4) == "cot":
                    return sgn*np.tan(float(res_match.group(5)))
                elif res_match.group(4) == "exp":
                    return sgn/np.exp(float(res_match.group(5)))

        res_match = re.match(pattern_for_not_negative_argument, needed_str)
        if res_match:
            sgn = float(res_match.group(1)) if res_match.group(1) else 1.0
            oper = res_match.group(3)
            if oper == "*":
                if res_match.group(4) == "sqrt":
                    return sgn*np.sqrt(float(res_match.group(5)))
            elif oper == "/":
                if res_match.group(4) == "sqrt":
                    return sgn/np.sqrt(float(res_match.group(5)))

        raise ValueError("Invalid Data")

