from __future__ import annotations

from dataclasses import dataclass
from willow import field, Serializable


@dataclass
class Person(Serializable):
    user_id: str = field(json={"key": "userId"})


if __name__ == "__main__":
    person = Person(user_id="abc123")
    print(person)

    data = person.to_dict()
    print(data)
    print(Person.from_dict(data))

    json = person.to_json()
    print(json)
    print(Person.from_json(json))
