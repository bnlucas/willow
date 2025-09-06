# Willow

**Willow** extends Python dataclasses with a collection of mixins and utilities designed for clean, efficient, and expressive data modeling. The library focuses on serialization, deserialization, validation, updates, comparison, and computed properties, making it ideal for API models, configuration objects, and internal data structures.

## Features

---

### Mixins

- **`WillowMixin`** – Core mixin providing cached `asdict()` results, field/property introspection, dirty tracking, and automatic cache invalidation when fields are updated. Improves performance and simplifies reflective operations.

- **`Serializable`** – Adds flexible serialization to dicts or JSON, including support for computed properties and nested dataclasses. Inclusion rules (`Include` enum) allow fine-grained control over which fields are included, e.g., omit `None` values or empty collections.

- **`Updatable`** – Enables immutable-like copying and updating via `copy()`, `update()`, and `batch_update()`. `batch_update()` temporarily disables validation, which is useful when performing multiple updates at once.

- **`Validated`** – Automatic validation for fields based on metadata (`validator` and `allow_none`). Raises `ValidationError` when constraints are violated. Ensures data integrity without verbose boilerplate.

- **`Comparable`** – Provides rich comparison operators (`==`, `<`, `>`, etc.) based on field values, allowing objects to be sorted or compared naturally.

- **`Hashable`** – Computes hash values based on field values, enabling usage as keys in dictionaries or members of sets.

- **`HooksMixin`** – Provides `_on_field_update` and `_on_validation` hooks triggered during field updates or validation. Useful for side effects such as logging or change tracking.

---

### Field Utilities

- **`willow.field`** – Dataclass field wrapper supporting validation, default values, serialization aliases, ignoring, and custom (de)serializers. Makes it easy to define fields with rich metadata.

- **`@willow_property`** – Marks computed properties for inclusion in serialization (`to_dict` / `to_json`). Fully supports `@x.setter` and `@x.deleter` syntax and allows custom serialization logic through metadata.

---

### Flexible Serialization

- **Inclusion Rules** – Control which members are serialized using the `Include` enum:  
  - `ALWAYS`: Include all members.  
  - `NON_NONE`: Include only members that are not `None`.  
  - `NON_EMPTY`: Include only non-empty members (`''`, `[]`, `{}`).  
  - `NON_DEFAULT`: Include members whose value differs from the default (fields only; cannot be used with computed properties).  

- **Nested Support** – Automatically handles nested dataclasses, lists, tuples, dicts, enums, UUIDs, and datetime objects.  

- **Custom Serialization** – Per-field or per-property serializers allow transforming values before they are emitted as dicts or JSON.

---

### Deserialization

- Create dataclass instances from dicts or JSON.  
- Supports nested dataclasses, optional fields, and type-safe conversion.  
- Fields marked `willow.ignore=True` are skipped.  

---

### Error Handling

- **`ValidationError`** – Raised when a field fails validation.  
- **`DeserializeError`** – Raised on deserialization failure.  
- **`WillowError`** – Base exception class for all Willow errors.

---

---

## Installation

```bash
pip install willow
```

or

```bash
pip install git+https://github.com/bnlucas/willow.git
```

---

## Usage

### Basic dataclass with validation and serialization

```python
from dataclasses import dataclass
from willow import field, Serializable, Validated, Updatable, willow_property

@dataclass
class User(Serializable, Validated, Updatable):
    id: int = field()
    name: str = field(validator=lambda x: len(x) > 0)
    email: str = field(default="")

    @willow_property(json={"key": "displayName"})
    def display_name(self) -> str:
        return f"{self.name} <{self.email}>"

user = User(id=1, name="Alice", email="alice@nullmailer.com")
print(user.to_dict())
# {'id': 1, 'name': 'Alice', 'email': 'alice@nullmailer.com', 'display_name': 'Alice <alice@nullmailer.com>'}
print(user.to_json())
# '{"id": 1, "name": "Alice", "email": "alice@nullmailer.com", 'displayName': 'Alice <alice@nullmailer.com>'}'
```

---

### Serialization with inclusion rules

```python
from willow import Include

@dataclass
class Product(Serializable):
    __json_wrapper__ = "product"
    __inclusion__ = Include.NON_NONE

    id: int
    name: str
    description: str | None = None

p = Product(id=1, name="Widget")
print(p.to_json())
# {"product": {"id": 1, "name": "Widget"}}
```

---

### Validation

```python
try:
    User(id=2, name="")
except ValidationError as e:
    print(e.field.name, e.value)
# name ''
```

---

### Updating & copying

```python
user2 = user.update(name="Bob")
print(user2)
# User(id=1, name='Bob', email='')

with user.batch_update() as u:
    u.name = "Charlie"  # temporarily disables validation
```

---

### Comparison & hashing

```python
from willow import Comparable, Hashable

@dataclass
class UserComparable(Comparable, Hashable):
    id: int
    name: str

user1 = UserComparable(id=1, name="Alice")
user2 = UserComparable(id=2, name="Bob")

print(user1 < user2)  # True
print(hash(user1))
```

---

### Working with properties

```python
@dataclass
class Config(Serializable):
    x: int
    y: int

    @willow_property
    def sum(self) -> int:
        return self.x + self.y

c = Config(x=2, y=3)
print(c.to_dict())
# {'x': 2, 'y': 3, 'sum': 5}
```

---

### Handling private fields

By default, fields and properties starting with `_` are considered private and excluded from serialization. Use `include_private=True` to include them in `asdict()` / `to_dict()` output.

---

### Include enum

- `ALWAYS`: Include all members
- `NON_NONE`: Exclude members that are `None`
- `NON_EMPTY`: Exclude members that are empty (`''`, `[]`, `{}`)
- `NON_DEFAULT`: Exclude members equal to the default value

---

## Mixins Overview

- **WillowMixin** – Core caching, dirty field tracking, field/property introspection.
- **Serializable** – Dict/JSON serialization with wrappers and inclusion rules.
- **Updatable** – Copy/update utilities and `batch_update` context.
- **Validated** – Automatic validation using field metadata.
- **Comparable** – Rich comparison operators based on field values.
- **Hashable** – Hash based on field values.
- **HooksMixin** – Automatic hook invocation on field updates and validation.
- **@willow_property** – Mark computed properties to include during serialization.

---

## Contributing

1. Fork the [repository](https://github.com/bnlucas/willow)
2. Create a branch
3. Add tests
4. Submit a pull request

---

## License

MIT License. See [LICENSE](https://github.com/bnlucas/willow/blob/main/LICENSE).
