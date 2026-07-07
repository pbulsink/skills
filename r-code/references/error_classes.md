# Error Classes

This package uses custom error classes for structured error handling. When throwing errors, use appropriate classes from this list:

## Common Error Classes

- `empty_input` - Input vector or data frame is empty
- `invalid_type` - Input is of incorrect type
- `missing_column` - Required column missing from data frame
- `invalid_value` - Input value is outside acceptable range
- `file_not_found` - Specified file does not exist

## Usage Pattern

```r
.pkg_abort("Input {.arg x} cannot be empty.", "empty_input", call = call)
```

The error class appears as the second argument to `.pkg_abort()`.