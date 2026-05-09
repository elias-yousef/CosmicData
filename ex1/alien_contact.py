from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from datetime import datetime


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class SpaceStation(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def Contact_ID(self):
        if self.contact_id[0] == 'A' and self.contact_id[1] == 'C':
            return (self)
        else:
            raise ValueError("Contact ID must start with \
'"'AC'"' (Alien Contact)")

    @model_validator(mode="after")
    def telepathic_witnesses(self):
        if self.contact_type == ContactType.TELEPATHIC:
            if self.witness_count < 3:
                raise ValueError("Telepathic contact requires at \
least 3 witnesses")
        return (self)

    @model_validator(mode="after")
    def physical_type(self):
        if self.contact_type == ContactType.PHYSICAL:
            if not self.is_verified:
                raise ValueError("Physical contact reports must be verified")
        return (self)

    @model_validator(mode="after")
    def strong_signals(self):
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Strong signals (> 7.0) should include \
received messages")
        else:
            return (self)


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("======================================")
    try:
        station = SpaceStation(
            contact_id="AC_2024_001",
            contact_type=ContactType.TELEPATHIC,
            timestamp=datetime.fromisoformat("2026-04-20T14:30:00"),
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=6,
            message_received="'Greetings from Zeta Reticuli'"
            )
        print("Valid contact report:")
        print(f"ID: {station.contact_id}")
        print(f"Type: {station.contact_type.name}")
        print(f"Location: {station.location}")
        print(f"Signal: {station.signal_strength}/10")
        print(f"Duration: {station.duration_minutes} minutes")
        print(f"Witnesses: {station.witness_count}")
        print(f"Message: {station.message_received}")
        print("\n======================================")
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'])
    try:
        print("Expected validation error:")
        station = SpaceStation(
            contact_id="AC_2024_001",
            contact_type=ContactType.TELEPATHIC,
            timestamp=datetime.fromisoformat("2026-04-20T14:30:00"),
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=6,
            )
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'])
