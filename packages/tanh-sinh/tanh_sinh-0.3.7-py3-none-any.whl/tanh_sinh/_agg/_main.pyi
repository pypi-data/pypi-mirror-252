from typing import Callable, Literal

def integrate(f: Callable | tuple[Callable, Callable, Callable], a: float, b: float, eps: float, max_steps: int = 10, mode: Literal['numpy', 'sympy'] = 'numpy', verbose: bool = False):
    """
    Integrate a function `f` between `a` and `b` with accuracy `eps`.

    For more details, see

    Hidetosi Takahasi, Masatake Mori,
    Double Exponential Formulas for Numerical Integration,
    PM. RIMS, Kyoto Univ., 9 (1974), 721-741

    and

    Mori, Masatake
    Discovery of the double exponential transformation and its developments,
    Publications of the Research Institute for Mathematical Sciences,
    41 (4): 897-935, ISSN 0034-5318,
    doi:10.2977/prims/1145474600,
    <http://www.kurims.kyoto-u.ac.jp/~okamoto/paper/Publ_RIMS_DE/41-4-38.pdf>.
    """
def integrate_lr(f_left: Callable | tuple[Callable, Callable, Callable], f_right: Callable | tuple[Callable, Callable, Callable], alpha: float, eps: float, max_steps: int = 10, mode: Literal['numpy', 'sympy'] = 'numpy', verbose: bool = False):
    """Integrate a function `f` between `a` and `b` with accuracy `eps`. The
    function `f` is given in terms of two functions

        * `f_left(s) = f(a + s)`, i.e., `f` linearly scaled such that `f_left(0) =
          f(a)`, `f_left(b-a) = f(b)`,

        * `f_right(s) = f(b - s)`, i.e., `f` linearly scaled such that `f_right(0) =
          f(b)`, `f_right(b-a) = f(a)`.

    Implemented are Bailey's enhancements plus a few more tricks.

    David H. Bailey, Karthik Jeyabalan, and Xiaoye S. Li,
    Error function quadrature,
    Experiment. Math., Volume 14, Issue 3 (2005), 317-329,
    <https://projecteuclid.org/euclid.em/1128371757>.

    David H. Bailey,
    Tanh-Sinh High-Precision Quadrature,
    2006,
    <https://www.davidhbailey.com/dhbpapers/dhb-tanh-sinh.pdf>.
    """
