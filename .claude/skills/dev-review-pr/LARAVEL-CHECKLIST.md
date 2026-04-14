# Laravel PR Review Checklist

Check every item for PHP/Laravel files in the PR.

## Security (Critical)

- [ ] No raw SQL queries without parameter binding
- [ ] Input validated via Form Requests (not inline in controller)
- [ ] No mass assignment vulnerabilities (`$fillable` or `$guarded` defined)
- [ ] Sensitive data not exposed in API responses (use API Resources)
- [ ] Authentication/authorization applied to protected routes
- [ ] No hardcoded credentials or secrets

## Architecture

- [ ] Business logic in Service classes, NOT controllers
- [ ] Controllers are thin — validate, delegate, respond
- [ ] API Resources used for JSON transformation
- [ ] Form Requests for validation
- [ ] Dependency injection via constructor or method injection
- [ ] PSR-12 coding standards followed

## Database

- [ ] Eager loading used to prevent N+1 queries (`with()`)
- [ ] Migrations are reversible (`down()` method works)
- [ ] Foreign key constraints defined
- [ ] Indexes on frequently queried columns
- [ ] No raw queries when Eloquent can do it

## Performance

- [ ] Long-running tasks dispatched to queues
- [ ] Database queries are efficient (no SELECT *)
- [ ] Caching applied where appropriate
- [ ] No unnecessary model loading

## Code Quality

- [ ] PHP 8.2+ features used (readonly, enums, typed properties)
- [ ] All methods have parameter and return type hints
- [ ] No deprecated Laravel features used
- [ ] Consistent naming: models singular, tables plural, controllers resource-named
- [ ] Config values not hardcoded — use `config()` or `.env`

## Testing

- [ ] Feature tests for new endpoints
- [ ] Queue::fake() / Mail::fake() for side effects
- [ ] Factory-based test data (not hardcoded)
- [ ] Tests verify response structure and status codes
- [ ] Edge cases covered (validation errors, not found, unauthorized)
- [ ] Coverage >85% for changed files
