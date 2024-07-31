# HEIR Jupyter playground

This is a way to start running [HEIR](https://heir.dev) compiler passes
in a Jupyter notebook or IPython notebook without
having to build the entire HEIR project from scratch.

Uses the [nightly HEIR build](https://github.com/google/heir/releases/tag/nightly).

## Usage

In Jupyter:

```python
%load_ext heir_play
```

```python
%%heir_opt --convert-if-to-select --canonicalize

func.func @secret_condition_with_non_secret_int(%inp: i16, %cond: !secret.secret<i1>) -> !secret.secret<i16> {
  %0 = secret.generic ins(%inp, %cond : i16, !secret.secret<i1>) {
  ^bb0(%copy_inp: i16, %secret_cond: i1):
    %1 = scf.if %secret_cond -> (i16) {
      %2 = arith.addi %copy_inp, %copy_inp : i16
      scf.yield %2 : i16
    } else {
      scf.yield %copy_inp : i16
    }
    secret.yield %1 : i16
  } -> !secret.secret<i16>
  return %0 : !secret.secret<i16>
}
```

