from pydantic import BaseModel


class Alex(BaseModel):
    age: int
    name: str


print("hi")
a = Alex(age=27, name="testing")
print(a)
