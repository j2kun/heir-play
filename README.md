# HEIR Jupyter playground

This is a way to start running [HEIR](https://heir.dev) compiler passes
in a Jupyter notebook or IPython notebook without
having to build the entire HEIR project from scratch.

Uses the [nightly HEIR build](https://github.com/google/heir/releases/tag/nightly).

## Usage

Load Jupyter:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

In Jupyter:

```python
%load_ext heir_play
```

```mlir
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

The cell should output something similar to

```mlir
Running heir-opt...
module {
  func.func @secret_condition_with_non_secret_int(%arg0: i16, %arg1: !secret.secret<i1>) -> !secret.secret<i16> {
    %0 = arith.addi %arg0, %arg0 : i16
    %1 = secret.generic ins(%arg1 : !secret.secret<i1>) {
    ^bb0(%arg2: i1):
      %2 = arith.select %arg2, %0, %arg0 : i16
      secret.yield %2 : i16
    } -> !secret.secret<i16>
    return %1 : !secret.secret<i16>
  }
}
```
