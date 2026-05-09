from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from datetime import datetime


class crew_ranks(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: crew_ranks
    age: int = Field(le=80, ge=18)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(le=50, ge=0)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def Mission_id(self):
        if self.mission_id[0] == 'M':
            return (self)
        else:
            raise ValueError('Mission ID must start with "M"')
        return (self)

    @model_validator(mode="after")
    def member(self):
        commander = 0
        for cr in self.crew:
            if cr.rank is crew_ranks.captain:
                commander += 1
            elif cr.rank is crew_ranks.commander:
                commander += 1
        if commander >= 1:
            return (self)
        else:
            raise ValueError("Must have at least one Commander or Captain")
        return (self)

    @model_validator(mode="after")
    def Long_missions(self):
        if self.duration_days > 365:
            exp = sum(1 for m in self.crew if m.years_experience >= 5)
            if exp < (len(self.crew) / 2):
                raise ValueError("Long missions (> 365 days) \
need 50%' experienced crew (5+ years)")
        return (self)

    @model_validator(mode="after")
    def active(self):
        temp = True
        for member in self.crew:
            if not member.is_active:
                temp = False
        if not temp:
            raise ValueError("All crew members must be active")
        return (self)


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    try:
        member_one = CrewMember(
            member_id="ID_3455",
            name="Sarah Connor",
            rank=crew_ranks.commander,
            age=50,
            specialization="Mission Command",
            years_experience=30,
            )
        member_two = CrewMember(
            member_id="ID_3485",
            name="John Smith",
            rank=crew_ranks.lieutenant,
            age=52,
            specialization="Navigation",
            years_experience=20,
            )
        member_three = CrewMember(
            member_id="ID_3499",
            name="Alice Johnson",
            rank=crew_ranks.officer,
            age=45,
            specialization="Engineering",
            years_experience=14,
            )
        mission_one = SpaceMission(
            mission_name="Mars Colony Establishment",
            mission_id="M2024_MARS",
            destination="Mars",
            launch_date="20261225T153000",
            duration_days=900,
            budget_millions=2500.0,
            crew=[member_one, member_two, member_three]
        )
        print(f"Mission: {mission_one.mission_name}")
        print(f"ID: {mission_one.mission_id}")
        print(f"Destination: {mission_one.destination}")
        print(f"Duration: {mission_one.duration_days}")
        print(f"Budget: ${mission_one.budget_millions}M")
        print(f"Crew size: {len(mission_one.crew)}")
        for member in mission_one.crew:
            print(f"- {member.name} ({member.rank}) - {member.specialization}")
    except ValidationError as e:
        for error in e.errors():
            print(error['msg'])
