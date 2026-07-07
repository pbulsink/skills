# Roxygen2 Syntax and Type Notation

## Parameter Documentation Format

Use the following format for `@param` definitions. Always place function-specific `@param` definitions before any `@inheritParams` lines. If no parameters exist, omit both tags.

```r
#' @param param_name (`TYPE`) Brief description (usually 1-3 sentences). Include [cross_references()] if needed.
```

### Type Notation Reference

| Notation | Meaning |
|----------|---------|
| ``(`character`)`` | Character vector |
| ``(`character(1)`)`` | Single string |
| ``(`logical(1)`)`` | Single logical |
| ``(`integer`)`` | Integer vector |
| ``(`integer(1)`)`` | Single integer |
| ``(`double`)`` | Double vector |
| ``(`vector(0)`)`` | A prototype (zero-length vector) |
| ``(`vector`)`` | A vector of unspecified type |
| ``(`list`)`` | List |
| ``(`data.frame`)`` | Data frame or tibble |
| ``(`function` or `NULL`)`` | A function or NULL |
| ``(`my_class`)`` | A class-specific type (use the actual class name) |
| ``(`any`)`` | Any type |

## Enumerated Values

When a parameter takes one of a fixed set of values, use a bulleted list:

```r
#' @param method (`character(1)`) The aggregation method. Can be one of:
#'   * `"mean"`: Arithmetic mean.
#'   * `"median"`: Median value.
#'   * `"sum"`: Total sum.
```

## Returns Documentation

Use `@returns` (not `@return`). Include a type when it is informative.

```r
#' @returns A summary tibble.
#' @returns (`logical(1)`) `TRUE` if `x` is a valid record.
#' @returns Either a tibble or a list, depending on the input.
#' @returns `NULL` (invisibly).
```

**Structured returns with columns:**

```r
#' @returns A [tibble::tibble()] with columns:
#'   - `name`: Record name.
#'   - `value`: Numeric value.
#'   - `status`: Status (`"active"` or `"inactive"`).
```
