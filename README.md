# Willow

**Willow** is a lightweight Python library that provides dataclass-focused utilities for serialization, deserialization, validation, and general object manipulation. It extends Python’s dataclass functionality with mixins and helper functions that simplify common tasks while keeping your data structures type-safe and consistent.

---

## Features

- **Mixins for common behaviors**
  - `Serializable`: Convert dataclasses to/from dictionaries or JSON with optional wrapper and inclusion rules.
  - `Updatable`: Immutable-style copying and updating of dataclasses.
  - `Validated`: Automatic field validation using metadata, with support for `allow_none` and exception-based validators.
  - `Comparable`: Implements rich comparison methods based on field values.
  - `Hashable`: Implements hash based on field values.
  - `WillowMixin`: Base mixin providing `_asdict()` and `_fields` caching.
  
- **Custom Field Support**
  - `willow.field`: Adds metadata options for validation, JSON serialization, default values, and more. Supports aliases, custom keys, serializers, deserializers, and ignoring fields.

- **Error Handling**
  - `DeserializeError`: Raised during deserialization failures.
  - `ValidationError`: Raised when a field fails validation.
  - `WillowError`: Base exception for all Willow errors.


- **Flexible Serialization**
  - JSON serialization with custom wrappers and inclusion rules (`Include` enum).
    - `ALWAYS`: Always include the field.
    - `NON_NULL`: Include only if the value is not `None`.
    - `NON_DEFAULT`: Include only if the value differs from the field's default.
  - Field-level control over serialization keys, aliases, and custom serializers.
  - Supports serialization of nested dataclasses, lists, tuples, dictionaries, enums, UUIDs, and datetime objects.

- **Type-Safe Deserialization**
  - Converts JSON or dicts into dataclass instances while respecting type hints.
  - Handles nested dataclasses, lists, tuples, dictionaries, enums, UUIDs, and datetime objects.
  - Optional field support for `Union[..., None]`.
  - Supports deserialization of nested dataclasses, lists, tuples, dictionaries, enums, UUIDs, and datetime objects.

---

## Installation

Install the latest release from PyPI:

```python
pip install willow
```

Or install directly from the GitHub repository:

```python
pip install git+https://github.com/bnlucas/willow.git
```

---

## Usage

### Defining a Dataclass with Willow

```python
from dataclasses import dataclass
from willow import field, Serializable, Validated, Updatable

@dataclass
class User(Serializable, Validated, Updatable):
    id: int = field()
    name: str = field(validator=lambda x: len(x) > 0)
    email: str = field(default="")
```

---

### Serialization & Deserialization

Class-level wrapper and inclusion:

```python
from dataclasses import dataclass
from willow import Serializable, Include, field

@dataclass
class User(Serializable):
    __json_wrapper__ = "user"
    __inclusion__ = Include.NON_NULL

    id: int
    name: str | None
    email: str | None = None

user = User(id=1, name="Alice", email=None)

print(user.to_json())
# {"user": {"id": 1, "name": "Alice"}}
```

Per-call overrides:

```python
json_str = user.to_json(wrapper="member", include=Include.ALWAYS)
print(json_str)
# {"member": {"id": 1, "name": "Alice", "email": null}}
```

---

### Field Metadata with `willow.field`

Custom keys, aliases, serializers, deserializers, and ignoring fields:

```python
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from willow import Serializable, Validated, field

def serialize_uuid(u: UUID) -> str:
    return str(u).replace("-", "")

def deserialize_uuid(s: str) -> UUID:
    return UUID(s)

@dataclass
class Event(Serializable, Validated):
    event_id: UUID = field(
        json={"key": "id"},
        willow={"serializer": serialize_uuid, "deserializer": deserialize_uuid},
    )
    name: str = field(json={"key": "eventName"})
    timestamp: datetime = field(
        json={"key": "ts"},
        willow={"serializer": datetime.isoformat, "deserializer": datetime.fromisoformat},
    )
    internal_note: str = field(
        default="secret",
        willow={"ignore": True}
    )
```

---

### Validation

Validators return `bool` or raise. If `allow_none=True` and value is `None`, validation is skipped.

```python
from dataclasses import dataclass
from willow import Validated, ValidationError, field

@dataclass
class User(Validated):
    id: int
    name: str = field(validator=lambda x: bool(x), allow_none=False)
    nickname: str | None = field(
        validator=lambda x: len(x) > 1 if x else True, allow_none=True
    )

# Valid instance
user = User(id=1, name="Alice", nickname=None)

# Invalid: name empty
try:
    User(id=2, name="")
except ValidationError as e:
    print(e.field.name, e.value)

# Invalid: nickname too short
try:
    User(id=3, name="Bob", nickname="A")
except ValidationError as e:
    print(e.field.name, e.value)
```

---

### Quick Reference: `willow.field`

| Argument / Metadata | Description | Notes |
|--------------------|------------|------|
| `default` | Default value if not provided | Standard dataclass behavior |
| `default_factory` | Callable to produce default | Standard dataclass behavior |
| `validator` | Callable returning `bool` or raising exception | Used by `Validated` mixin |
| `allow_none` | Skip validation if value is `None` | Only relevant for `Validated` |
| `json.key` | Custom key for (de)serialization | Overrides field name in dict/JSON |
| `json.aliases` | List of alternative keys to accept on input | Used in deserialization |
| `willow.serializer` | Callable to transform field during serialization | e.g., UUID → str |
| `willow.deserializer` | Callable to transform field during deserialization | e.g., str → UUID |
| `willow.ignore` | Boolean to omit field in (de)serialization | Defaults to `False` |

---

### Updating & Copying

```python
from dataclasses import dataclass
from willow import Updatable, field

@dataclass
class User(Updatable):
    id: int
    name: str

user = User(id=1, name="Alice")
updated_user = user.update(name="Bob")
print(updated_user)
# Output: User(id=1, name='Bob')
```

---

### Comparison & Hashing

```python
from dataclasses import dataclass
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

## Enums

- `Include`: Controls which fields are included during serialization.
  - `ALWAYS`: Always include the field.
  - `NON_NULL`: Include only if the value is not `None`.
  - `NON_DEFAULT`: Include only if the value differs from the field's default.

## Errors

- `WillowError`
- `ValidationError`
- `DeserializeError`

## Mixins

- `WillowMixin`
- `Serializable`
- `Updatable`
- `Validated`
- `Comparable`
- `Hashable`

---

## Contributing

1. Fork the [repository](https://github.com/bnlucas/willow)
2. Create a branch  
3. Add tests  
4. Submit a pull request  

---

## License

`willow` is distributed under the MIT license. See the [LICENSE](https://github.com/bnlucas/willow/blob/main/LICENSE) file for details.
