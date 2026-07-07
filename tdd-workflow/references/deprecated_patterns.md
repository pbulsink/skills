# Deprecated testthat Patterns

## Edition 3 Migration Guide

Replace these deprecated patterns with their modern equivalents:

```r
# Deprecated → Modern
context("Data validation")        # Remove — filename serves this purpose
expect_equivalent(x, y)          # expect_equal(x, y, ignore_attr = TRUE)
with_mock(...)                    # local_mocked_bindings(...)
expect_is(x, "data.frame")       # expect_s3_class(x, "data.frame")
```