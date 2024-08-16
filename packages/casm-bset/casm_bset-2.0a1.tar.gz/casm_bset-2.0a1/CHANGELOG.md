# Changelog

All notable changes to `casm-bset` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [2.0a1] - 2024-08-15

This release creates the casm-bset CASM cluster expansion basis set construction module. This includes:

- Methods for generating coupled cluster expansion Hamiltonians of occupation, strain, displacement, and magnetic spin degrees of freedom (DoF) appropriate for the symmetry of any multi-component crystalline solid.
- Methods for generating C++ code for a CASM cluster expansion calculator (Clexulator) which efficiently evaluates the cluster expansion basis function for configuration represented using the CASM `ConfigDoFValues` data structure
- Generalized methods for creating symmetry adapted basis functions of other variables

This package is designed to work with the cluster expansion calculator (Clexulator) evaluation methods which are implemented in [libcasm-clexulator](https://github.com/prisms-center/CASMcode_clexulator). 

This package may be installed via pip install. This release also includes API documentation, built using Sphinx.
