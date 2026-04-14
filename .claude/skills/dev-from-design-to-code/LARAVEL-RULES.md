# Laravel Best Practices

Derived from [laravel-specialist](https://skills.sh/jeffallan/claude-skills/laravel-specialist) and [Laravel MCP docs](https://laravel.com/docs/12.x/mcp).

## Mandatory Requirements

**Must do:**
- PHP 8.2+ features: readonly, enums, typed properties
- Type hint ALL method parameters and return types
- Eager loading to prevent N+1 queries
- API Resources for JSON transformation
- Queue long-running tasks
- >85% test coverage
- Service containers and dependency injection
- PSR-12 coding standards

**Must NOT do:**
- Unprotected raw queries (SQL injection)
- Skip eager loading
- Store sensitive data unencrypted
- Business logic in controllers
- Hardcode configuration values
- Skip input validation
- Use deprecated features

## Architecture

```
app/
├── Http/
│   ├── Controllers/Api/
│   │   └── ContactController.php
│   ├── Requests/
│   │   └── StoreContactRequest.php
│   └── Resources/
│       └── ContactResource.php
├── Models/
│   └── Contact.php
├── Services/
│   └── ContactService.php
├── Jobs/
│   └── SendContactNotification.php
└── Mcp/               (if exposing MCP server)
    ├── Servers/
    ├── Tools/
    └── Resources/
```

## Model Pattern

```php
final class Contact extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = ['name', 'email', 'phone', 'subject', 'message'];

    protected function casts(): array
    {
        return [
            'subject' => ContactSubject::class, // backed enum
        ];
    }
}
```

## Controller Pattern

```php
final class ContactController extends Controller
{
    public function store(
        StoreContactRequest $request,
        ContactService $service,
    ): ContactResource {
        $contact = $service->create($request->validated());
        SendContactNotification::dispatch($contact);
        return new ContactResource($contact);
    }
}
```

## Test Pattern (Pest)

```php
it('stores a contact submission', function () {
    Queue::fake();

    $response = postJson('/api/contact', [
        'name' => 'Test User',
        'email' => 'test@example.com',
        'message' => 'Hello',
    ]);

    $response->assertCreated()
        ->assertJsonStructure(['data' => ['id', 'name', 'email']]);

    Queue::assertPushed(SendContactNotification::class);
});
```

## Laravel MCP Integration

If the project needs to expose an MCP server:

```php
// routes/ai.php
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp', AppServer::class)
    ->middleware(['auth:sanctum']);
```

Tools provide structured AI access to app data:
```php
#[Description('List all services offered')]
class ListServicesTool extends Tool
{
    public function handle(Request $request): Response
    {
        $services = Service::all();
        return Response::structured($services->toArray());
    }

    public function schema(JsonSchema $schema): array
    {
        return [
            'category' => $schema->string()->description('Filter by category'),
        ];
    }
}
```

## Validation Checkpoints

Before considering backend complete:
- [ ] All migrations run successfully
- [ ] Routes listed and correct (`php artisan route:list`)
- [ ] Queue jobs process correctly
- [ ] Tests pass with >85% coverage
- [ ] PSR-12 compliant (`./vendor/bin/pint`)
