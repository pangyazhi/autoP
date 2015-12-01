import time
import rom
from autoP.user import User


class UiObject(rom.Model):
    name = rom.String(required=True, unique=True, index=True)
    description = rom.Text()
    xpath = rom.Text(index=True, keygen=rom.SIMPLE)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class Computer(rom.Model):
    name = rom.String(required=True, unique=True, index=True)
    ipAddress = rom.String(required=True)
    osVersion = rom.String(required=True)
    status = rom.String(required=True)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class Environment(rom.Model):
    name = rom.String(required=True, unique=True, index=True)
    status = rom.String(required=True)
    variables = rom.ManyToOne(Variable)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)
    client = rom.ForeignModel(Computer, required=True)
    appServer = rom.ForeignModel(Computer, required=True)
    dbServer = rom.ForeignModel(Computer, required=True)

    def add_variable(self, name, data):
        variable = Variable(name=name, data=data, parent=self)
        variable.save()


class Instance(rom.Model):
    testName = rom.String(required=True, index=True)
    suiteName = rom.String(required=True, index=True)
    status = rom.String(required=True)
    environment = rom.String(Environment)
    description = rom.Text()
    variables = rom.OneToMany(Variable)
    xpath = rom.Text(index=True, keygen=rom.SIMPLE)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class Variable(rom.Model):
    name = rom.String(required=True, unique=True, index=True)
    data = rom.String()
    description = rom.Text()
    parent = rom.ForeignModel(rom.Model)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class DataObject(rom.Model):
    name = rom.String(required=True, unique=True, index=True)
    description = rom.Text()
    data = rom.String()
    parent = rom.ForeignModel(rom.Model)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class Result(rom.Model):
    name = rom.String(required=True, unique=True, index=True)
    description = rom.Text()
    instance = rom.ForeignModel(Instance)
    parent = rom.ForeignModel(rom.Model)
    original = rom.String()
    final = rom.String()
    stopped_at = rom.Float(default=time.time)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class StepResult(Result):
    action = rom.String(required=True)
    data = rom.ForeignModel(DataObject)
    uiObject = rom.ForeignModel(UiObject)
    reason = rom.String()
    snapshot = rom.String()


class TestActivity(rom.Model):
    name = rom.String(required=True, unique=True, index=True)
    description = rom.Text()
    parent = rom.ForeignModel(rom.Model)
    author = rom.ForeignModel(User)
    enabled = rom.Boolean()
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)