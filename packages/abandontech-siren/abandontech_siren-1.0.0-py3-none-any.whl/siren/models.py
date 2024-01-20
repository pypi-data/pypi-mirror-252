from pydantic import BaseModel, field_validator, model_validator

MAX_OP_LEVEL = 4


class Command(BaseModel):
    command: str
    multiplayer_only: bool = False
    singleplayer_only: bool = False
    op_level: int
    block_command: bool = False
    mob_command: bool = False
    player_command: bool = False
    world_command: bool = False

    @field_validator("op_level")
    def op_level_in_range(cls, level: int):
        """Validate the op level is between the min and max values"""
        if 0 <= level <= MAX_OP_LEVEL:
            return level

        raise ValueError(f"op_level must be a value 0-{MAX_OP_LEVEL}")

    @model_validator(mode="after")
    def multiplayer_only_and_singleplayer_only_are_exclusive(self):
        if self.singleplayer_only and self.multiplayer_only:
            raise ValueError("singleplayer_only and multiplayer_only are mutually exclusive")

        return self
