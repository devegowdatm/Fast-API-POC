"""
    Module having logic to convert postgres record object to
    Plain python object to map the data w.r.t pydantic model
"""


class GenerateModelFields:

    def __init__(self, schema_model):
        """
        schema_model.__fields__.keys() method returns,
        list of pydantic model attributes.
        example:
            if schema_model = ItemBase
            self.schema_fields = ['name', 'description', 'price']

        """
        self.schema_fields = schema_model.__fields__.keys()

    def set_fields(self, data):
        """
            Set schema attributes to object.
            Example:
                data = prostgres Object({name: 'abc', 'descrption': 'des', 'price': 10})
                self.name = 'abc'
                self.price = 10
        """
        for field in self.schema_fields:
            setattr(self, field, data[field])
