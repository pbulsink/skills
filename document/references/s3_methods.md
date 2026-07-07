# S3 Methods and @rdname Grouping

## S3 Methods We Own (Generic defined in this package)

The generic function receives full documentation. Methods use `@rdname` to link back to the generic's help page, followed by `@export`.

```r
#' Format a summary object
#'
#' @param x (`any`) The object to format.
#' @param ... Additional arguments passed to methods.
#' @returns A formatted character string.
#' @keywords internal
.format_summary <- function(x, ...) {
  UseMethod(".format_summary")
}

#' @rdname .format_summary
#' @export
.format_summary.data_summary <- function(x, ...) {
  # method implementation
}
```

## S3 Methods We Don't Own (Generic from another package)

Provide standalone documentation for methods of generics defined in external packages.

```r
#' Title describing the method
#'
#' @param x (`TYPE`) Description.
#' @param ... Additional arguments (ignored).
#' @returns Description.
#' @exportS3Method pkg::generic
method.class <- function(x, ...) { ... }
```
