# Python for Data Analysis, 3rd Edition — Study Checklist

Wes McKinney · O'Reilly. Free online: https://wesmckinney.com/book/

> Sub-section list reconstructed from the known 3rd-edition structure (chapter titles confirmed via O'Reilly + GitHub; section 4 verified). Check items off as you drill them. **Core NumPy/pandas chapters for your practice notebook: 4, 5, 7, 8, 10, 11.**

---

## 1. Preliminaries
- [ ] What Is This Book About? · What Kinds of Data?
- [ ] Why Python for Data Analysis? (Python as glue, the two-language problem, why not Python)
- [ ] Essential Python Libraries (NumPy, pandas, matplotlib, IPython/Jupyter, SciPy, scikit-learn, statsmodels)
- [ ] Installation and Setup (Miniconda, packages, IDEs)
- [ ] Community/Conferences · Navigating This Book

## 2. Python Language Basics, IPython, and Jupyter Notebooks
- [ ] The Python Interpreter
- [ ] IPython Basics — shell, Jupyter notebook, tab completion, introspection
- [ ] Python Language Basics — language semantics, scalar types, control flow

## 3. Built-In Data Structures, Functions, and Files
- [ ] Data Structures and Sequences — tuple, list, dict, set, built-in sequence functions, comprehensions
- [ ] Functions — namespaces/scope, multiple returns, functions as objects, lambdas, generators, errors & exceptions
- [ ] Files and the Operating System — bytes and Unicode with files

## 4. NumPy Basics: Arrays and Vectorized Computation  ⭐
- [ ] The NumPy ndarray — creating ndarrays, dtypes, arithmetic, basic indexing & slicing, boolean indexing, fancy indexing, transposing/swapping axes
- [ ] Pseudorandom Number Generation
- [ ] Universal Functions (ufuncs)
- [ ] Array-Oriented Programming — `where`, math & statistical methods, boolean-array methods, sorting, unique & set logic
- [ ] File Input and Output with Arrays
- [ ] Linear Algebra
- [ ] Example: Random Walks (single + many at once)

## 5. Getting Started with pandas  ⭐
- [ ] Data Structures — Series, DataFrame, Index objects
- [ ] Essential Functionality — reindexing, dropping entries, indexing/selection/filtering, arithmetic & data alignment, function application & mapping, sorting & ranking, duplicate axis labels
- [ ] Summarizing & Descriptive Statistics — correlation & covariance, unique values / value counts / membership

## 6. Data Loading, Storage, and File Formats
- [ ] Reading & Writing Text Format — reading in pieces, writing out, other delimited formats, JSON, XML & HTML scraping
- [ ] Binary Data Formats — Excel, HDF5
- [ ] Interacting with Web APIs
- [ ] Interacting with Databases

## 7. Data Cleaning and Preparation  ⭐
- [ ] Handling Missing Data — filtering out, filling in
- [ ] Data Transformation — duplicates, mapping, replacing values, renaming axis indexes, discretization & binning, outliers, permutation & sampling, dummy/indicator variables
- [ ] Extension Data Types
- [ ] String Manipulation — built-in methods, regular expressions, pandas string functions
- [ ] Categorical Data — motivation, Categorical type, computations, categorical methods

## 8. Data Wrangling: Join, Combine, and Reshape  ⭐
- [ ] Hierarchical Indexing — reordering/sorting levels, summary stats by level, indexing with columns
- [ ] Combining & Merging — database-style joins, merging on index, concatenating along an axis, combining with overlap
- [ ] Reshaping & Pivoting — hierarchical indexing, long↔wide format

## 9. Plotting and Visualization
- [ ] matplotlib API Primer — figures & subplots, colors/markers/line styles, ticks/labels/legends, annotations, saving, configuration
- [ ] Plotting with pandas and seaborn — line, bar, histograms & density, scatter/point, facet grids & categorical
- [ ] Other Python Visualization Tools

## 10. Data Aggregation and Group Operations  ⭐
- [ ] How to Think About Group Operations — iterating, selecting columns, grouping with dicts/Series/functions/index levels
- [ ] Data Aggregation — column-wise & multiple functions, aggregated data without row indexes
- [ ] Apply: split-apply-combine — suppressing group keys, quantile/bucket analysis, worked examples (filling missing values, sampling, weighted avg & correlation, group-wise linear regression)
- [ ] Group Transforms and "Unwrapped" GroupBys
- [ ] Pivot Tables and Cross-Tabulation

## 11. Time Series  ⭐
- [ ] Date and Time Data Types and Tools — string↔datetime conversion
- [ ] Time Series Basics — indexing/selection/subsetting, duplicate indices
- [ ] Date Ranges, Frequencies, and Shifting — generating ranges, frequencies & offsets, shifting (lead/lag)
- [ ] Time Zone Handling — localization & conversion, tz-aware timestamps, operations across zones
- [ ] Periods and Period Arithmetic — frequency conversion, quarterly, timestamps↔periods, PeriodIndex from arrays
- [ ] Resampling and Frequency Conversion — downsampling, upsampling & interpolation, with periods, grouped time resampling
- [ ] Moving Window Functions — exponentially weighted, binary, user-defined

## 12. Introduction to Modeling Libraries in Python
- [ ] Interfacing Between pandas and Model Code
- [ ] Creating Model Descriptions with Patsy — formula transformations, categorical data
- [ ] Introduction to statsmodels — linear models, time series processes
- [ ] Introduction to scikit-learn

## 13. Data Analysis Examples
- [ ] Bitly Data from 1.USA.gov — counting time zones (pure Python vs pandas)
- [ ] MovieLens 1M Dataset — measuring rating disagreement
- [ ] US Baby Names 1880–2010 — analyzing naming trends
- [ ] USDA Food Database
- [ ] 2012 Federal Election Commission Database — donations by occupation/employer, bucketing amounts, by state

## Appendix A: Advanced NumPy
- [ ] ndarray Object Internals · dtype hierarchy
- [ ] Advanced Array Manipulation — reshaping, C vs FORTRAN order, concatenating/splitting, tile & repeat, take & put
- [ ] Broadcasting — over other axes, setting values by broadcasting
- [ ] Advanced ufunc Usage — instance methods, writing new ufuncs
- [ ] Structured and Record Arrays — nested dtypes, why use them
- [ ] More About Sorting — argsort & lexsort, alternative algorithms, partial sorts, searchsorted
- [ ] Writing Fast NumPy Functions with Numba — custom ufuncs
- [ ] Advanced Array I/O — memory-mapped files, HDF5
- [ ] Performance Tips — contiguous memory

## Appendix B: More on the IPython System
- [ ] Terminal Keyboard Shortcuts
- [ ] Magic Commands — `%run`, executing from clipboard
- [ ] Using the Command History — searching/reusing, input & output variables
- [ ] Interacting with the OS — shell commands & aliases, directory bookmarks
- [ ] Software Development Tools — debugger, timing (`%time`/`%timeit`), profiling (`%prun`), line-by-line profiling
- [ ] Tips for Productive Code Development — reloading modules, code design tips
- [ ] Advanced IPython Features — profiles & configuration
