<!-- Powered by BMAD™ Core -->

# Document Function

---

task:
  id: document-function
  name: Document Function
  description: Generate comprehensive documentation for a function or method in various documentation formats
  persona_default: api-documenter
  inputs:
    - function-signature (the function signature to document)
    - language (programming language: javascript, python, ruby, go, etc.)
    - doc-format (optional: jsdoc, sphinx, rdoc, godoc, javadoc - auto-detected if not specified)
  steps:
    - Parse function signature to extract name, parameters, and return type
    - Generate documentation template based on language and format
    - Add comprehensive parameter descriptions with types and constraints
    - Add detailed return value description
    - Document possible exceptions or error conditions
    - Create basic usage example
    - Add notes about side effects, performance, or important behaviors
    - Format according to documentation standard
  output: Formatted function documentation ready for insertion into codebase

---

## Purpose

This task helps you generate complete, professional function documentation in the appropriate format for your programming language. Proper documentation improves code maintainability, helps teammates understand APIs, and provides clear usage guidance.

## Prerequisites

Before starting this task:

- Function signature is available (or full function code)
- Programming language identified
- Understanding of function's purpose and behavior
- Knowledge of expected inputs/outputs

## Supported Documentation Formats

### JavaScript/TypeScript - JSDoc

```javascript
/**
 * Brief description of what the function does
 *
 * @param {Type} paramName - Parameter description
 * @param {Type} [optionalParam] - Optional parameter description
 * @returns {ReturnType} Return value description
 * @throws {ErrorType} When error occurs
 * @example
 * const result = functionName(arg1, arg2);
 */
```

### Python - Sphinx/NumPy Style

```python
"""
Brief description of what the function does.

Parameters
----------
param_name : Type
    Parameter description
optional_param : Type, optional
    Optional parameter description (default: value)

Returns
-------
ReturnType
    Return value description

Raises
------
ErrorType
    When error occurs

Examples
--------
>>> result = function_name(arg1, arg2)
>>> print(result)
"""
```

### Ruby - RDoc

```ruby
##
# Brief description of what the method does
#
# ==== Parameters
# * +param_name+ - (Type) Parameter description
# * +optional_param+ - (Type) Optional parameter description
#
# ==== Returns
# * (ReturnType) Return value description
#
# ==== Raises
# * ErrorType - When error occurs
#
# ==== Examples
#   result = function_name(arg1, arg2)
```

### Go - GoDoc

```go
// FunctionName brief description of what the function does.
//
// Parameters:
//   - paramName: Parameter description
//   - optionalParam: Optional parameter description
//
// Returns the return value description.
//
// Errors:
//   - ErrorType: When error occurs
//
// Example:
//   result := FunctionName(arg1, arg2)
```

### Java - JavaDoc

```java
/**
 * Brief description of what the method does
 *
 * @param paramName Parameter description
 * @param optionalParam Optional parameter description
 * @return Return value description
 * @throws ErrorType When error occurs
 * @see RelatedClass
 * @since 1.0
 * @example
 * <pre>
 * ReturnType result = functionName(arg1, arg2);
 * </pre>
 */
```

## Workflow Steps

### 1. Parse Function Signature

Extract key components from the function signature:

**JavaScript Example:**

```javascript
async function fetchUser(userId, options = {})
```

**Extracted:**
- **Name:** fetchUser
- **Parameters:** userId (required), options (optional, default: {})
- **Return type:** Promise (async)
- **Modifiers:** async

**Python Example:**

```python
def calculate_average(numbers: List[float], precision: int = 2) -> float:
```

**Extracted:**
- **Name:** calculate_average
- **Parameters:** numbers (List[float]), precision (int, default: 2)
- **Return type:** float

### 2. Generate Documentation Template

Choose template based on language and format:

**For JavaScript (JSDoc):**

```javascript
/**
 * [DESCRIPTION]
 *
 * @param {[TYPE]} [PARAM_NAME] - [DESCRIPTION]
 * @returns {[TYPE]} [DESCRIPTION]
 * @throws {[ERROR_TYPE]} [CONDITION]
 * @example
 * [EXAMPLE_CODE]
 */
```

### 3. Add Parameter Descriptions

For each parameter, document:

- **Type:** Data type (string, number, object, etc.)
- **Purpose:** What the parameter controls
- **Constraints:** Valid ranges, formats, or values
- **Default value:** If parameter is optional

**Example:**

```javascript
/**
 * @param {string} userId - The unique identifier for the user to fetch.
 *                          Must be a valid MongoDB ObjectId (24 hex chars).
 * @param {Object} [options] - Optional configuration object
 * @param {boolean} [options.includeDeleted=false] - Include soft-deleted users
 * @param {string[]} [options.fields] - Fields to include in response
 */
```

### 4. Add Return Value Description

Document what the function returns:

- **Type:** Return data type
- **Structure:** For objects/arrays, describe shape
- **Null/undefined cases:** When function returns nothing
- **Promise resolution:** For async functions

**Example:**

```javascript
/**
 * @returns {Promise<User>} Promise resolving to User object with properties:
 *   - id (string): User's unique identifier
 *   - email (string): User's email address
 *   - profile (Object): User profile data
 * @returns {Promise<null>} If user not found
 */
```

### 5. Document Error Conditions

List exceptions or errors the function can throw:

**Example:**

```javascript
/**
 * @throws {ValidationError} If userId is not a valid ObjectId format
 * @throws {DatabaseError} If database connection fails
 * @throws {NotFoundError} If user does not exist (when options.strict = true)
 */
```

**Python Example:**

```python
"""
Raises
------
ValueError
    If numbers list is empty
TypeError
    If numbers contains non-numeric values
"""
```

### 6. Create Usage Example

Provide clear, runnable example:

**Basic Example:**

```javascript
/**
 * @example
 * const user = await fetchUser('507f1f77bcf86cd799439011');
 * console.log(user.email); // 'user@example.com'
 */
```

**Advanced Example (optional):**

```javascript
/**
 * @example
 * // Fetch user with specific fields only
 * const user = await fetchUser('507f1f77bcf86cd799439011', {
 *   fields: ['email', 'profile.name']
 * });
 *
 * @example
 * // Include soft-deleted users
 * const deletedUser = await fetchUser('507f...', {
 *   includeDeleted: true
 * });
 */
```

### 7. Add Important Notes

Document critical behaviors:

**Side effects:**

```javascript
/**
 * @note This function modifies the global cache when user is fetched.
 * Subsequent calls with same userId will return cached data.
 */
```

**Performance considerations:**

```javascript
/**
 * @note This function makes a database query. Consider using batch
 * operations for fetching multiple users.
 */
```

**Thread safety / async concerns:**

```javascript
/**
 * @note This function is not thread-safe. Use mutex if calling
 * concurrently with same userId.
 */
```

### 8. Format According to Standard

Apply language-specific formatting rules:

**JSDoc standards:**
- Use `@param` not `@parameter`
- Use `{Type}` not `{type}`
- Use hyphens between param name and description

**Sphinx standards:**
- Use underlines for section headers
- Use proper indentation (4 spaces)
- Follow NumPy style for scientific code

## Success Criteria

Function documentation is complete when:

- [ ] Function name and signature documented
- [ ] All parameters described with types and constraints
- [ ] Return value clearly documented with type
- [ ] All possible errors/exceptions listed
- [ ] At least one usage example provided
- [ ] Important behaviors/side effects noted
- [ ] Documentation format matches language standard
- [ ] Documentation is complete enough for someone unfamiliar with the code

## Output Format

The output should be formatted documentation ready to paste into source code:

**JavaScript (JSDoc) Example:**

```javascript
/**
 * Fetches a user from the database by their unique identifier.
 *
 * This function performs a database query to retrieve user data.
 * Results are cached for 5 minutes to improve performance.
 *
 * @param {string} userId - The unique identifier for the user.
 *                          Must be a valid MongoDB ObjectId (24 hex characters).
 * @param {Object} [options] - Optional configuration object
 * @param {boolean} [options.includeDeleted=false] - Include soft-deleted users in results
 * @param {string[]} [options.fields] - Specific fields to include (improves performance)
 * @param {boolean} [options.strict=false] - Throw error if user not found
 *
 * @returns {Promise<User|null>} Promise resolving to User object with properties:
 *   - id (string): User's unique identifier
 *   - email (string): User's email address
 *   - profile (Object): User profile data
 *   Returns null if user not found and strict=false.
 *
 * @throws {ValidationError} If userId is not a valid ObjectId format
 * @throws {DatabaseError} If database connection fails
 * @throws {NotFoundError} If user not found and options.strict=true
 *
 * @example
 * // Basic usage
 * const user = await fetchUser('507f1f77bcf86cd799439011');
 * console.log(user.email);
 *
 * @example
 * // Fetch specific fields only
 * const user = await fetchUser('507f1f77bcf86cd799439011', {
 *   fields: ['email', 'profile.name']
 * });
 *
 * @example
 * // Strict mode - throws if not found
 * try {
 *   const user = await fetchUser('invalid-id', { strict: true });
 * } catch (error) {
 *   console.error('User not found:', error);
 * }
 *
 * @since 2.0.0
 * @see User
 * @see DatabaseError
 */
```

**Python (Sphinx) Example:**

```python
"""
Calculate the average of a list of numbers with configurable precision.

This function computes the arithmetic mean of the input numbers and
rounds the result to the specified number of decimal places.

Parameters
----------
numbers : List[float]
    List of numbers to average. Must contain at least one element.
precision : int, optional
    Number of decimal places to round to (default: 2).
    Must be non-negative.

Returns
-------
float
    The arithmetic mean of the input numbers, rounded to specified precision.

Raises
------
ValueError
    If numbers list is empty or precision is negative.
TypeError
    If numbers contains non-numeric values.

Examples
--------
>>> calculate_average([1.0, 2.0, 3.0])
2.0
>>> calculate_average([10, 20, 30], precision=0)
20.0
>>> calculate_average([1.234, 5.678], precision=3)
3.456

Notes
-----
This function uses Python's built-in round() which implements
banker's rounding (round half to even).

See Also
--------
median : Calculate median of numbers
std_dev : Calculate standard deviation
"""
```

## Common Pitfalls to Avoid

**❌ Vague parameter descriptions:**
```javascript
@param {string} userId - The user ID
```
✅ **Better:**
```javascript
@param {string} userId - The unique identifier for the user.
                         Must be a valid MongoDB ObjectId (24 hex characters).
```

**❌ Missing type information:**
```javascript
@param options - Configuration options
```
✅ **Better:**
```javascript
@param {Object} [options] - Optional configuration object
@param {boolean} [options.includeDeleted=false] - Include soft-deleted users
```

**❌ No usage examples:**
```javascript
// Only parameter and return documentation, no examples
```
✅ **Better:**
```javascript
@example
const user = await fetchUser('507f1f77bcf86cd799439011');
```

**❌ Not documenting error conditions:**
```javascript
// Missing @throws annotations
```
✅ **Better:**
```javascript
@throws {ValidationError} If userId is not a valid ObjectId
@throws {DatabaseError} If database connection fails
```

**❌ Copying description to every parameter:**
```javascript
@param {string} firstName - The first name
@param {string} lastName - The last name
@param {string} email - The email
```
✅ **Better:**
```javascript
@param {string} firstName - User's first name (required for profile creation)
@param {string} lastName - User's last name (used for display purposes)
@param {string} email - User's email address (must be unique, used for login)
```

## Examples

### Example 1: JavaScript Async Function

**Input:**
```javascript
async function createOrder(userId, items, paymentMethod) {
  // ... implementation
}
```

**Generated Documentation:**
```javascript
/**
 * Creates a new order for a user with specified items and payment method.
 *
 * This function validates the order data, calculates totals, processes
 * payment, and creates the order record in the database. The entire
 * operation is transactional and will roll back on any failure.
 *
 * @param {string} userId - The ID of the user placing the order.
 *                          Must be a valid registered user ID.
 * @param {OrderItem[]} items - Array of items to include in the order.
 *                               Each item must have { productId, quantity, price }.
 * @param {string} paymentMethod - Payment method identifier ('card', 'paypal', 'crypto').
 *
 * @returns {Promise<Order>} Promise resolving to created Order object with properties:
 *   - id (string): Unique order identifier
 *   - total (number): Total order amount in cents
 *   - status (string): Order status ('pending', 'paid', 'failed')
 *   - createdAt (Date): Order creation timestamp
 *
 * @throws {ValidationError} If userId invalid, items empty, or paymentMethod unsupported
 * @throws {PaymentError} If payment processing fails
 * @throws {InventoryError} If any item is out of stock
 * @throws {DatabaseError} If order creation fails
 *
 * @example
 * // Create order with credit card
 * const order = await createOrder('user-123', [
 *   { productId: 'prod-1', quantity: 2, price: 1999 },
 *   { productId: 'prod-2', quantity: 1, price: 2999 }
 * ], 'card');
 * console.log('Order ID:', order.id);
 *
 * @example
 * // Handle errors
 * try {
 *   const order = await createOrder(userId, items, 'paypal');
 * } catch (error) {
 *   if (error instanceof InventoryError) {
 *     console.error('Out of stock:', error.outOfStockItems);
 *   }
 * }
 */
```

### Example 2: Python Class Method

**Input:**
```python
def parse_csv(self, file_path: str, delimiter: str = ',', skip_header: bool = True) -> pd.DataFrame:
```

**Generated Documentation:**
```python
"""
Parse a CSV file and return a pandas DataFrame.

This method reads a CSV file from the specified path, applies
the configured parsing options, and returns the data as a
DataFrame. Large files are processed in chunks to manage memory.

Parameters
----------
file_path : str
    Absolute or relative path to the CSV file to parse.
    File must exist and be readable.
delimiter : str, optional
    Character used to separate fields in the CSV (default: ',').
    Common alternatives: '\t' for TSV, ';' for European CSV.
skip_header : bool, optional
    Whether to skip the first row as header (default: True).
    If False, generates numeric column names.

Returns
-------
pd.DataFrame
    DataFrame containing the parsed CSV data. Column names are
    taken from the header row (if skip_header=True) or generated
    as integers 0, 1, 2, ...

Raises
------
FileNotFoundError
    If file_path does not exist.
PermissionError
    If file_path is not readable due to permissions.
ValueError
    If delimiter is empty or multi-character.
pd.errors.ParserError
    If CSV file is malformed and cannot be parsed.

Examples
--------
>>> parser = CSVParser()
>>> df = parser.parse_csv('data/sales.csv')
>>> print(df.shape)
(1000, 5)

>>> # Parse TSV file without header
>>> df = parser.parse_csv('data/export.tsv', delimiter='\t', skip_header=False)
>>> print(df.columns)
Int64Index([0, 1, 2, 3], dtype='int64')

Notes
-----
For files larger than 100MB, consider using parse_csv_chunked()
for better memory efficiency.

See Also
--------
parse_csv_chunked : Parse large CSV files in chunks
to_csv : Export DataFrame to CSV format
"""
```

## Next Steps

After generating function documentation:

1. Insert documentation into source code above function definition
2. Use `write-usage-examples.md` task for more extensive examples
3. Update API reference documentation if exists
4. Run documentation linter (ESLint, pydocstyle, etc.)
5. Generate HTML docs with documentation tool (JSDoc, Sphinx, etc.)
6. Review with api-documenter agent for consistency
